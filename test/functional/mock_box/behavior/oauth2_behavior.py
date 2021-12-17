# coding: utf-8

from datetime import datetime, timedelta
import json
from uuid import uuid4

from bottle import request, redirect
from sqlalchemy.orm.exc import NoResultFound

from test.functional.mock_box.db_model.application_model import ApplicationModel
from test.functional.mock_box.db_model.token_model import TokenModel
from test.functional.mock_box.db_model.user_model import UserModel
from test.functional.mock_box.util.db_utils import get_token_record_by_token
from test.functional.mock_box.util.http_utils import abort


class OAuth2Behavior:
    ACCESS_TOKEN_DURATION_SECONDS = 3600
    REFRESH_TOKEN_DURATION_DAYS = 60
    AUTH_CODE_DURATION_SECONDS = 30

    def __init__(self, db_session):
        self._db_session = db_session
        self._auth_request = {}

    def add_application(self, client_id, client_secret, user_ids):
        users = self._db_session.query(UserModel).filter(UserModel.user_id.in_(user_ids)).all()
        app = ApplicationModel(client_id=client_id, client_secret=client_secret, users=users)
        self._db_session.add(app)
        self._db_session.commit()

    def _get_application_by_id(self, client_id):
        try:
            return self._db_session.query(ApplicationModel).filter_by(client_id=client_id).one()
        except NoResultFound:
            abort(400, 'Invalid client id: {0}'.format(client_id))

    def _get_user_by_login(self, user_login):
        try:
            return self._db_session.query(UserModel).filter_by(login=user_login).one()
        except NoResultFound:
            abort(401)

    def check_authorization_header(self):
        """
        Check that the request has an auth header and that its token matches the currently valid token.
        Further check that the token isn't expired.

        Called by methods decorated with the authorize decorator.
        """
        authorization_header = request.headers.get('Authorization')
        if not authorization_header or not authorization_header.startswith('Bearer '):
            abort(401)
        token = authorization_header[7:]
        token_record = get_token_record_by_token(self._db_session, token)
        if datetime.utcnow() > token_record.expires_at:
            abort(401)

    def _create_tokens(self, client_id, user_login=None, owned_by_id=None):
        if owned_by_id is None:
            user = self._get_user_by_login(user_login)
            owned_by_id = user.id
        app = self._get_application_by_id(client_id)
        access_token, refresh_token = uuid4().hex, uuid4().hex
        access_token_valid_until = datetime.utcnow() + timedelta(seconds=self.ACCESS_TOKEN_DURATION_SECONDS)
        refresh_token_valid_until = datetime.utcnow() + timedelta(days=self.REFRESH_TOKEN_DURATION_DAYS)
        self._db_session.add(TokenModel(
            token=access_token,
            expires_at=access_token_valid_until,
            authorized_application_id=app.id,
            owned_by_id=owned_by_id,
            token_type='access'
        ))
        self._db_session.add(TokenModel(
            token=refresh_token,
            expires_at=refresh_token_valid_until,
            authorized_application_id=app.id,
            owned_by_id=owned_by_id,
            token_type='refresh'
        ))
        return access_token, access_token_valid_until, refresh_token, refresh_token_valid_until

    def oauth2_authorize(self):
        """
        Shortcut OAuth2 authorize method. Instead of presenting a webview for a user to login, provides the code
        directly. Saves the tokens so they can be issued by calls to token.
        """
        code = uuid4().hex
        state = request.params.state
        client_id = request.params.client_id
        redirect_uri = request.params.redirect_uri
        user_login = request.params.get('box_login', '')
        self._auth_request = {
            'code': code,
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'state': state,
        }
        return {'user_login': user_login, 'action': '{0}://{1}{2}'.format(*request.urlparts[:3])}

    def oauth2_finish_loop(self):
        user_login = request.forms.get('login')
        client_id = self._auth_request['client_id']
        access_token, _, refresh_token, _ = self._create_tokens(client_id, user_login)
        self._auth_request['access_token'] = access_token
        self._auth_request['refresh_token'] = refresh_token
        redirect_uri = self._auth_request['redirect_uri']
        code = self._auth_request['code']
        state = self._auth_request['state']
        self._db_session.commit()
        redirect('{0}?{1}'.format(redirect_uri, '&'.join(('code={0}'.format(code), 'state={0}'.format(state)))))

    def oauth2_token(self):
        """
        OAuth2 /token method.
        Either exchanges an auth code for an access/refresh token pair, or refreshes a token.
        """
        grant_type = request.forms.get('grant_type')
        client_id, client_secret = request.forms.get('client_id'), request.forms.get('client_secret')
        app = self._get_application_by_id(client_id)
        if client_secret != app.client_secret:
            abort(400, 'Invalid client secret: {0}'.format(client_secret))

        if grant_type == 'authorization_code':
            code = request.forms.get('code')
            if self._auth_request is None:
                abort(400, 'Invalid code: {0}'.format(code))
            access_token, refresh_token = self._auth_request['access_token'], self._auth_request['refresh_token']
        elif grant_type == 'refresh_token':
            refresh_token = request.forms.get('refresh_token')
            refresh_token_record = get_token_record_by_token(self._db_session, refresh_token)
            if refresh_token_record.token_type == 'refresh':
                if datetime.utcnow() > refresh_token_record.expires_at:
                    abort(400, 'Token expired: {0}'.format(refresh_token))
                access_token, _, refresh_token, _ = self._create_tokens(
                    client_id,
                    owned_by_id=refresh_token_record.owned_by_id,
                )
            else:
                abort(400, 'Invalid token: {0}'.format(refresh_token))
        else:
            abort(400, 'Invalid grant type: {0}'.format(grant_type))

        return json.dumps({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': self.ACCESS_TOKEN_DURATION_SECONDS,
        })

    def expire_token(self, token):
        token_record = get_token_record_by_token(self._db_session, token)
        token_record.expires_at = datetime.utcnow()
        self._db_session.commit()
