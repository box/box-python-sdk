from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.internal.null_value import NullValue

from typing import Union

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

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.internal.utils import DateTime


class AddShareLinkToWebLinkSharedLinkAccessField(str, Enum):
    OPEN = 'open'
    COMPANY = 'company'
    COLLABORATORS = 'collaborators'


class AddShareLinkToWebLinkSharedLinkPermissionsField(BaseObject):
    def __init__(
        self,
        *,
        can_download: Optional[bool] = None,
        can_preview: Optional[bool] = None,
        can_edit: Optional[bool] = None,
        **kwargs
    ):
        """
                :param can_download: If the shared link allows for downloading of files.
        This can only be set when `access` is set to
        `open` or `company`., defaults to None
                :type can_download: Optional[bool], optional
                :param can_preview: If the shared link allows for previewing of files.
        This value is always `true`. For shared links on folders
        this also applies to any items in the folder., defaults to None
                :type can_preview: Optional[bool], optional
                :param can_edit: This value can only be `true` is `type` is `file`., defaults to None
                :type can_edit: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.can_download = can_download
        self.can_preview = can_preview
        self.can_edit = can_edit


class AddShareLinkToWebLinkSharedLink(BaseObject):
    def __init__(
        self,
        *,
        access: Optional[AddShareLinkToWebLinkSharedLinkAccessField] = None,
        password: Optional[str] = None,
        vanity_name: Optional[str] = None,
        unshared_at: Optional[DateTime] = None,
        permissions: Optional[AddShareLinkToWebLinkSharedLinkPermissionsField] = None,
        **kwargs
    ):
        """
                :param access: The level of access for the shared link. This can be
        restricted to anyone with the link (`open`), only people
        within the company (`company`) and only those who
        have been invited to the file (`collaborators`).

        If not set, this field defaults to the access level specified
        by the enterprise admin. To create a shared link with this
        default setting pass the `shared_link` object with
        no `access` field, for example `{ "shared_link": {} }`.

        The `company` access level is only available to paid
        accounts., defaults to None
                :type access: Optional[AddShareLinkToWebLinkSharedLinkAccessField], optional
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
        self.permissions = permissions


class UpdateSharedLinkOnWebLinkSharedLinkAccessField(str, Enum):
    OPEN = 'open'
    COMPANY = 'company'
    COLLABORATORS = 'collaborators'


class UpdateSharedLinkOnWebLinkSharedLinkPermissionsField(BaseObject):
    def __init__(
        self,
        *,
        can_download: Optional[bool] = None,
        can_preview: Optional[bool] = None,
        can_edit: Optional[bool] = None,
        **kwargs
    ):
        """
                :param can_download: If the shared link allows for downloading of files.
        This can only be set when `access` is set to
        `open` or `company`., defaults to None
                :type can_download: Optional[bool], optional
                :param can_preview: If the shared link allows for previewing of files.
        This value is always `true`. For shared links on folders
        this also applies to any items in the folder., defaults to None
                :type can_preview: Optional[bool], optional
                :param can_edit: This value can only be `true` is `type` is `file`., defaults to None
                :type can_edit: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.can_download = can_download
        self.can_preview = can_preview
        self.can_edit = can_edit


class UpdateSharedLinkOnWebLinkSharedLink(BaseObject):
    def __init__(
        self,
        *,
        access: Optional[UpdateSharedLinkOnWebLinkSharedLinkAccessField] = None,
        password: Optional[str] = None,
        vanity_name: Optional[str] = None,
        unshared_at: Optional[DateTime] = None,
        permissions: Optional[
            UpdateSharedLinkOnWebLinkSharedLinkPermissionsField
        ] = None,
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
                :type access: Optional[UpdateSharedLinkOnWebLinkSharedLinkAccessField], optional
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
        self.permissions = permissions


class RemoveSharedLinkFromWebLinkSharedLink(BaseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SharedLinksWebLinksManager:
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

    def find_web_link_for_shared_link(
        self,
        boxapi: str,
        *,
        fields: Optional[List[str]] = None,
        if_none_match: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> WebLink:
        """
                Returns the web link represented by a shared link.

                A shared web link can be represented by a shared link,


                which can originate within the current enterprise or within another.


                This endpoint allows an application to retrieve information about a


                shared web link when only given a shared link.

                :param boxapi: A header containing the shared link and optional password for the
        shared link.

        The format for this header is as follows:

        `shared_link=[link]&shared_link_password=[password]`.
                :type boxapi: str
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param if_none_match: Ensures an item is only returned if it has changed.

        Pass in the item's last observed `etag` value
        into this header and the endpoint will fail
        with a `304 Not Modified` if the item has not
        changed since., defaults to None
                :type if_none_match: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params(
            {
                'if-none-match': to_string(if_none_match),
                'boxapi': to_string(boxapi),
                **extra_headers,
            }
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shared_items#web_links',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, WebLink)

    def get_shared_link_for_web_link(
        self,
        web_link_id: str,
        fields: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> WebLink:
        """
                Gets the information for a shared link on a web link.
                :param web_link_id: The ID of the web link.
        Example: "12345"
                :type web_link_id: str
                :param fields: Explicitly request the `shared_link` fields
        to be returned for this item.
                :type fields: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/web_links/',
                        to_string(web_link_id),
                        '#get_shared_link',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, WebLink)

    def add_share_link_to_web_link(
        self,
        web_link_id: str,
        fields: str,
        *,
        shared_link: Optional[AddShareLinkToWebLinkSharedLink] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> WebLink:
        """
                Adds a shared link to a web link.
                :param web_link_id: The ID of the web link.
        Example: "12345"
                :type web_link_id: str
                :param fields: Explicitly request the `shared_link` fields
        to be returned for this item.
                :type fields: str
                :param shared_link: The settings for the shared link to create on the web link.

        Use an empty object (`{}`) to use the default settings for shared
        links., defaults to None
                :type shared_link: Optional[AddShareLinkToWebLinkSharedLink], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'shared_link': shared_link}
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/web_links/',
                        to_string(web_link_id),
                        '#add_shared_link',
                    ]
                ),
                method='PUT',
                params=query_params_map,
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, WebLink)

    def update_shared_link_on_web_link(
        self,
        web_link_id: str,
        fields: str,
        *,
        shared_link: Optional[UpdateSharedLinkOnWebLinkSharedLink] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> WebLink:
        """
                Updates a shared link on a web link.
                :param web_link_id: The ID of the web link.
        Example: "12345"
                :type web_link_id: str
                :param fields: Explicitly request the `shared_link` fields
        to be returned for this item.
                :type fields: str
                :param shared_link: The settings for the shared link to update., defaults to None
                :type shared_link: Optional[UpdateSharedLinkOnWebLinkSharedLink], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'shared_link': shared_link}
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/web_links/',
                        to_string(web_link_id),
                        '#update_shared_link',
                    ]
                ),
                method='PUT',
                params=query_params_map,
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, WebLink)

    def remove_shared_link_from_web_link(
        self,
        web_link_id: str,
        fields: str,
        *,
        shared_link: Union[
            Optional[RemoveSharedLinkFromWebLinkSharedLink], NullValue
        ] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> WebLink:
        """
                Removes a shared link from a web link.
                :param web_link_id: The ID of the web link.
        Example: "12345"
                :type web_link_id: str
                :param fields: Explicitly request the `shared_link` fields
        to be returned for this item.
                :type fields: str
                :param shared_link: By setting this value to `null`, the shared link
        is removed from the web link., defaults to None
                :type shared_link: Union[Optional[RemoveSharedLinkFromWebLinkSharedLink], NullValue], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'shared_link': shared_link}
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/web_links/',
                        to_string(web_link_id),
                        '#remove_shared_link',
                    ]
                ),
                method='PUT',
                params=query_params_map,
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, WebLink)
