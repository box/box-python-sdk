from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.internal.null_value import NullValue

from typing import Union

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.items import Items

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


class GetFolderByIdSort(str, Enum):
    ID = 'id'
    NAME = 'name'
    DATE = 'date'
    SIZE = 'size'


class GetFolderByIdDirection(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class UpdateFolderByIdSyncState(str, Enum):
    SYNCED = 'synced'
    NOT_SYNCED = 'not_synced'
    PARTIALLY_SYNCED = 'partially_synced'


class UpdateFolderByIdParent(BaseObject):
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


class UpdateFolderByIdSharedLinkAccessField(str, Enum):
    OPEN = 'open'
    COMPANY = 'company'
    COLLABORATORS = 'collaborators'


class UpdateFolderByIdSharedLinkPermissionsField(BaseObject):
    def __init__(self, *, can_download: Optional[bool] = None, **kwargs):
        """
                :param can_download: If the shared link allows for downloading of files.
        This can only be set when `access` is set to
        `open` or `company`., defaults to None
                :type can_download: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.can_download = can_download


class UpdateFolderByIdSharedLink(BaseObject):
    def __init__(
        self,
        *,
        access: Optional[UpdateFolderByIdSharedLinkAccessField] = None,
        password: Optional[str] = None,
        vanity_name: Optional[str] = None,
        unshared_at: Optional[DateTime] = None,
        permissions: Optional[UpdateFolderByIdSharedLinkPermissionsField] = None,
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
                :type access: Optional[UpdateFolderByIdSharedLinkAccessField], optional
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
        as vanity URLs are a lot easier to guess than regular shared links., defaults to None
                :type vanity_name: Optional[str], optional
                :param unshared_at: The timestamp at which this shared link will
        expire. This field can only be set by
        users with paid accounts., defaults to None
                :type unshared_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.access = access
        self.password = password
        self.vanity_name = vanity_name
        self.unshared_at = unshared_at
        self.permissions = permissions


class UpdateFolderByIdFolderUploadEmailAccessField(str, Enum):
    OPEN = 'open'
    COLLABORATORS = 'collaborators'


class UpdateFolderByIdFolderUploadEmail(BaseObject):
    def __init__(
        self,
        *,
        access: Optional[UpdateFolderByIdFolderUploadEmailAccessField] = None,
        **kwargs
    ):
        """
                :param access: When this parameter has been set, users can email files
        to the email address that has been automatically
        created for this folder.

        To create an email address, set this property either when
        creating or updating the folder.

        When set to `collaborators`, only emails from registered email
        addresses for collaborators will be accepted. This includes
        any email aliases a user might have registered.

        When set to `open` it will accept emails from any email
        address., defaults to None
                :type access: Optional[UpdateFolderByIdFolderUploadEmailAccessField], optional
        """
        super().__init__(**kwargs)
        self.access = access


class UpdateFolderByIdCollections(BaseObject):
    def __init__(
        self, *, id: Optional[str] = None, type: Optional[str] = None, **kwargs
    ):
        """
        :param id: The unique identifier for this object., defaults to None
        :type id: Optional[str], optional
        :param type: The type for this object., defaults to None
        :type type: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class GetFolderItemsSort(str, Enum):
    ID = 'id'
    NAME = 'name'
    DATE = 'date'
    SIZE = 'size'


class GetFolderItemsDirection(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class CreateFolderParent(BaseObject):
    def __init__(self, id: str, **kwargs):
        """
        :param id: The ID of parent folder.
        :type id: str
        """
        super().__init__(**kwargs)
        self.id = id


class CreateFolderFolderUploadEmailAccessField(str, Enum):
    OPEN = 'open'
    COLLABORATORS = 'collaborators'


class CreateFolderFolderUploadEmail(BaseObject):
    def __init__(
        self,
        *,
        access: Optional[CreateFolderFolderUploadEmailAccessField] = None,
        **kwargs
    ):
        """
                :param access: When this parameter has been set, users can email files
        to the email address that has been automatically
        created for this folder.

        To create an email address, set this property either when
        creating or updating the folder.

        When set to `collaborators`, only emails from registered email
        addresses for collaborators will be accepted. This includes
        any email aliases a user might have registered.

        When set to `open` it will accept emails from any email
        address., defaults to None
                :type access: Optional[CreateFolderFolderUploadEmailAccessField], optional
        """
        super().__init__(**kwargs)
        self.access = access


class CreateFolderSyncState(str, Enum):
    SYNCED = 'synced'
    NOT_SYNCED = 'not_synced'
    PARTIALLY_SYNCED = 'partially_synced'


class CopyFolderParent(BaseObject):
    def __init__(self, id: str, **kwargs):
        """
        :param id: The ID of parent folder.
        :type id: str
        """
        super().__init__(**kwargs)
        self.id = id


class FoldersManager:
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

    def get_folder_by_id(
        self,
        folder_id: str,
        *,
        fields: Optional[List[str]] = None,
        sort: Optional[GetFolderByIdSort] = None,
        direction: Optional[GetFolderByIdDirection] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        if_none_match: Optional[str] = None,
        boxapi: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FolderFull:
        """
                Retrieves details for a folder, including the first 100 entries

                in the folder.


                Passing `sort`, `direction`, `offset`, and `limit`


                parameters in query allows you to manage the


                list of returned


                [folder items](r://folder--full#param-item-collection).


                To fetch more items within the folder, use the


                [Get items in a folder](e://get-folders-id-items) endpoint.

                :param folder_id: The unique identifier that represent a folder.

        The ID for any folder can be determined
        by visiting this folder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/folder/123`
        the `folder_id` is `123`.

        The root folder of a Box account is
        always represented by the ID `0`.
        Example: "12345"
                :type folder_id: str
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested.

        Additionally this field can be used to query any metadata
        applied to the file by specifying the `metadata` field as well
        as the scope and key of the template to retrieve, for example
        `?fields=metadata.enterprise_12345.contractTemplate`., defaults to None
                :type fields: Optional[List[str]], optional
                :param sort: Defines the **second** attribute by which items
        are sorted.

        The folder type affects the way the items
        are sorted:

          * **Standard folder**:
          Items are always sorted by
          their `type` first, with
          folders listed before files,
          and files listed
          before web links.

          * **Root folder**:
          This parameter is not supported
          for marker-based pagination
          on the root folder

          (the folder with an `id` of `0`).

          * **Shared folder with parent path
          to the associated folder visible to
          the collaborator**:
          Items are always sorted by
          their `type` first, with
          folders listed before files,
          and files listed
          before web links., defaults to None
                :type sort: Optional[GetFolderByIdSort], optional
                :param direction: The direction to sort results in. This can be either in alphabetical ascending
        (`ASC`) or descending (`DESC`) order., defaults to None
                :type direction: Optional[GetFolderByIdDirection], optional
                :param offset: The offset of the item at which to begin the response.

        Queries with offset parameter value
        exceeding 10000 will be rejected
        with a 400 response., defaults to None
                :type offset: Optional[int], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param if_none_match: Ensures an item is only returned if it has changed.

        Pass in the item's last observed `etag` value
        into this header and the endpoint will fail
        with a `304 Not Modified` if the item has not
        changed since., defaults to None
                :type if_none_match: Optional[str], optional
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
        query_params_map: Dict[str, str] = prepare_params(
            {
                'fields': to_string(fields),
                'sort': to_string(sort),
                'direction': to_string(direction),
                'offset': to_string(offset),
                'limit': to_string(limit),
            }
        )
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
                        '/2.0/folders/',
                        to_string(folder_id),
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
        return deserialize(response.data, FolderFull)

    def update_folder_by_id(
        self,
        folder_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        sync_state: Optional[UpdateFolderByIdSyncState] = None,
        can_non_owners_invite: Optional[bool] = None,
        parent: Optional[UpdateFolderByIdParent] = None,
        shared_link: Optional[UpdateFolderByIdSharedLink] = None,
        folder_upload_email: Union[
            Optional[UpdateFolderByIdFolderUploadEmail], NullValue
        ] = None,
        tags: Optional[List[str]] = None,
        is_collaboration_restricted_to_enterprise: Optional[bool] = None,
        collections: Union[
            Optional[List[UpdateFolderByIdCollections]], NullValue
        ] = None,
        can_non_owners_view_collaborators: Optional[bool] = None,
        fields: Optional[List[str]] = None,
        if_match: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FolderFull:
        r"""
                Updates a folder. This can be also be used to move the folder,

                create shared links, update collaborations, and more.

                :param folder_id: The unique identifier that represent a folder.

        The ID for any folder can be determined
        by visiting this folder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/folder/123`
        the `folder_id` is `123`.

        The root folder of a Box account is
        always represented by the ID `0`.
        Example: "12345"
                :type folder_id: str
                :param name: The optional new name for this folder.

        The following restrictions to folder names apply: names containing
        non-printable ASCII characters, forward and backward slashes
        (`/`, `\`), names with trailing spaces, and names `.` and `..` are
        not allowed.

        Folder names must be unique within their parent folder. The name check is case-insensitive,
        so a folder named `New Folder` cannot be created in a parent folder that already contains
        a folder named `new folder`., defaults to None
                :type name: Optional[str], optional
                :param description: The optional description of this folder., defaults to None
                :type description: Optional[str], optional
                :param sync_state: Specifies whether a folder should be synced to a
        user's device or not. This is used by Box Sync
        (discontinued) and is not used by Box Drive., defaults to None
                :type sync_state: Optional[UpdateFolderByIdSyncState], optional
                :param can_non_owners_invite: Specifies if users who are not the owner
        of the folder can invite new collaborators to the folder., defaults to None
                :type can_non_owners_invite: Optional[bool], optional
                :param tags: The tags for this item. These tags are shown in
        the Box web app and mobile apps next to an item.

        To add or remove a tag, retrieve the item's current tags,
        modify them, and then update this field.

        There is a limit of 100 tags per item, and 10,000
        unique tags per enterprise., defaults to None
                :type tags: Optional[List[str]], optional
                :param is_collaboration_restricted_to_enterprise: Specifies if new invites to this folder are restricted to users
        within the enterprise. This does not affect existing
        collaborations., defaults to None
                :type is_collaboration_restricted_to_enterprise: Optional[bool], optional
                :param collections: An array of collections to make this folder
        a member of. Currently
        we only support the `favorites` collection.

        To get the ID for a collection, use the
        [List all collections][1] endpoint.

        Passing an empty array `[]` or `null` will remove
        the folder from all collections.

        [1]: e://get-collections, defaults to None
                :type collections: Union[Optional[List[UpdateFolderByIdCollections]], NullValue], optional
                :param can_non_owners_view_collaborators: Restricts collaborators who are not the owner of
        this folder from viewing other collaborations on
        this folder.

        It also restricts non-owners from inviting new
        collaborators.

        When setting this field to `false`, it is required
        to also set `can_non_owners_invite_collaborators` to
        `false` if it has not already been set., defaults to None
                :type can_non_owners_view_collaborators: Optional[bool], optional
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param if_match: Ensures this item hasn't recently changed before
        making changes.

        Pass in the item's last observed `etag` value
        into this header and the endpoint will fail
        with a `412 Precondition Failed` if it
        has changed since., defaults to None
                :type if_match: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'name': name,
            'description': description,
            'sync_state': sync_state,
            'can_non_owners_invite': can_non_owners_invite,
            'parent': parent,
            'shared_link': shared_link,
            'folder_upload_email': folder_upload_email,
            'tags': tags,
            'is_collaboration_restricted_to_enterprise': (
                is_collaboration_restricted_to_enterprise
            ),
            'collections': collections,
            'can_non_owners_view_collaborators': can_non_owners_view_collaborators,
        }
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params(
            {'if-match': to_string(if_match), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/folders/',
                        to_string(folder_id),
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
        return deserialize(response.data, FolderFull)

    def delete_folder_by_id(
        self,
        folder_id: str,
        *,
        recursive: Optional[bool] = None,
        if_match: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a folder, either permanently or by moving it to

                the trash.

                :param folder_id: The unique identifier that represent a folder.

        The ID for any folder can be determined
        by visiting this folder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/folder/123`
        the `folder_id` is `123`.

        The root folder of a Box account is
        always represented by the ID `0`.
        Example: "12345"
                :type folder_id: str
                :param recursive: Delete a folder that is not empty by recursively deleting the
        folder and all of its content., defaults to None
                :type recursive: Optional[bool], optional
                :param if_match: Ensures this item hasn't recently changed before
        making changes.

        Pass in the item's last observed `etag` value
        into this header and the endpoint will fail
        with a `412 Precondition Failed` if it
        has changed since., defaults to None
                :type if_match: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'recursive': to_string(recursive)}
        )
        headers_map: Dict[str, str] = prepare_params(
            {'if-match': to_string(if_match), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/folders/',
                        to_string(folder_id),
                    ]
                ),
                method='DELETE',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def get_folder_items(
        self,
        folder_id: str,
        *,
        fields: Optional[List[str]] = None,
        usemarker: Optional[bool] = None,
        marker: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[GetFolderItemsSort] = None,
        direction: Optional[GetFolderItemsDirection] = None,
        boxapi: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Items:
        """
                Retrieves a page of items in a folder. These items can be files,

                folders, and web links.


                To request more information about the folder itself, like its size,


                use the [Get a folder](#get-folders-id) endpoint instead.

                :param folder_id: The unique identifier that represent a folder.

        The ID for any folder can be determined
        by visiting this folder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/folder/123`
        the `folder_id` is `123`.

        The root folder of a Box account is
        always represented by the ID `0`.
        Example: "12345"
                :type folder_id: str
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested.

        Additionally this field can be used to query any metadata
        applied to the file by specifying the `metadata` field as well
        as the scope and key of the template to retrieve, for example
        `?fields=metadata.enterprise_12345.contractTemplate`., defaults to None
                :type fields: Optional[List[str]], optional
                :param usemarker: Specifies whether to use marker-based pagination instead of
        offset-based pagination. Only one pagination method can
        be used at a time.

        By setting this value to true, the API will return a `marker` field
        that can be passed as a parameter to this endpoint to get the next
        page of the response., defaults to None
                :type usemarker: Optional[bool], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param offset: The offset of the item at which to begin the response.

        Queries with offset parameter value
        exceeding 10000 will be rejected
        with a 400 response., defaults to None
                :type offset: Optional[int], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param sort: Defines the **second** attribute by which items
        are sorted.

        The folder type affects the way the items
        are sorted:

          * **Standard folder**:
          Items are always sorted by
          their `type` first, with
          folders listed before files,
          and files listed
          before web links.

          * **Root folder**:
          This parameter is not supported
          for marker-based pagination
          on the root folder

          (the folder with an `id` of `0`).

          * **Shared folder with parent path
          to the associated folder visible to
          the collaborator**:
          Items are always sorted by
          their `type` first, with
          folders listed before files,
          and files listed
          before web links., defaults to None
                :type sort: Optional[GetFolderItemsSort], optional
                :param direction: The direction to sort results in. This can be either in alphabetical ascending
        (`ASC`) or descending (`DESC`) order., defaults to None
                :type direction: Optional[GetFolderItemsDirection], optional
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
        query_params_map: Dict[str, str] = prepare_params(
            {
                'fields': to_string(fields),
                'usemarker': to_string(usemarker),
                'marker': to_string(marker),
                'offset': to_string(offset),
                'limit': to_string(limit),
                'sort': to_string(sort),
                'direction': to_string(direction),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'boxapi': to_string(boxapi), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/folders/',
                        to_string(folder_id),
                        '/items',
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
        return deserialize(response.data, Items)

    def create_folder(
        self,
        name: str,
        parent: CreateFolderParent,
        *,
        folder_upload_email: Optional[CreateFolderFolderUploadEmail] = None,
        sync_state: Optional[CreateFolderSyncState] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FolderFull:
        r"""
                Creates a new empty folder within the specified parent folder.
                :param name: The name for the new folder.

        The following restrictions to folder names apply: names containing
        non-printable ASCII characters, forward and backward slashes
        (`/`, `\`), names with trailing spaces, and names `.` and `..` are
        not allowed.

        Folder names must be unique within their parent folder. The name check is case-insensitive,
        so a folder named `New Folder` cannot be created in a parent folder that already contains
        a folder named `new folder`.
                :type name: str
                :param parent: The parent folder to create the new folder within.
                :type parent: CreateFolderParent
                :param sync_state: Specifies whether a folder should be synced to a
        user's device or not. This is used by Box Sync
        (discontinued) and is not used by Box Drive., defaults to None
                :type sync_state: Optional[CreateFolderSyncState], optional
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'name': name,
            'parent': parent,
            'folder_upload_email': folder_upload_email,
            'sync_state': sync_state,
        }
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/folders']),
                method='POST',
                params=query_params_map,
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, FolderFull)

    def copy_folder(
        self,
        folder_id: str,
        parent: CopyFolderParent,
        *,
        name: Optional[str] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FolderFull:
        r"""
                Creates a copy of a folder within a destination folder.

                The original folder will not be changed.

                :param folder_id: The unique identifier of the folder to copy.

        The ID for any folder can be determined
        by visiting this folder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/folder/123`
        the `folder_id` is `123`.

        The root folder with the ID `0` can not be copied.
        Example: "0"
                :type folder_id: str
                :param parent: The destination folder to copy the folder to.
                :type parent: CopyFolderParent
                :param name: An optional new name for the copied folder.

        There are some restrictions to the file name. Names containing
        non-printable ASCII characters, forward and backward slashes
        (`/`, `\`), as well as names with trailing spaces are
        prohibited.

        Additionally, the names `.` and `..` are
        not allowed either., defaults to None
                :type name: Optional[str], optional
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'name': name, 'parent': parent}
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/folders/',
                        to_string(folder_id),
                        '/copy',
                    ]
                ),
                method='POST',
                params=query_params_map,
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, FolderFull)
