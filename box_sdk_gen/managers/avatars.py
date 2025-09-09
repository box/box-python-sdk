from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.user_avatar import UserAvatar

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.networking.fetch_options import MultipartItem

from box_sdk_gen.serialization.json import SerializedData


class AvatarsManager:
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

    def get_user_avatar(
        self, user_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ByteStream:
        """
                Retrieves an image of a the user's avatar.
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
                        '/avatar',
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.BINARY,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return response.content

    def create_user_avatar(
        self,
        user_id: str,
        pic: ByteStream,
        *,
        pic_file_name: Optional[str] = None,
        pic_content_type: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UserAvatar:
        """
                Adds or updates a user avatar.
                :param user_id: The ID of the user.
        Example: "12345"
                :type user_id: str
                :param pic: The image file to be uploaded to Box.
        Accepted file extensions are `.jpg` or `.png`.
        The maximum file size is 1MB.
                :type pic: ByteStream
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'pic': pic,
            'pic_file_name': pic_file_name,
            'pic_content_type': pic_content_type,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/users/',
                        to_string(user_id),
                        '/avatar',
                    ]
                ),
                method='POST',
                headers=headers_map,
                multipart_data=[
                    MultipartItem(
                        part_name='pic',
                        file_stream=pic,
                        file_name=pic_file_name,
                        content_type=pic_content_type,
                    )
                ],
                content_type='multipart/form-data',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, UserAvatar)

    def delete_user_avatar(
        self, user_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Removes an existing user avatar.

                You cannot reverse this operation.

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
                        '/avatar',
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
