
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Tuple, TYPE_CHECKING, Union, Any

from boxsdk.auth.oauth2 import OAuth2
from boxsdk.exception import BoxOAuthException
from boxsdk.config import API
from boxsdk.object.user import User

if TYPE_CHECKING:
    from boxsdk.network.network_interface import NetworkResponse


class ServerAuth(ABC, OAuth2):
    USER_SUBJECT_TYPE = 'user'
    ENTERPRISE_SUBJECT_TYPE = 'enterprise'

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            enterprise_id: Optional[str] = None,
            user: Optional[Union[str, 'User']] = None,
            **kwargs: Any
    ):
        super().__init__(client_id=client_id, client_secret=client_secret, **kwargs)
        self._enterprise_id = enterprise_id
        self._user_id = self._normalize_user_id(user)

    def _refresh(self, access_token: str) -> Tuple[str, None]:
        """
        Base class override.

        Instead of refreshing an access token using a refresh token, we just issue a new JWT request.
        """
        # pylint:disable=unused-argument
        if self._user_id is None:
            new_access_token = self.authenticate_instance()
        else:
            new_access_token = self.authenticate_user()
        return new_access_token, None

    def authenticate_user(self, user: Union[str, 'User'] = None) -> str:
        """
        Get an access token for a User.

        May be one of this application's created App User. Depending on the
        configured User Access Level, may also be any other App User or Managed
        User in the enterprise.

        <https://developer.box.com/en/guides/applications/>
        <https://developer.box.com/en/guides/authentication/select/>

        :param user:
            (optional) The user to authenticate, expressed as a Box User ID or
            as a :class:`User` instance.

            If not given, then the most recently provided user ID, if
            available, will be used.
        :raises:
            :exc:`ValueError` if no user ID was passed and the object is not
            currently configured with one.
        :return:
            The access token for the user.
        """
        sub = self._normalize_user_id(user) or self._user_id
        if not sub:
            raise ValueError("authenticate_user: Requires the user ID, but it was not provided.")
        self._user_id = sub
        return self._authenticate(sub, self.USER_SUBJECT_TYPE)

    authenticate_app_user = authenticate_user

    def authenticate_instance(self, enterprise: Optional[str] = None) -> str:
        """
        Get an access token for a Box Developer Edition enterprise.

        :param enterprise:
            The ID of the Box Developer Edition enterprise.

            Optional if the value was already given to `__init__`,
            otherwise required.
        :raises:
            :exc:`ValueError` if `None` was passed for the enterprise ID here
            and in `__init__`, or if the non-`None` value passed here does not
            match the non-`None` value passed to `__init__`.
        :return:
            The access token for the enterprise which can provision/deprovision app users.
        """
        enterprises = [enterprise, self._enterprise_id]
        if not any(enterprises):
            raise ValueError("authenticate_instance: Requires the enterprise ID, but it was not provided.")
        if all(enterprises) and (enterprise != self._enterprise_id):
            raise ValueError(
                f"authenticate_instance: Given enterprise ID {enterprise!r}, "
                f"but {self} already has ID {self._enterprise_id!r}"
            )
        if not self._enterprise_id:
            self._enterprise_id = enterprise
        self._user_id = None
        return self._authenticate(self._enterprise_id, self.ENTERPRISE_SUBJECT_TYPE)

    def _authenticate(self, subject_id: str, subject_type: str) -> str:
        """
        Authenticate with server type authentication (JWT or CCG).
        If authorization fails because the expiration time is out of sync with the Box servers,
        retry using the time returned in the error response.
        Pass an enterprise ID to get an enterprise token (which can be used to provision/deprovision users),
        or a user ID to get a user token.

        :param subject_id:
            The enterprise ID or user ID to auth.
        :param subject_type:
            Either 'enterprise' or 'user'
        :return:
            The access token for the enterprise or app user.
        """
        attempt_number = 0
        date = None
        while True:
            try:
                return self._fetch_access_token(subject_id, subject_type, date)
            except BoxOAuthException as ex:
                network_response = ex.network_response
                code = network_response.status_code  # pylint: disable=maybe-no-member
                box_datetime = self._get_date_header(network_response)

                if attempt_number >= API.MAX_RETRY_ATTEMPTS:
                    raise ex

                if code == 429 or code >= 500:
                    date = None
                elif box_datetime is not None and self._was_exp_claim_rejected_due_to_clock_skew(network_response):
                    date = box_datetime
                else:
                    raise ex

                time_delay = self._session.get_retry_after_time(
                    attempt_number,
                    network_response.headers.get('Retry-After', None)
                )
                time.sleep(time_delay)
                attempt_number += 1
                self._logger.debug('Retrying authentication request')

    @abstractmethod
    def _fetch_access_token(self, subject_id: str, subject_type: str, now_time: Optional[datetime] = None) -> str:
        pass

    @staticmethod
    def _get_date_header(network_response: 'NetworkResponse') -> Optional[datetime]:
        """
        Get datetime object for Date header, if the Date header is available.

        :param network_response:
            The response from the Box API that should include a Date header.
        :return:
            The datetime parsed from the Date header, or None if the header is absent or if it couldn't be parsed.
        """
        box_date_header = network_response.headers.get('Date', None)
        if box_date_header is not None:
            try:
                return datetime.strptime(box_date_header, '%a, %d %b %Y %H:%M:%S %Z')
            except ValueError:
                pass
        return None

    @staticmethod
    def _was_exp_claim_rejected_due_to_clock_skew(network_response: 'NetworkResponse') -> bool:
        """
        Determine whether the network response indicates that the authorization request was rejected because of
        the exp claim. This can happen if the current system time is too different from the Box server time.

        Returns True if the status code is 400, the error code is invalid_grant, and the error description indicates
        a problem with the exp claim; False, otherwise.

        :param network_response:
            The response from the Box API that should include a Date header.
        """
        status_code = network_response.status_code
        try:
            json_response = network_response.json()
        except ValueError:
            return False
        error_code = json_response.get('error', '')
        error_description = json_response.get('error_description', '')
        return status_code == 400 and error_code == 'invalid_grant' and 'exp' in error_description

    @classmethod
    def _normalize_user_id(cls, user: Any) -> Optional[str]:
        """Get a Box user ID from a selection of supported param types.

        :param user:
            An object representing the user or user ID.

            Currently supported types are `unicode` (which represents the user
            ID) and :class:`User`.

            If `None`, returns `None`.
        :raises:  :exc:`TypeError` for unsupported types.
        """
        if user is None:
            return None
        if isinstance(user, User):
            return user.object_id
        if isinstance(user, str):
            return str(user)
        raise TypeError(f"Got unsupported type {user.__class__.__name__!r} for user.")
