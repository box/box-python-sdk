from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from enum import Enum

from typing import Dict

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.internal.utils import DateTime


class CreateWebLinkParent(BaseObject):
    def __init__(self, id: str, **kwargs):
        """
        :param id: The ID of parent folder.
        :type id: str
        """
        super().__init__(**kwargs)
        self.id = id


class UpdateWebLinkByIdParent(BaseObject):
    def __init__(
        self, *, id: Optional[str] = None, user_id: Optional[str] = None, **kwargs
    ):
        """
        :param id: The ID of parent item., defaults to None
        :type id: Optional[str], optional
        :param user_id: The input for `user_id` is optional. Moving to non-root folder is not allowed when `user_id` is present. Parent folder id should be zero when `user_id` is provided., defaults to None
        :type user_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.user_id = user_id


class UpdateWebLinkByIdSharedLinkAccessField(str, Enum):
    OPEN = 'open'
    COMPANY = 'company'
    COLLABORATORS = 'collaborators'


class UpdateWebLinkByIdSharedLink(BaseObject):
    def __init__(
        self,
        *,
        access: Optional[UpdateWebLinkByIdSharedLinkAccessField] = None,
        password: Optional[str] = None,
        vanity_name: Optional[str] = None,
        unshared_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
                :param access: The level of access for the shared link. This can be
        restricted to anyone with the link (`open`), only people
        within the company (`company`) and only those who
        have been invited to the folder (`collaborators`).

        If not set, this field defaults to the access level specified
        by the enterprise admin. To create a shared link with this
        default setting pass the `shared_link` object with
        no `access` field, for example `{ "shared_link": {} }`.

        The `company` access level is only available to paid
        accounts., defaults to None
                :type access: Optional[UpdateWebLinkByIdSharedLinkAccessField], optional
                :param password: The password required to access the shared link. Set the
        password to `null` to remove it.
        Passwords must now be at least eight characters
        long and include a number, upper case letter, or
        a non-numeric or non-alphabetic character.
        A password can only be set when `access` is set to `open`., defaults to None
                :type password: Optional[str], optional
                :param vanity_name: Defines a custom vanity name to use in the shared link URL,
        for example `https://app.box.com/v/my-shared-link`.

        Custom URLs should not be used when sharing sensitive content
        as vanity URLs are a lot easier to guess than regular shared
        links., defaults to None
                :type vanity_name: Optional[str], optional
                :param unshared_at: The timestamp at which this shared link will
        expire. This field can only be set by
        users with paid accounts. The value must be greater than the
        current date and time., defaults to None
                :type unshared_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.access = access
        self.password = password
        self.vanity_name = vanity_name
        self.unshared_at = unshared_at


class WebLinksManager:
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

    def create_web_link(
        self,
        url: str,
        parent: CreateWebLinkParent,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> WebLink:
        """
                Creates a web link object within a folder.
                :param url: The URL that this web link links to. Must start with
        `"http://"` or `"https://"`.
                :type url: str
                :param parent: The parent folder to create the web link within.
                :type parent: CreateWebLinkParent
                :param name: Name of the web link. Defaults to the URL if not set., defaults to None
                :type name: Optional[str], optional
                :param description: Description of the web link., defaults to None
                :type description: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'url': url,
            'parent': parent,
            'name': name,
            'description': description,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/web_links']
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
        return deserialize(response.data, WebLink)

    def get_web_link_by_id(
        self,
        web_link_id: str,
        *,
        boxapi: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> WebLink:
        """
                Retrieve information about a web link.
                :param web_link_id: The ID of the web link.
        Example: "12345"
                :type web_link_id: str
                :param boxapi: The URL, and optional password, for the shared link of this item.

        This header can be used to access items that have not been
        explicitly shared with a user.

        Use the format `shared_link=[link]` or if a password is required then
        use `shared_link=[link]&shared_link_password=[password]`.

        This header can be used on the file or folder shared, as well as on any files
        or folders nested within the item., defaults to None
                :type boxapi: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'boxapi': to_string(boxapi), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/web_links/',
                        to_string(web_link_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, WebLink)

    def update_web_link_by_id(
        self,
        web_link_id: str,
        *,
        url: Optional[str] = None,
        parent: Optional[UpdateWebLinkByIdParent] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        shared_link: Optional[UpdateWebLinkByIdSharedLink] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> WebLink:
        """
                Updates a web link object.
                :param web_link_id: The ID of the web link.
        Example: "12345"
                :type web_link_id: str
                :param url: The new URL that the web link links to. Must start with
        `"http://"` or `"https://"`., defaults to None
                :type url: Optional[str], optional
                :param name: A new name for the web link. Defaults to the URL if not set., defaults to None
                :type name: Optional[str], optional
                :param description: A new description of the web link., defaults to None
                :type description: Optional[str], optional
                :param shared_link: The settings for the shared link to update., defaults to None
                :type shared_link: Optional[UpdateWebLinkByIdSharedLink], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'url': url,
            'parent': parent,
            'name': name,
            'description': description,
            'shared_link': shared_link,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/web_links/',
                        to_string(web_link_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, WebLink)

    def delete_web_link_by_id(
        self,
        web_link_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a web link.
                :param web_link_id: The ID of the web link.
        Example: "12345"
                :type web_link_id: str
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
                        '/2.0/web_links/',
                        to_string(web_link_id),
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
