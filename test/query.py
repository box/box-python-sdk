from typing import Dict

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.metadata_template import MetadataTemplate

from box_sdk_gen.managers.metadata_templates import CreateMetadataTemplateFields

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsTypeField,
)

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.metadata_full import MetadataFull

from box_sdk_gen.managers.file_metadata import CreateFileMetadataByIdScope

from box_sdk_gen.schemas.v2026_r0.query_results_v2026_r0 import QueryResultsV2026R0

from box_sdk_gen.managers.query import CreateQueryV2026R0Query

from box_sdk_gen.schemas.v2026_r0.query_ancestor_reference_v2026_r0 import (
    QueryAncestorReferenceV2026R0,
)

from box_sdk_gen.managers.metadata_templates import DeleteMetadataTemplateScope

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsOptionsField,
)

from box_sdk_gen.schemas.v2026_r0.query_insights_metric_definition_v2026_r0 import (
    QueryInsightsMetricDefinitionV2026R0TypeField,
)

from box_sdk_gen.schemas.v2026_r0.query_insights_v2026_r0 import QueryInsightsV2026R0

from box_sdk_gen.managers.query import CreateQueryInsightV2026R0Query

from box_sdk_gen.schemas.v2026_r0.query_insights_group_by_v2026_r0 import (
    QueryInsightsGroupByV2026R0,
)

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import delay_in_seconds

from test.commons import get_default_client

from test.commons import upload_new_file

from box_sdk_gen.schemas.v2026_r0.query_insights_metric_definition_v2026_r0 import (
    QueryInsightsMetricDefinitionV2026R0,
)

client: BoxClient = get_default_client()


def testCreateQueryV2026R0():
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
        ],
    )
    assert template.template_key == template_key
    file: FileFull = upload_new_file()
    metadata: MetadataFull = client.file_metadata.create_file_metadata_by_id(
        file.id,
        CreateFileMetadataByIdScope.ENTERPRISE,
        template_key,
        {'name': 'John', 'age': 23, 'birthDate': '2001-01-03T02:20:50.520Z'},
    )
    assert metadata.template == template_key
    assert metadata.scope == template.scope
    delay_in_seconds(10)
    search_from: str = ''.join([template.scope, ':', template.template_key])
    md_prefix: str = ''.join(
        ['metadata.', template.scope, '."', template.template_key, '"']
    )
    predicate: str = ''.join(
        [md_prefix, '.name = :name AND ', md_prefix, '.age < :age']
    )
    query_result: QueryResultsV2026R0 = client.query.create_query_v2026_r0(
        CreateQueryV2026R0Query(
            predicate=predicate,
            params={'name': 'John', 'age': 50},
            ancestors=[QueryAncestorReferenceV2026R0(id='0', type='folder')],
        ),
        limit=10,
        fields=['box:item:name', search_from],
    )
    assert len(query_result.entries) >= 0
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template.template_key
    )
    client.files.delete_file_by_id(file.id)


def testCreateQueryInsightV2026R0():
    template_key: str = ''.join(['key', get_uuid()])
    template: MetadataTemplate = client.metadata_templates.create_metadata_template(
        'enterprise',
        template_key,
        template_key=template_key,
        fields=[
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.ENUM,
                key='category',
                display_name='category',
                options=[
                    CreateMetadataTemplateFieldsOptionsField(key='Sales'),
                    CreateMetadataTemplateFieldsOptionsField(key='Support'),
                ],
            ),
            CreateMetadataTemplateFields(
                type=CreateMetadataTemplateFieldsTypeField.FLOAT,
                key='amount',
                display_name='amount',
            ),
        ],
    )
    assert template.template_key == template_key
    file: FileFull = upload_new_file()
    metadata: MetadataFull = client.file_metadata.create_file_metadata_by_id(
        file.id,
        CreateFileMetadataByIdScope.ENTERPRISE,
        template_key,
        {'category': 'Sales', 'amount': 150},
    )
    assert metadata.template == template_key
    delay_in_seconds(5)
    md_prefix: str = ''.join(
        ['metadata.', template.scope, '."', template.template_key, '"']
    )
    predicate: str = ''.join([md_prefix, '.amount > :minAmount'])
    metrics: Dict[str, QueryInsightsMetricDefinitionV2026R0] = {
        'totalAmount': QueryInsightsMetricDefinitionV2026R0(
            type=QueryInsightsMetricDefinitionV2026R0TypeField.SUM,
            field=''.join([md_prefix, '.amount']),
        ),
        'countItems': QueryInsightsMetricDefinitionV2026R0(
            type=QueryInsightsMetricDefinitionV2026R0TypeField.COUNT,
            field=''.join([md_prefix, '.category']),
        ),
    }
    insight_result: QueryInsightsV2026R0 = client.query.create_query_insight_v2026_r0(
        CreateQueryInsightV2026R0Query(
            predicate=predicate,
            params={'minAmount': 0},
            ancestors=[QueryAncestorReferenceV2026R0(id='0', type='folder')],
            group_by=[
                QueryInsightsGroupByV2026R0(
                    field=''.join([md_prefix, '.category']), bucket_limit=5
                )
            ],
        ),
        metrics,
    )
    assert len(insight_result.insights) >= 0
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template.template_key
    )
    client.files.delete_file_by_id(file.id)
