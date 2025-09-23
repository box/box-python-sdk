from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.collaboration import Collaboration

from box_sdk_gen.managers.user_collaborations import CreateCollaborationItem

from box_sdk_gen.managers.user_collaborations import CreateCollaborationItemTypeField

from box_sdk_gen.managers.user_collaborations import CreateCollaborationAccessibleBy

from box_sdk_gen.managers.user_collaborations import (
    CreateCollaborationAccessibleByTypeField,
)

from box_sdk_gen.managers.user_collaborations import CreateCollaborationRole

from box_sdk_gen.schemas.v2025_r0.external_users_submit_delete_job_response_v2025_r0 import (
    ExternalUsersSubmitDeleteJobResponseV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.user_reference_v2025_r0 import UserReferenceV2025R0

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from test.box_sdk_gen.test.commons import upload_new_file

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))


def testSubmitJobToDeleteExternalUsers():
    file: FileFull = upload_new_file()
    file_collaboration: Collaboration = client.user_collaborations.create_collaboration(
        CreateCollaborationItem(type=CreateCollaborationItemTypeField.FILE, id=file.id),
        CreateCollaborationAccessibleBy(
            type=CreateCollaborationAccessibleByTypeField.USER,
            id=get_env_var('BOX_EXTERNAL_USER_ID'),
        ),
        CreateCollaborationRole.EDITOR,
    )
    external_users_job_delete_response: ExternalUsersSubmitDeleteJobResponseV2025R0 = (
        client.external_users.submit_job_to_delete_external_users_v2025_r0(
            [UserReferenceV2025R0(id=get_env_var('BOX_EXTERNAL_USER_ID'))]
        )
    )
    assert len(external_users_job_delete_response.entries) == 1
    assert external_users_job_delete_response.entries[0].status == 202
    client.files.delete_file_by_id(file.id)
