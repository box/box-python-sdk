from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.trash_folder_restored import TrashFolderRestored

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.trash_folder import TrashFolder

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


class RestoreFolderFromTrashParent(BaseObject):
    def __init__(self, *, id: Optional[str] = None, **kwargs):
        """
        :param id: The ID of parent item., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id


class TrashedFoldersManager:
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

    def restore_folder_from_trash(
        self,
        folder_id: str,
        *,
        name: Optional[str] = None,
        parent: Optional[RestoreFolderFromTrashParent] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TrashFolderRestored:
        """
                Restores a folder that has been moved to the trash.

                An optional new parent ID can be provided to restore the folder to in case the


                original folder has been deleted.


                During this operation, part of the file tree will be locked, mainly


                the source folder and all of its descendants, as well as the destination


                folder.


                For the duration of the operation, no other move, copy, delete, or restore


                operation can performed on any of the locked folders.

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
                :param name: An optional new name for the folder., defaults to None
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
        return deserialize(response.data, TrashFolderRestored)

    def get_trashed_folder_by_id(
        self,
        folder_id: str,
        *,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TrashFolder:
        """
                Retrieves a folder that has been moved to the trash.

                Please note that only if the folder itself has been moved to the


                trash can it be retrieved with this API call. If instead one of


                its parent folders was moved to the trash, only that folder


                can be inspected using the


                [`GET /folders/:id/trash`](e://get_folders_id_trash) API.


                To list all items that have been moved to the trash, please


                use the [`GET /folders/trash/items`](e://get-folders-trash-items/)


                API.

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
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
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
                        '/2.0/folders/',
                        to_string(folder_id),
                        '/trash',
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
        return deserialize(response.data, TrashFolder)

    def delete_trashed_folder_by_id(
        self,
        folder_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Permanently deletes a folder that is in the trash.

                This action cannot be undone.

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
                        '/2.0/folders/',
                        to_string(folder_id),
                        '/trash',
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
