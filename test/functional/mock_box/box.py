# coding: utf-8

from datetime import datetime
from os.path import dirname, join

from bottle import Bottle, debug, request, response, view, TEMPLATE_PATH
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from test.functional.mock_box.behavior.event_behavior import EventBehavior
from test.functional.mock_box.behavior.file_behavior import FileBehavior
from test.functional.mock_box.behavior.folder_behavior import FolderBehavior
from test.functional.mock_box.behavior.oauth2_behavior import OAuth2Behavior
from test.functional.mock_box.behavior.user_behavior import UserBehavior
from test.functional.mock_box.db_model import DbModel
# pylint:disable=unused-import
from test.functional.mock_box.db_model.collaboration_model import CollaborationModel
from test.functional.mock_box.db_model.event_model import EventModel
from test.functional.mock_box.db_model.file_model import FileModel
from test.functional.mock_box.db_model.folder_model import FolderModel
from test.functional.mock_box.db_model.group_model import GroupModel
from test.functional.mock_box.db_model.lock_model import LockModel
from test.functional.mock_box.db_model.share_model import ShareFileModel, ShareFolderModel
# pylint:enable=unused-import
from test.functional.mock_box.db_model.user_model import UserModel
from test.functional.mock_box.util.chaos_utils import allow_chaos
from test.functional.mock_box.util.http_utils import (
    authorize,
    log_request,
    rate_limit,
    retry_after,
    DELETE,
    GET,
    OPTIONS,
    POST,
    PUT,
    StoppableWSGIRefServer,
)


TEMPLATE_PATH.insert(0, join(dirname(__file__), 'views'))


class Box:
    """
    Fake Box. Sets up 4 webservers - one for auth, one for upload, one for events, and one for the rest of the api.
    """
    API_PORT = 18086
    UPLOAD_PORT = 18087
    OAUTH_API_PORT = 18088
    EVENT_PORT = 18089
    OAUTH_AUTHORIZE_PORT = 18090
    RATE_LIMIT_THRESHOLD = 100
    RATE_LIMIT_REQUEST_PER_SECOND = 4

    def __init__(self):
        debug(True)
        self._db_engine = None
        self._db_session = None
        self._db_session_maker = None
        self.reset_filesystem()
        # Mock Box consists of 3 webservers - one for the content API, one for the upload API, and one for OAuth2
        api, upload, oauth_api, event, oauth_authorize = Bottle(), Bottle(), Bottle(), Bottle(), Bottle()
        app_mapping = {
            self.API_PORT: api,
            self.EVENT_PORT: event,
            self.OAUTH_API_PORT: oauth_api,
            self.UPLOAD_PORT: upload,
            self.OAUTH_AUTHORIZE_PORT: oauth_authorize,
        }
        # Since we don't instantiate the servers until Box is instantiated, we have to apply the routes now
        for routed_method in (getattr(self, m) for m in dir(self) if hasattr(getattr(self, m), 'route')):
            app_port = routed_method.app
            app = app_mapping[app_port]
            app.route(routed_method.route, routed_method.verb, routed_method)
        for code in [400, 401, 404, 409, 429, 500]:
            for app in app_mapping.values():
                app.error(code)(self.handle_error)
        self._api = StoppableWSGIRefServer(host='localhost', port=self.API_PORT).run(api)
        self._upload = StoppableWSGIRefServer(host='localhost', port=self.UPLOAD_PORT).run(upload)
        self._oauth_api = StoppableWSGIRefServer(host='localhost', port=self.OAUTH_API_PORT).run(oauth_api)
        self._event = StoppableWSGIRefServer(host='localhost', port=self.EVENT_PORT).run(event)
        self._oauth_authorize = StoppableWSGIRefServer(host='localhost', port=self.OAUTH_AUTHORIZE_PORT).run(oauth_authorize)
        self._rate_limit_bucket = (self.RATE_LIMIT_THRESHOLD, datetime.utcnow())

    @staticmethod
    def handle_error(error):
        response.content_type = 'application/json'
        return error.body

    def shutdown(self):
        """Shutdown the webservers and wait for them to exit."""
        self._api.shutdown()
        self._upload.shutdown()
        self._oauth_api.shutdown()
        self._oauth_authorize.shutdown()
        self._api.wait()
        self._upload.wait()
        self._oauth_api.wait()
        self._oauth_authorize.wait()

    def reset_filesystem(self, users=(), applications=()):
        """
        Create in-memory DB that can be accessed by multiple threads.
        Set up auth requests, the rate limit bucket, and the request log.
        """
        self._db_engine = sqlalchemy.create_engine(
            'sqlite:///:memory:',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
        )
        DbModel.metadata.create_all(self._db_engine)
        self._db_session_maker = sessionmaker(bind=self._db_engine, autoflush=True)
        self._db_session = self._db_session_maker()
        self._db_session.add(FolderModel(folder_id=0))
        self._db_session.commit()
        self._rate_limit_bucket = (self.RATE_LIMIT_THRESHOLD, datetime.utcnow())
        self._request_log = []
        self._oauth_behavior = OAuth2Behavior(self._db_session)
        self._file_behavior = FileBehavior(self._db_session)
        self._folder_behavior = FolderBehavior(self._db_session)
        self._event_behavior = EventBehavior(self._db_session)
        self._user_behavior = UserBehavior(self._db_session)
        user_ids = []
        for user_info in users:
            user_name, user_login = user_info
            user_id = self.add_user(user_name, user_login)
            user_ids.append(user_id)
        for app_info in applications:
            client_id, client_secret, user_index = app_info
            self.add_application(client_id, client_secret, user_ids[user_index])

    @property
    def requests(self):
        return self._request_log

    @property
    def oauth(self):
        return self._oauth_behavior

    def add_application(self, client_id, client_secret, user_ids):
        return self._oauth_behavior.add_application(client_id, client_secret, user_ids)

    def add_user(self, name, login):
        user = UserModel(name=name, login=login)
        self._db_session.add(user)
        self._db_session.commit()
        return user.user_id

    def check_authorization_header(self):
        """
        Check that the request has an auth header and that its token matches the currently valid token.
        Further check that the token isn't expired.

        Called by methods decorated with the authorize decorator.
        """
        return self._oauth_behavior.check_authorization_header()

    def check_rate_limits(self):
        """
        Implements the token bucket algorithm, whereby incoming requests remove tokens from a fixed capacity bucket
        that is refilling at the steady state rate limit.
        In this case, the bucket capacity is RATE_LIMIT_THRESHOLD and the refill rate is RATE_LIMIT_REQUEST_PER_SECOND.

        Requests that are over the rate limit are aborted with 429 (Too Many Requests). A Retry-After header is
        specified that estimates when another request will succeed.
        """
        capactiy, timestamp = self._rate_limit_bucket
        now = datetime.utcnow()
        delta = self.RATE_LIMIT_REQUEST_PER_SECOND * (now - timestamp).microseconds / 1e6
        new_capacity = min(self.RATE_LIMIT_THRESHOLD, capactiy + delta)
        self._rate_limit_bucket = (new_capacity - 1, now)
        if new_capacity < 1:
            delay = (-(new_capacity - 4) / self.RATE_LIMIT_REQUEST_PER_SECOND) * 2
            retry_after(delay)

    def append_to_request_log(self):
        self._request_log.append((request.method, request.route))

    @log_request
    @allow_chaos
    @GET(OAUTH_AUTHORIZE_PORT, '/')
    @view('oauth2')
    def oauth2_authorize(self):
        return self._oauth_behavior.oauth2_authorize()

    @log_request
    @allow_chaos
    @POST(OAUTH_AUTHORIZE_PORT, '/')
    def oauth2_finish_loop(self):
        return self._oauth_behavior.oauth2_finish_loop()

    @log_request
    @allow_chaos
    @POST(OAUTH_API_PORT, '/token')
    def oauth2_token(self):
        return self._oauth_behavior.oauth2_token()

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @POST(UPLOAD_PORT, '/files/<file_id>/content')
    def update_file(self, file_id):
        return self._file_behavior.update_file(file_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @POST(UPLOAD_PORT, '/files/content')
    def upload_file(self):
        return self._file_behavior.upload_file()

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @GET(API_PORT, '/files/<file_id>')
    def get_file_info(self, file_id):
        return self._file_behavior.get_file_info(file_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @PUT(API_PORT, '/files/<file_id>')
    def update_file_info(self, file_id):
        return self._file_behavior.update_file_info(file_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @POST(API_PORT, '/files/<file_id>/copy')
    def copy_file(self, file_id):
        return self._file_behavior.copy_file(file_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @GET(API_PORT, '/files/<file_id>/content')
    def download_file(self, file_id):
        return self._file_behavior.download_file(file_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @DELETE(API_PORT, '/files/<file_id>')
    def delete_file(self, file_id):
        return self._file_behavior.delete_file(file_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @GET(API_PORT, '/folders/<folder_id>')
    def get_folder_info(self, folder_id):
        return self._folder_behavior.get_folder_info(folder_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @PUT(API_PORT, '/folders/<folder_id>')
    def update_folder_info(self, folder_id):
        return self._folder_behavior.update_folder_info(folder_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @POST(API_PORT, '/folders/<folder_id>/copy')
    def copy_folder(self, folder_id):
        return self._folder_behavior.copy_folder(folder_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @DELETE(API_PORT, '/folders/<folder_id>')
    def delete_folder(self, folder_id):
        return self._folder_behavior.delete_folder(folder_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @GET(API_PORT, '/folders/<folder_id>/items')
    def get_folder_items(self, folder_id):
        return self._folder_behavior.get_folder_items(folder_id)

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @POST(API_PORT, '/folders')
    def create_folder(self):
        return self._folder_behavior.create_folder()

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @GET(API_PORT, '/events')
    def get_events(self):
        return self._event_behavior.get_events()

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @OPTIONS(API_PORT, '/events')
    def get_long_poll_url(self):
        return self._event_behavior.get_long_poll_url()

    @log_request
    @allow_chaos
    @GET(EVENT_PORT, '/subscribe')
    def subscribe(self):
        return self._event_behavior.subscribe()

    @log_request
    @allow_chaos
    @GET(EVENT_PORT, '/check')
    def check(self):
        return self._event_behavior.subscribe()

    @log_request
    @rate_limit
    @authorize
    @allow_chaos
    @GET(API_PORT, '/users/<user_id>')
    def get_user_info(self, user_id):
        return self._user_behavior.get_user_info(user_id)
