from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.metadata_template import MetadataTemplate

from box_sdk_gen.managers.metadata_templates import CreateMetadataTemplateFields

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsTypeField,
)

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsOptionsField,
)

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.metadata_full import MetadataFull

from box_sdk_gen.managers.file_metadata import CreateFileMetadataByIdScope

from box_sdk_gen.schemas.metadata_query_results import MetadataQueryResults

from box_sdk_gen.managers.metadata_templates import DeleteMetadataTemplateScope

from box_sdk_gen.schemas.search_results_response import SearchResultsResponse

from box_sdk_gen.schemas.metadata_filter import MetadataFilter

from box_sdk_gen.schemas.metadata_filter import MetadataFilterScopeField

from box_sdk_gen.managers.search import SearchForContentTrashContent

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import date_time_from_string

from box_sdk_gen.internal.utils import delay_in_seconds

from test.box_sdk_gen.test.commons import get_default_client

from box_sdk_gen.schemas.metadata_field_filter_date_range import (
    MetadataFieldFilterDateRange,
)

from box_sdk_gen.schemas.metadata_field_filter_float_range import (
    MetadataFieldFilterFloatRange,
)

from box_sdk_gen.schemas.search_results import SearchResults

from box_sdk_gen.schemas.search_results_with_shared_links import (
    SearchResultsWithSharedLinks,
)

client: BoxClient = get_default_client()


def testCreateMetaDataQueryExecuteRead():
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
    assert template.template_key == template_key
    files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=get_uuid(), parent=UploadFileAttributesParentField(id='0')
        ),
        generate_byte_stream(10),
    )
    file: FileFull = files.entries[0]
    metadata: MetadataFull = client.file_metadata.create_file_metadata_by_id(
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
    assert metadata.template == template_key
    assert metadata.scope == template.scope
    delay_in_seconds(5)
    search_from: str = ''.join([template.scope, '.', template.template_key])
    query: MetadataQueryResults = client.search.search_by_metadata_query(
        search_from,
        '0',
        query='name = :name AND age < :age AND birthDate >= :birthDate AND countryCode = :countryCode AND sports = :sports',
        query_params={
            'name': 'John',
            'age': 50,
            'birthDate': '2001-01-01T02:20:10.120Z',
            'countryCode': 'US',
            'sports': ['basketball', 'tennis'],
        },
    )
    assert len(query.entries) >= 0
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template.template_key
    )
    client.files.delete_file_by_id(file.id)


def testMetadataFilters():
    template_key: str = ''.join(['key', get_uuid()])
    template: MetadataTemplate = client.metadata_templates.create_metadata_template(
        'enterprise',
        template_key,
        template_key=template_key,
        fields=[
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.FLOAT,
                key='floatField',
                display_name='floatField',
            ),
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.STRING,
                key='stringField',
                display_name='stringField',
            ),
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.DATE,
                key='dateField',
                display_name='dateField',
            ),
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.ENUM,
                key='enumField',
                display_name='enumField',
                options=[
                    CreateMetadataTemplateFieldsOptionsField(key='enumValue1'),
                    CreateMetadataTemplateFieldsOptionsField(key='enumValue2'),
                ],
            ),
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.MULTISELECT,
                key='multiSelectField',
                display_name='multiSelectField',
                options=[
                    CreateMetadataTemplateFieldsOptionsField(key='multiSelectValue1'),
                    CreateMetadataTemplateFieldsOptionsField(key='multiSelectValue2'),
                ],
            ),
        ],
    )
    files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=get_uuid(), parent=UploadFileAttributesParentField(id='0')
        ),
        generate_byte_stream(10),
    )
    file: FileFull = files.entries[0]
    metadata: MetadataFull = client.file_metadata.create_file_metadata_by_id(
        file.id,
        CreateFileMetadataByIdScope.ENTERPRISE,
        template_key,
        {
            'floatField': 10,
            'stringField': 'stringValue',
            'dateField': '2035-01-02T00:00:00Z',
            'enumField': 'enumValue2',
            'multiSelectField': ['multiSelectValue1', 'multiSelectValue2'],
        },
    )
    search_filters: Dict[str, str] = {
        'stringField': 'stringValue',
        'dateField': MetadataFieldFilterDateRange(
            lt=date_time_from_string('2035-01-01T00:00:00Z'),
            gt=date_time_from_string('2035-01-03T00:00:00Z'),
        ),
        'floatField': MetadataFieldFilterFloatRange(lt=9.5, gt=10.5),
        'enumField': 'enumValue2',
        'multiSelectField': ['multiSelectValue1', 'multiSelectValue2'],
    }
    query: SearchResultsResponse = client.search.search_for_content(
        ancestor_folder_ids=['0'],
        mdfilters=[
            MetadataFilter(
                filters=search_filters,
                scope=MetadataFilterScopeField.ENTERPRISE,
                template_key=template_key,
            )
        ],
    )
    query_results: SearchResults = query
    assert len(query_results.entries) >= 0
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template.template_key
    )
    client.files.delete_file_by_id(file.id)


def testGetSearch():
    keyword: str = 'test'
    search: SearchResultsResponse = client.search.search_for_content(
        query=keyword,
        ancestor_folder_ids=['0'],
        trash_content=SearchForContentTrashContent.NON_TRASHED_ONLY,
    )
    assert to_string(search.type) == 'search_results_items'
    search_results: SearchResults = search
    assert len(search_results.entries) >= 0
    search_with_shared_link: SearchResultsResponse = client.search.search_for_content(
        query=keyword,
        ancestor_folder_ids=['0'],
        trash_content=SearchForContentTrashContent.NON_TRASHED_ONLY,
        include_recent_shared_links=True,
    )
    assert to_string(search_with_shared_link.type) == 'search_results_with_shared_links'
    search_results_with_shared_link: SearchResultsWithSharedLinks = (
        search_with_shared_link
    )
    assert len(search_results_with_shared_link.entries) >= 0
