from box_sdk_gen.internal.utils import to_string

from typing import List

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.metadata_template import MetadataTemplate

from box_sdk_gen.managers.metadata_templates import CreateMetadataTemplateFields

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsTypeField,
)

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsOptionsField,
)

from box_sdk_gen.schemas.metadata_full import MetadataFull

from box_sdk_gen.managers.file_metadata import CreateFileMetadataByIdScope

from box_sdk_gen.managers.file_metadata import UpdateFileMetadataByIdScope

from box_sdk_gen.managers.file_metadata import UpdateFileMetadataByIdRequestBody

from box_sdk_gen.managers.file_metadata import UpdateFileMetadataByIdRequestBodyOpField

from box_sdk_gen.managers.file_metadata import DeleteFileMetadataByIdScope

from box_sdk_gen.managers.metadata_templates import DeleteMetadataTemplateScope

from box_sdk_gen.schemas.metadatas import Metadatas

from box_sdk_gen.managers.file_metadata import GetFileMetadataByIdScope

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

client: BoxClient = get_default_client()


def testUpdatingFileMetadata():
    file: FileFull = upload_new_file()
    template_key: str = ''.join(['key', get_uuid()])
    template: MetadataTemplate = client.metadata_templates.create_metadata_template(
        'enterprise',
        template_key,
        template_key=template_key,
        fields=[
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.STRING,
                key='name',
                display_name='name',
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
    created_metadata: MetadataFull = client.file_metadata.create_file_metadata_by_id(
        file.id,
        CreateFileMetadataByIdScope.ENTERPRISE,
        template_key,
        {
            'name': 'John',
            'age': 23,
            'birthDate': '2001-01-03T02:20:50.520Z',
            'countryCode': 'US',
            'sports': ['basketball', 'tennis'],
        },
    )
    updated_metadata: MetadataFull = client.file_metadata.update_file_metadata_by_id(
        file.id,
        UpdateFileMetadataByIdScope.ENTERPRISE,
        template_key,
        [
            UpdateFileMetadataByIdRequestBody(
                op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE,
                path='/name',
                value='Jack',
            ),
            UpdateFileMetadataByIdRequestBody(
                op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE,
                path='/age',
                value=24,
            ),
            UpdateFileMetadataByIdRequestBody(
                op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE,
                path='/birthDate',
                value='2000-01-03T02:20:50.520Z',
            ),
            UpdateFileMetadataByIdRequestBody(
                op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE,
                path='/countryCode',
                value='CA',
            ),
            UpdateFileMetadataByIdRequestBody(
                op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE,
                path='/sports',
                value=['football'],
            ),
        ],
    )
    assert to_string(updated_metadata.template) == template_key
    assert to_string(updated_metadata.extra_data.get('name')) == 'Jack'
    assert to_string(updated_metadata.extra_data.get('age')) == '24'
    assert (
        to_string(updated_metadata.extra_data.get('birthDate'))
        == '2000-01-03T02:20:50.520Z'
    )
    assert to_string(updated_metadata.extra_data.get('countryCode')) == 'CA'
    sports: List[str] = updated_metadata.extra_data.get('sports')
    assert sports[0] == 'football'
    client.file_metadata.delete_file_metadata_by_id(
        file.id, DeleteFileMetadataByIdScope.ENTERPRISE, template_key
    )
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template_key
    )
    client.files.delete_file_by_id(file.id)


def testGlobalFileMetadata():
    file: FileFull = upload_new_file()
    file_metadata: Metadatas = client.file_metadata.get_file_metadata(file.id)
    assert len(file_metadata.entries) == 0
    created_metadata: MetadataFull = client.file_metadata.create_file_metadata_by_id(
        file.id, CreateFileMetadataByIdScope.GLOBAL, 'properties', {'abc': 'xyz'}
    )
    assert to_string(created_metadata.template) == 'properties'
    assert to_string(created_metadata.scope) == 'global'
    assert created_metadata.version == 0
    received_metadata: MetadataFull = client.file_metadata.get_file_metadata_by_id(
        file.id, GetFileMetadataByIdScope.GLOBAL, 'properties'
    )
    assert to_string(received_metadata.extra_data.get('abc')) == 'xyz'
    new_value: str = 'bar'
    client.file_metadata.update_file_metadata_by_id(
        file.id,
        UpdateFileMetadataByIdScope.GLOBAL,
        'properties',
        [
            UpdateFileMetadataByIdRequestBody(
                op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE,
                path='/abc',
                value=new_value,
            )
        ],
    )
    received_updated_metadata: MetadataFull = (
        client.file_metadata.get_file_metadata_by_id(
            file.id, GetFileMetadataByIdScope.GLOBAL, 'properties'
        )
    )
    assert to_string(received_updated_metadata.extra_data.get('abc')) == new_value
    client.file_metadata.delete_file_metadata_by_id(
        file.id, DeleteFileMetadataByIdScope.GLOBAL, 'properties'
    )
    with pytest.raises(Exception):
        client.file_metadata.get_file_metadata_by_id(
            file.id, GetFileMetadataByIdScope.GLOBAL, 'properties'
        )
    client.files.delete_file_by_id(file.id)


def testEnterpriseFileMetadata():
    file: FileFull = upload_new_file()
    template_key: str = ''.join(['key', get_uuid()])
    client.metadata_templates.create_metadata_template(
        'enterprise',
        template_key,
        template_key=template_key,
        fields=[
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.STRING,
                key='name',
                display_name='name',
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
    created_metadata: MetadataFull = client.file_metadata.create_file_metadata_by_id(
        file.id,
        CreateFileMetadataByIdScope.ENTERPRISE,
        template_key,
        {
            'name': 'John',
            'age': 23,
            'birthDate': '2001-01-03T02:20:50.520Z',
            'countryCode': 'US',
            'sports': ['basketball', 'tennis'],
        },
    )
    assert to_string(created_metadata.template) == template_key
    assert to_string(created_metadata.extra_data.get('name')) == 'John'
    assert to_string(created_metadata.extra_data.get('age')) == '23'
    assert (
        to_string(created_metadata.extra_data.get('birthDate'))
        == '2001-01-03T02:20:50.520Z'
    )
    assert to_string(created_metadata.extra_data.get('countryCode')) == 'US'
    sports: List[str] = created_metadata.extra_data.get('sports')
    assert sports[0] == 'basketball'
    assert sports[1] == 'tennis'
    client.file_metadata.delete_file_metadata_by_id(
        file.id, DeleteFileMetadataByIdScope.ENTERPRISE, template_key
    )
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template_key
    )
    client.files.delete_file_by_id(file.id)
