from datetime import datetime

import pytest

from boxsdk.object.metadata_template import MetadataField, MetadataFieldType
from test.integration_new import CLIENT
from test.integration_new.context_managers.box_test_folder import BoxTestFolder

FILE_TESTS_DIRECTORY_NAME = 'metadata_template-integration-tests'


@pytest.fixture(scope="module", autouse=True)
def parent_folder():
    with BoxTestFolder(name=f'{FILE_TESTS_DIRECTORY_NAME} {datetime.now()}') as folder:
        yield folder


def test_create_metedata_template_with_fields(parent_folder):
    metadata_template_fields = [
        MetadataField(
            field_type=MetadataFieldType.ENUM,
            display_name='State',
            key='state',
            description='Which state in USA',
            options=['CA', 'TX', 'NY'],
            hidden=True
        )
    ]

    metadata_template = CLIENT.create_metadata_template(
        display_name="template_name", fields=metadata_template_fields, hidden=False
    )

    try:
        assert metadata_template.displayName == 'template_name'
        assert not metadata_template.hidden

        metadata_template_field = metadata_template.fields[0]
        assert metadata_template_field['type'] == 'enum'
        assert metadata_template_field['displayName'] == 'State'
        assert metadata_template_field['key'] == 'state'
        assert metadata_template_field['description'] == 'Which state in USA'
        assert len(metadata_template_field['options']) == 3
        assert metadata_template_field['hidden']

    finally:
        metadata_template.delete()
