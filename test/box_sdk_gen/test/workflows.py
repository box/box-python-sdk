from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.workflows import Workflows

from box_sdk_gen.schemas.workflow import Workflow

from box_sdk_gen.managers.workflows import StartWorkflowType

from box_sdk_gen.managers.workflows import StartWorkflowFlow

from box_sdk_gen.managers.workflows import StartWorkflowFiles

from box_sdk_gen.managers.workflows import StartWorkflowFilesTypeField

from box_sdk_gen.managers.workflows import StartWorkflowFolder

from box_sdk_gen.managers.workflows import StartWorkflowFolderTypeField

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import generate_byte_stream

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

client: BoxClient = get_default_client()


def testWorkflows():
    admin_client: BoxClient = get_default_client_with_user_subject(
        get_env_var('USER_ID')
    )
    workflow_folder_id: str = get_env_var('WORKFLOW_FOLDER_ID')
    uploaded_files: Files = admin_client.uploads.upload_file(
        UploadFileAttributes(
            name=get_uuid(),
            parent=UploadFileAttributesParentField(id=workflow_folder_id),
        ),
        generate_byte_stream(1024 * 1024),
    )
    file: FileFull = uploaded_files.entries[0]
    workflow_file_id: str = file.id
    workflows: Workflows = admin_client.workflows.get_workflows(workflow_folder_id)
    assert len(workflows.entries) == 1
    workflow_to_run: Workflow = workflows.entries[0]
    assert to_string(workflow_to_run.type) == 'workflow'
    assert workflow_to_run.is_enabled == True
    assert to_string(workflow_to_run.flows[0].type) == 'flow'
    assert to_string(workflow_to_run.flows[0].trigger.type) == 'trigger'
    assert (
        to_string(workflow_to_run.flows[0].trigger.trigger_type)
        == 'WORKFLOW_MANUAL_START'
    )
    assert to_string(workflow_to_run.flows[0].outcomes[0].action_type) == 'delete_file'
    assert to_string(workflow_to_run.flows[0].outcomes[0].type) == 'outcome'
    admin_client.workflows.start_workflow(
        workflow_to_run.id,
        StartWorkflowFlow(type='flow', id=workflow_to_run.flows[0].id),
        [
            StartWorkflowFiles(
                type=StartWorkflowFilesTypeField.FILE, id=workflow_file_id
            )
        ],
        StartWorkflowFolder(
            type=StartWorkflowFolderTypeField.FOLDER, id=workflow_folder_id
        ),
        type=StartWorkflowType.WORKFLOW_PARAMETERS,
    )
