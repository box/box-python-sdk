from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.metadata_template import MetadataTemplate

from box_sdk_gen.managers.metadata_templates import CreateMetadataTemplateFields

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsTypeField,
)

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsOptionsField,
)

from box_sdk_gen.managers.metadata_templates import UpdateMetadataTemplateScope

from box_sdk_gen.managers.metadata_templates import UpdateMetadataTemplateRequestBody

from box_sdk_gen.managers.metadata_templates import (
    UpdateMetadataTemplateRequestBodyOpField,
)

from box_sdk_gen.managers.metadata_templates import GetMetadataTemplateScope

from box_sdk_gen.schemas.metadata_templates import MetadataTemplates

from box_sdk_gen.managers.metadata_templates import DeleteMetadataTemplateScope

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.metadata_full import MetadataFull

from box_sdk_gen.managers.file_metadata import CreateFileMetadataByIdScope

from box_sdk_gen.managers.file_metadata import DeleteFileMetadataByIdScope

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

client: BoxClient = get_default_client()


def testMetadataTemplates():
    template_key: str = ''.join(['key', get_uuid()])
    template: MetadataTemplate = client.metadata_templates.create_metadata_template(
        'enterprise',
        template_key,
        template_key=template_key,
        fields=[
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.STRING,
                key='testName',
                display_name='testName',
            ),
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.FLOAT,
                key='age',
                display_name='age',
            ),
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.DATE,
                key='birthDate',
                display_name='birthDate',
            ),
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.ENUM,
                key='countryCode',
                display_name='countryCode',
                options=[
                    CreateMetadataTemplateFieldsOptionsField(key='US'),
                    CreateMetadataTemplateFieldsOptionsField(key='CA'),
                ],
            ),
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.MULTISELECT,
                key='sports',
                display_name='sports',
                options=[
                    CreateMetadataTemplateFieldsOptionsField(key='basketball'),
                    CreateMetadataTemplateFieldsOptionsField(key='football'),
                    CreateMetadataTemplateFieldsOptionsField(key='tennis'),
                ],
            ),
        ],
    )
    assert template.template_key == template_key
    assert template.display_name == template_key
    assert len(template.fields) == 5
    assert template.fields[0].key == 'testName'
    assert template.fields[0].display_name == 'testName'
    assert to_string(template.fields[0].type) == 'string'
    assert template.fields[1].key == 'age'
    assert template.fields[1].display_name == 'age'
    assert to_string(template.fields[1].type) == 'float'
    assert template.fields[2].key == 'birthDate'
    assert template.fields[2].display_name == 'birthDate'
    assert to_string(template.fields[2].type) == 'date'
    assert template.fields[3].key == 'countryCode'
    assert template.fields[3].display_name == 'countryCode'
    assert to_string(template.fields[3].type) == 'enum'
    assert template.fields[4].key == 'sports'
    assert template.fields[4].display_name == 'sports'
    assert to_string(template.fields[4].type) == 'multiSelect'
    updated_template: MetadataTemplate = (
        client.metadata_templates.update_metadata_template(
            UpdateMetadataTemplateScope.ENTERPRISE,
            template_key,
            [
                UpdateMetadataTemplateRequestBody(
                    op=UpdateMetadataTemplateRequestBodyOpField.ADDFIELD,
                    field_key='newfieldname',
                    data={'type': 'string', 'displayName': 'newFieldName'},
                )
            ],
        )
    )
    assert len(updated_template.fields) == 6
    assert updated_template.fields[5].key == 'newfieldname'
    assert updated_template.fields[5].display_name == 'newFieldName'
    get_metadata_template: MetadataTemplate = (
        client.metadata_templates.get_metadata_template_by_id(template.id)
    )
    assert get_metadata_template.id == template.id
    get_metadata_template_schema: MetadataTemplate = (
        client.metadata_templates.get_metadata_template(
            GetMetadataTemplateScope.ENTERPRISE, template.template_key
        )
    )
    assert get_metadata_template_schema.id == template.id
    enterprise_metadata_templates: MetadataTemplates = (
        client.metadata_templates.get_enterprise_metadata_templates()
    )
    assert len(enterprise_metadata_templates.entries) > 0
    global_metadata_templates: MetadataTemplates = (
        client.metadata_templates.get_global_metadata_templates()
    )
    assert len(global_metadata_templates.entries) > 0
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template.template_key
    )
    with pytest.raises(Exception):
        client.metadata_templates.delete_metadata_template(
            DeleteMetadataTemplateScope.ENTERPRISE, template.template_key
        )


def testGetMetadataTemplateByInstance():
    file: FileFull = upload_new_file()
    template_key: str = ''.join(['key', get_uuid()])
    template: MetadataTemplate = client.metadata_templates.create_metadata_template(
        'enterprise',
        template_key,
        template_key=template_key,
        fields=[
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.STRING,
                key='testName',
                display_name='testName',
            )
        ],
    )
    created_metadata_instance: MetadataFull = (
        client.file_metadata.create_file_metadata_by_id(
            file.id,
            CreateFileMetadataByIdScope.ENTERPRISE,
            template_key,
            {'testName': 'xyz'},
        )
    )
    metadata_templates: MetadataTemplates = (
        client.metadata_templates.get_metadata_templates_by_instance_id(
            created_metadata_instance.id
        )
    )
    assert len(metadata_templates.entries) == 1
    assert metadata_templates.entries[0].display_name == template_key
    assert metadata_templates.entries[0].template_key == template_key
    client.file_metadata.delete_file_metadata_by_id(
        file.id, DeleteFileMetadataByIdScope.ENTERPRISE, template_key
    )
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template.template_key
    )
    client.files.delete_file_by_id(file.id)
