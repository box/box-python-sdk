from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.legal_hold_policy import LegalHoldPolicy

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.legal_hold_policy_assignment import LegalHoldPolicyAssignment

from box_sdk_gen.managers.legal_hold_policy_assignments import (
    CreateLegalHoldPolicyAssignmentAssignTo,
)

from box_sdk_gen.managers.legal_hold_policy_assignments import (
    CreateLegalHoldPolicyAssignmentAssignToTypeField,
)

from box_sdk_gen.schemas.legal_hold_policy_assignments import LegalHoldPolicyAssignments

from box_sdk_gen.schemas.files_on_hold import FilesOnHold

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

client: BoxClient = get_default_client()


def testLegalHoldPolicyAssignments():
    legal_hold_policy_name: str = get_uuid()
    legal_hold_description: str = 'test description'
    legal_hold_policy: LegalHoldPolicy = (
        client.legal_hold_policies.create_legal_hold_policy(
            legal_hold_policy_name, description=legal_hold_description, is_ongoing=True
        )
    )
    legal_hold_policy_id: str = legal_hold_policy.id
    file: FileFull = upload_new_file()
    file_id: str = file.id
    legal_hold_policy_assignment: LegalHoldPolicyAssignment = (
        client.legal_hold_policy_assignments.create_legal_hold_policy_assignment(
            legal_hold_policy_id,
            CreateLegalHoldPolicyAssignmentAssignTo(
                type=CreateLegalHoldPolicyAssignmentAssignToTypeField.FILE, id=file_id
            ),
        )
    )
    assert (
        to_string(legal_hold_policy_assignment.legal_hold_policy.type)
        == 'legal_hold_policy'
    )
    assert legal_hold_policy_assignment.assigned_to.id == file_id
    assert to_string(legal_hold_policy_assignment.assigned_to.type) == 'file'
    legal_hold_policy_assignment_id: str = legal_hold_policy_assignment.id
    legal_hold_policy_assignment_from_api: LegalHoldPolicyAssignment = (
        client.legal_hold_policy_assignments.get_legal_hold_policy_assignment_by_id(
            legal_hold_policy_assignment_id
        )
    )
    assert legal_hold_policy_assignment_from_api.id == legal_hold_policy_assignment_id
    legal_policy_assignments: LegalHoldPolicyAssignments = (
        client.legal_hold_policy_assignments.get_legal_hold_policy_assignments(
            legal_hold_policy_id
        )
    )
    assert len(legal_policy_assignments.entries) == 1
    files_on_hold: FilesOnHold = (
        client.legal_hold_policy_assignments.get_legal_hold_policy_assignment_file_on_hold(
            legal_hold_policy_assignment_id
        )
    )
    assert len(files_on_hold.entries) == 1
    assert files_on_hold.entries[0].id == file_id
    client.legal_hold_policy_assignments.delete_legal_hold_policy_assignment_by_id(
        legal_hold_policy_assignment_id
    )
    with pytest.raises(Exception):
        client.legal_hold_policy_assignments.delete_legal_hold_policy_assignment_by_id(
            legal_hold_policy_assignment_id
        )
    client.files.delete_file_by_id(file_id)
    try:
        client.legal_hold_policies.delete_legal_hold_policy_by_id(legal_hold_policy_id)
    except Exception:
        print(
            ''.join(['Could not delete Legal Policy with id: ', legal_hold_policy_id])
        )
