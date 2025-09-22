from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.schemas.retention_policy import RetentionPolicy

from box_sdk_gen.managers.retention_policies import CreateRetentionPolicyPolicyType

from box_sdk_gen.managers.retention_policies import (
    CreateRetentionPolicyDispositionAction,
)

from box_sdk_gen.managers.retention_policies import CreateRetentionPolicyRetentionType

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.retention_policy_assignment import RetentionPolicyAssignment

from box_sdk_gen.managers.retention_policy_assignments import (
    CreateRetentionPolicyAssignmentAssignTo,
)

from box_sdk_gen.managers.retention_policy_assignments import (
    CreateRetentionPolicyAssignmentAssignToTypeField,
)

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.managers.uploads import UploadFileVersionAttributes

from box_sdk_gen.schemas.file_version_retentions import FileVersionRetentions

from box_sdk_gen.schemas.file_version_retention import FileVersionRetention

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.client import BoxClient

from test.box_sdk_gen.test.commons import create_new_folder

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testCreateUpdateGetDeleteRetentionPolicy():
    description: str = get_uuid()
    retention_policy: RetentionPolicy = (
        client.retention_policies.create_retention_policy(
            get_uuid(),
            CreateRetentionPolicyPolicyType.FINITE,
            CreateRetentionPolicyDispositionAction.REMOVE_RETENTION,
            description=description,
            retention_length='1',
            retention_type=CreateRetentionPolicyRetentionType.MODIFIABLE,
            can_owner_extend_retention=False,
        )
    )
    assert retention_policy.description == description
    assert retention_policy.can_owner_extend_retention == False
    assert to_string(retention_policy.retention_type) == 'modifiable'
    folder: FolderFull = create_new_folder()
    retention_policy_assignment: RetentionPolicyAssignment = (
        client.retention_policy_assignments.create_retention_policy_assignment(
            retention_policy.id,
            CreateRetentionPolicyAssignmentAssignTo(
                id=folder.id,
                type=CreateRetentionPolicyAssignmentAssignToTypeField.FOLDER,
            ),
        )
    )
    assert retention_policy_assignment.retention_policy.id == retention_policy.id
    assert retention_policy_assignment.assigned_to.id == folder.id
    assert to_string(retention_policy_assignment.assigned_to.type) == to_string(
        folder.type
    )
    files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=get_uuid(), parent=UploadFileAttributesParentField(id=folder.id)
        ),
        generate_byte_stream(10),
    )
    file: FileFull = files.entries[0]
    new_files: Files = client.uploads.upload_file_version(
        file.id, UploadFileVersionAttributes(name=file.name), generate_byte_stream(20)
    )
    new_file: FileFull = new_files.entries[0]
    assert new_file.id == file.id
    file_version_retentions: FileVersionRetentions = (
        client.file_version_retentions.get_file_version_retentions()
    )
    file_version_retentions_count: int = len(file_version_retentions.entries)
    assert file_version_retentions_count >= 0
    if file_version_retentions_count == 0:
        client.retention_policies.delete_retention_policy_by_id(retention_policy.id)
        client.folders.delete_folder_by_id(folder.id, recursive=True)
        return None
    file_version_retention: FileVersionRetention = file_version_retentions.entries[0]
    file_version_retention_by_id: FileVersionRetention = (
        client.file_version_retentions.get_file_version_retention_by_id(
            file_version_retention.id
        )
    )
    assert file_version_retention_by_id.id == file_version_retention.id
    client.retention_policies.delete_retention_policy_by_id(retention_policy.id)
    client.folders.delete_folder_by_id(folder.id, recursive=True)
