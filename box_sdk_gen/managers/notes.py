from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.schemas.v2026_r0.folder_reference_v2026_r0 import (
    FolderReferenceV2026R0,
)

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2026_r0.notes_convert_response_v2026_r0 import (
    NotesConvertResponseV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.client_error_v2026_r0 import ClientErrorV2026R0

from box_sdk_gen.parameters.v2026_r0.box_version_header_v2026_r0 import (
    BoxVersionHeaderV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.notes_convert_request_body_v2026_r0 import (
    NotesConvertRequestBodyV2026R0,
)

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


class CreateNoteConvertV2026R0ContentFormat(str, Enum):
    MARKDOWN = 'markdown'


class NotesManager:
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

    def create_note_convert_v2026_r0(
        self,
        content: str,
        parent: FolderReferenceV2026R0,
        name: str,
        *,
        content_format: CreateNoteConvertV2026R0ContentFormat = CreateNoteConvertV2026R0ContentFormat.MARKDOWN,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> NotesConvertResponseV2026R0:
        """
        Creates a Box Note (`.boxnote` file) from supported source content. See the `content_format` field for supported formats.
        :param content: The content to convert to a note. See the `content_format` field for supported formats.
        :type content: str
        :param name: The name for the created note. The `.boxnote` extension is appended automatically.
        :type name: str
        :param content_format: Format of the content to convert., defaults to CreateNoteConvertV2026R0ContentFormat.MARKDOWN
        :type content_format: CreateNoteConvertV2026R0ContentFormat, optional
        :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
        :type box_version: BoxVersionHeaderV2026R0, optional
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'content': content,
            'content_format': content_format,
            'parent': parent,
            'name': name,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/notes/convert']
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
        return deserialize(response.data, NotesConvertResponseV2026R0)
