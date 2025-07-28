from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.email_aliases import EmailAliases

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.email_alias import EmailAlias

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData


class EmailAliasesManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_user_email_aliases(
        self, user_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> EmailAliases:
        """
                Retrieves all email aliases for a user. The collection

                does not include the primary login for the user.

                :param user_id: The ID of the user.
        Example: "12345"
                :type user_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/users/',
                        to_string(user_id),
                        '/email_aliases',
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, EmailAliases)

    def create_user_email_alias(
        self,
        user_id: str,
        email: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> EmailAlias:
        """
                Adds a new email alias to a user account..
                :param user_id: The ID of the user.
        Example: "12345"
                :type user_id: str
                :param email: The email address to add to the account as an alias.

        Note: The domain of the email alias needs to be registered
         to your enterprise.
        See the [domain verification guide](
          https://support.box.com/hc/en-us/articles/4408619650579-Domain-Verification
          ) for steps to add a new domain.
                :type email: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'email': email}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/users/',
                        to_string(user_id),
                        '/email_aliases',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, EmailAlias)

    def delete_user_email_alias_by_id(
        self,
        user_id: str,
        email_alias_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Removes an email alias from a user.
                :param user_id: The ID of the user.
        Example: "12345"
                :type user_id: str
                :param email_alias_id: The ID of the email alias.
        Example: "23432"
                :type email_alias_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/users/',
                        to_string(user_id),
                        '/email_aliases/',
                        to_string(email_alias_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None
