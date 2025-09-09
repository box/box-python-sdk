from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.folder_full import FolderFull

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


class TransferOwnedFolderOwnedBy(BaseObject):
    def __init__(self, id: str, **kwargs):
        """
                :param id: The ID of the user who the folder will be
        transferred to.
                :type id: str
        """
        super().__init__(**kwargs)
        self.id = id


class TransferManager:
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

    def transfer_owned_folder(
        self,
        user_id: str,
        owned_by: TransferOwnedFolderOwnedBy,
        *,
        fields: Optional[List[str]] = None,
        notify: Optional[bool] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FolderFull:
        """
                Move all of the items (files, folders and workflows) owned by a user into

                another user's account


                Only the root folder (`0`) can be transferred.


                Folders can only be moved across users by users with administrative


                permissions.


                All existing shared links and folder-level collaborations are transferred


                during the operation. Please note that while collaborations at the individual


                file-level are transferred during the operation, the collaborations are


                deleted when the original user is deleted.


                If the user has a large number of items across all folders, the call will


                be run asynchronously. If the operation is not completed within 10 minutes,


                the user will receive a 200 OK response, and the operation will continue running.


                If the destination path has a metadata cascade policy attached to any of


                the parent folders, a metadata cascade operation will be kicked off


                asynchronously.


                There is currently no way to check for when this operation is finished.


                The destination folder's name will be in the format `{User}'s Files and


                Folders`, where `{User}` is the display name of the user.


                To make this API call your application will need to have the "Read and write


                all files and folders stored in Box" scope enabled.


                Please make sure the destination user has access to `Relay` or `Relay Lite`,


                and has access to the files and folders involved in the workflows being


                transferred.


                Admins will receive an email when the operation is completed.

                :param user_id: The ID of the user.
        Example: "12345"
                :type user_id: str
                :param owned_by: The user who the folder will be transferred to.
                :type owned_by: TransferOwnedFolderOwnedBy
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param notify: Determines if users should receive email notification
        for the action performed., defaults to None
                :type notify: Optional[bool], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'owned_by': owned_by}
        query_params_map: Dict[str, str] = prepare_params(
            {'fields': to_string(fields), 'notify': to_string(notify)}
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/users/',
                        to_string(user_id),
                        '/folders/0',
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
