from box_sdk_gen.internal.utils import to_string

from typing import List

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.metadata_template import MetadataTemplate

from box_sdk_gen.managers.metadata_templates import CreateMetadataTemplateFields

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsTypeField,
)

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsOptionsField,
)

from box_sdk_gen.schemas.metadata_full import MetadataFull

from box_sdk_gen.managers.folder_metadata import CreateFolderMetadataByIdScope

from box_sdk_gen.managers.folder_metadata import UpdateFolderMetadataByIdScope

from box_sdk_gen.managers.folder_metadata import UpdateFolderMetadataByIdRequestBody

from box_sdk_gen.managers.folder_metadata import (
    UpdateFolderMetadataByIdRequestBodyOpField,
)

from box_sdk_gen.managers.folder_metadata import DeleteFolderMetadataByIdScope

from box_sdk_gen.managers.metadata_templates import DeleteMetadataTemplateScope

from box_sdk_gen.schemas.metadatas import Metadatas

from box_sdk_gen.managers.folder_metadata import GetFolderMetadataByIdScope

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import create_new_folder

client: BoxClient = get_default_client()


def testUpdatingFolderMetadata():
    folder: FolderFull = create_new_folder()
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
    created_metadata: MetadataFull = (
        client.folder_metadata.create_folder_metadata_by_id(
            folder.id,
            CreateFolderMetadataByIdScope.ENTERPRISE,
            template_key,
            {
                'name': 'John',
                'age': 23,
                'birthDate': '2001-01-03T02:20:50.520Z',
                'countryCode': 'US',
                'sports': ['basketball', 'tennis'],
            },
        )
    )
    updated_metadata: MetadataFull = (
        client.folder_metadata.update_folder_metadata_by_id(
            folder.id,
            UpdateFolderMetadataByIdScope.ENTERPRISE,
            template_key,
            [
                UpdateFolderMetadataByIdRequestBody(
                    op=UpdateFolderMetadataByIdRequestBodyOpField.REPLACE,
                    path='/name',
                    value='Jack',
                ),
                UpdateFolderMetadataByIdRequestBody(
                    op=UpdateFolderMetadataByIdRequestBodyOpField.REPLACE,
                    path='/age',
                    value=24,
                ),
                UpdateFolderMetadataByIdRequestBody(
                    op=UpdateFolderMetadataByIdRequestBodyOpField.REPLACE,
                    path='/birthDate',
                    value='2000-01-03T02:20:50.520Z',
                ),
                UpdateFolderMetadataByIdRequestBody(
                    op=UpdateFolderMetadataByIdRequestBodyOpField.REPLACE,
                    path='/countryCode',
                    value='CA',
                ),
                UpdateFolderMetadataByIdRequestBody(
                    op=UpdateFolderMetadataByIdRequestBodyOpField.REPLACE,
                    path='/sports',
                    value=['football'],
                ),
            ],
        )
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
    client.folder_metadata.delete_folder_metadata_by_id(
        folder.id, DeleteFolderMetadataByIdScope.ENTERPRISE, template_key
    )
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template_key
    )
    client.folders.delete_folder_by_id(folder.id)


def testGlobalFolderMetadata():
    folder: FolderFull = create_new_folder()
    folder_metadata: Metadatas = client.folder_metadata.get_folder_metadata(folder.id)
    assert len(folder_metadata.entries) == 0
    created_metadata: MetadataFull = (
        client.folder_metadata.create_folder_metadata_by_id(
            folder.id,
            CreateFolderMetadataByIdScope.GLOBAL,
            'properties',
            {'abc': 'xyz'},
        )
    )
    assert to_string(created_metadata.template) == 'properties'
    assert to_string(created_metadata.scope) == 'global'
    assert created_metadata.version == 0
    received_metadata: MetadataFull = client.folder_metadata.get_folder_metadata_by_id(
        folder.id, GetFolderMetadataByIdScope.GLOBAL, 'properties'
    )
    assert to_string(received_metadata.extra_data.get('abc')) == 'xyz'
    new_value: str = 'bar'
    client.folder_metadata.update_folder_metadata_by_id(
        folder.id,
        UpdateFolderMetadataByIdScope.GLOBAL,
        'properties',
        [
            UpdateFolderMetadataByIdRequestBody(
                op=UpdateFolderMetadataByIdRequestBodyOpField.REPLACE,
                path='/abc',
                value=new_value,
            )
        ],
    )
    received_updated_metadata: MetadataFull = (
        client.folder_metadata.get_folder_metadata_by_id(
            folder.id, GetFolderMetadataByIdScope.GLOBAL, 'properties'
        )
    )
    assert to_string(received_updated_metadata.extra_data.get('abc')) == new_value
    client.folder_metadata.delete_folder_metadata_by_id(
        folder.id, DeleteFolderMetadataByIdScope.GLOBAL, 'properties'
    )
    with pytest.raises(Exception):
        client.folder_metadata.get_folder_metadata_by_id(
            folder.id, GetFolderMetadataByIdScope.GLOBAL, 'properties'
        )
    client.folders.delete_folder_by_id(folder.id)


def testEnterpriseFolderMetadata():
    folder: FolderFull = create_new_folder()
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
    created_metadata: MetadataFull = (
        client.folder_metadata.create_folder_metadata_by_id(
            folder.id,
            CreateFolderMetadataByIdScope.ENTERPRISE,
            template_key,
            {
                'name': 'John',
                'age': 23,
                'birthDate': '2001-01-03T02:20:50.520Z',
                'countryCode': 'US',
                'sports': ['basketball', 'tennis'],
            },
        )
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
    client.folder_metadata.delete_folder_metadata_by_id(
        folder.id, DeleteFolderMetadataByIdScope.ENTERPRISE, template_key
    )
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template_key
    )
    client.folders.delete_folder_by_id(folder.id)
