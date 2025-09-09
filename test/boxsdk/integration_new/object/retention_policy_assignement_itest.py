from datetime import datetime
import pytest

from boxsdk import BoxAPIException
from test.boxsdk.integration_new.context_managers.box_retention_policy import (
    BoxRetentionPolicy,
)
from test.boxsdk.integration_new.context_managers.box_test_file import BoxTestFile
from test.boxsdk.integration_new.context_managers.box_test_folder import BoxTestFolder
from test.boxsdk.integration_new.context_managers.box_metadata_template import (
    BoxTestMetadataTemplate,
)

RETENTION_POLICY_ASSIGNMENT_TESTS_DIRECTORY_NAME = (
    'retention-policy-assignment-integration-tests'
)


@pytest.fixture(scope="module", autouse=True)
def parent_folder():
    with BoxTestFolder(
        name=f'{RETENTION_POLICY_ASSIGNMENT_TESTS_DIRECTORY_NAME} {datetime.now()}'
    ) as folder:
        yield folder


@pytest.fixture(scope="module", autouse=True)
def test_file(parent_folder, small_file_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        yield file


def test_delete_retention_policy_assignment(parent_folder, small_file_path):
    with BoxRetentionPolicy(
        disposition_action='permanently_delete', retention_length=1
    ) as retention_policy:
        with BoxTestFolder(
            name=f'{RETENTION_POLICY_ASSIGNMENT_TESTS_DIRECTORY_NAME} {datetime.now()}'
        ) as folder_under_retention:
            retention_policy_assignment = retention_policy.assign(
                folder_under_retention
            )

            assignment = retention_policy_assignment.get()
            assert assignment.id is not None

            retention_policy_assignment.delete()

            with pytest.raises(BoxAPIException):
                retention_policy_assignment.get()


def test_retention_policy_assignement_to_metadata_template():
    with BoxTestMetadataTemplate(display_name="test_template") as metadata_template:
        with BoxRetentionPolicy(
            disposition_action='permanently_delete', retention_length=1
        ) as retention_policy:
            retention_policy_assignment = retention_policy.assign(
                metadata_template, start_date_field='upload_date'
            )

            assignment = retention_policy_assignment.get()
            assert assignment.id is not None
            assert assignment.start_date_field == 'upload_date'

            retention_policy_assignment.delete()

            with pytest.raises(BoxAPIException):
                retention_policy_assignment.get()
