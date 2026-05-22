from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.schemas.access_token import AccessToken

from box_sdk_gen.schemas.v2026_r0.notes_convert_response_v2026_r0 import (
    NotesConvertResponseV2026R0,
)

from box_sdk_gen.managers.notes import CreateNoteConvertV2026R0ContentFormat

from box_sdk_gen.schemas.v2026_r0.folder_reference_v2026_r0 import (
    FolderReferenceV2026R0,
)

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.client import BoxClient

from box_sdk_gen.box.developer_token_auth import BoxDeveloperTokenAuth

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))


def testConvertMarkdownToBoxNote():
    note_name: str = get_uuid()
    markdown_content: str = r"""# Heading

Some text"""
    downscoped_token: AccessToken = client.auth.downscope_token(['item_upload'])
    downscoped_client: BoxClient = BoxClient(
        auth=BoxDeveloperTokenAuth(token=downscoped_token.access_token)
    )
    response: NotesConvertResponseV2026R0 = (
        downscoped_client.notes.create_note_convert_v2026_r0(
            markdown_content,
            FolderReferenceV2026R0(id='0'),
            note_name,
            content_format=CreateNoteConvertV2026R0ContentFormat.MARKDOWN,
        )
    )
    assert not response.id == ''
    assert to_string(response.type) == 'file'
    file: FileFull = client.files.get_file_by_id(response.id)
    assert file.name == ''.join([note_name, '.boxnote'])
    assert file.parent.id == '0'
    client.files.delete_file_by_id(response.id)
