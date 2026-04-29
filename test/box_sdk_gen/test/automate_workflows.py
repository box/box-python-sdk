from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.v2026_r0.automate_workflows_v2026_r0 import (
    AutomateWorkflowsV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.automate_workflow_action_v2026_r0 import (
    AutomateWorkflowActionV2026R0,
)

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import generate_byte_stream

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

client: BoxClient = get_default_client()


def testAutomateWorkflows():
    admin_client: BoxClient = get_default_client_with_user_subject(
        get_env_var('USER_ID')
    )
    workflow_folder_id: str = get_env_var('AUTOMATE_WORKFLOW_FOLDER_ID')
    uploaded_files: Files = admin_client.uploads.upload_file(
        UploadFileAttributes(
            name=get_uuid(),
            parent=UploadFileAttributesParentField(id=workflow_folder_id),
        ),
        generate_byte_stream(1024 * 1024),
    )
    file: FileFull = uploaded_files.entries[0]
    workflow_file_id: str = file.id
    automate_workflows: AutomateWorkflowsV2026R0 = (
        admin_client.automate_workflows.get_automate_workflows_v2026_r0(
            workflow_folder_id
        )
    )
    assert len(automate_workflows.entries) == 1
    workflow_action: AutomateWorkflowActionV2026R0 = automate_workflows.entries[0]
    assert to_string(workflow_action.type) == 'workflow_action'
    assert to_string(workflow_action.action_type) == 'run_workflow'
    assert to_string(workflow_action.workflow.type) == 'workflow'
    admin_client.automate_workflows.create_automate_workflow_start_v2026_r0(
        workflow_action.workflow.id, workflow_action.id, [workflow_file_id]
    )
