import pytest

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.metadata_taxonomy import MetadataTaxonomy

from box_sdk_gen.schemas.metadata_taxonomies import MetadataTaxonomies

from box_sdk_gen.schemas.metadata_taxonomy_levels import MetadataTaxonomyLevels

from box_sdk_gen.schemas.metadata_taxonomy_level import MetadataTaxonomyLevel

from box_sdk_gen.schemas.metadata_taxonomy_node import MetadataTaxonomyNode

from box_sdk_gen.schemas.metadata_taxonomy_nodes import MetadataTaxonomyNodes

from box_sdk_gen.schemas.metadata_template import MetadataTemplate

from box_sdk_gen.managers.metadata_templates import CreateMetadataTemplateFields

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsTypeField,
)

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsOptionsRulesField,
)

from box_sdk_gen.managers.metadata_templates import DeleteMetadataTemplateScope

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import delay_in_seconds

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testMetadataTaxonomiesCRUD():
    namespace: str = ''.join(['enterprise_', get_env_var('ENTERPRISE_ID')])
    uuid: str = get_uuid()
    taxonomy_key: str = ''.join(['geography', uuid])
    display_name: str = ''.join(['Geography Taxonomy', uuid])
    created_taxonomy: MetadataTaxonomy = (
        client.metadata_taxonomies.create_metadata_taxonomy(
            display_name, namespace, key=taxonomy_key
        )
    )
    assert created_taxonomy.display_name == display_name
    assert created_taxonomy.namespace == namespace
    taxonomies: MetadataTaxonomies = client.metadata_taxonomies.get_metadata_taxonomies(
        namespace
    )
    assert len(taxonomies.entries) > 0
    assert taxonomies.entries[0].namespace == namespace
    updated_display_name: str = ''.join(['Geography Taxonomy UPDATED', uuid])
    updated_taxonomy: MetadataTaxonomy = (
        client.metadata_taxonomies.update_metadata_taxonomy(
            namespace, taxonomy_key, updated_display_name
        )
    )
    assert updated_taxonomy.display_name == updated_display_name
    assert updated_taxonomy.namespace == namespace
    assert updated_taxonomy.id == created_taxonomy.id
    get_taxonomy: MetadataTaxonomy = (
        client.metadata_taxonomies.get_metadata_taxonomy_by_key(namespace, taxonomy_key)
    )
    assert get_taxonomy.display_name == updated_display_name
    assert get_taxonomy.namespace == namespace
    assert get_taxonomy.id == created_taxonomy.id
    client.metadata_taxonomies.delete_metadata_taxonomy(namespace, taxonomy_key)
    with pytest.raises(Exception):
        client.metadata_taxonomies.get_metadata_taxonomy_by_key(namespace, taxonomy_key)


def testMetadataTaxonomiesNodes():
    namespace: str = ''.join(['enterprise_', get_env_var('ENTERPRISE_ID')])
    uuid: str = get_uuid()
    taxonomy_key: str = ''.join(['geography', uuid])
    display_name: str = ''.join(['Geography Taxonomy', uuid])
    created_taxonomy: MetadataTaxonomy = (
        client.metadata_taxonomies.create_metadata_taxonomy(
            display_name, namespace, key=taxonomy_key
        )
    )
    assert created_taxonomy.display_name == display_name
    assert created_taxonomy.namespace == namespace
    taxonomy_levels: MetadataTaxonomyLevels = (
        client.metadata_taxonomies.create_metadata_taxonomy_level(
            namespace,
            taxonomy_key,
            [
                MetadataTaxonomyLevel(
                    display_name='Continent', description='Continent Level'
                ),
                MetadataTaxonomyLevel(
                    display_name='Country', description='Country Level'
                ),
            ],
        )
    )
    assert len(taxonomy_levels.entries) == 2
    assert taxonomy_levels.entries[0].display_name == 'Continent'
    assert taxonomy_levels.entries[1].display_name == 'Country'
    updated_taxonomy_levels: MetadataTaxonomyLevel = (
        client.metadata_taxonomies.update_metadata_taxonomy_level_by_id(
            namespace,
            taxonomy_key,
            1,
            'Continent UPDATED',
            description='Continent Level UPDATED',
        )
    )
    assert updated_taxonomy_levels.display_name == 'Continent UPDATED'
    assert updated_taxonomy_levels.description == 'Continent Level UPDATED'
    assert updated_taxonomy_levels.level == taxonomy_levels.entries[0].level
    taxonomy_levels_after_addition: MetadataTaxonomyLevels = (
        client.metadata_taxonomies.add_metadata_taxonomy_level(
            namespace, taxonomy_key, 'Region', description='Region Description'
        )
    )
    assert len(taxonomy_levels_after_addition.entries) == 3
    assert taxonomy_levels_after_addition.entries[2].display_name == 'Region'
    taxonomy_levels_after_deletion: MetadataTaxonomyLevels = (
        client.metadata_taxonomies.delete_metadata_taxonomy_level(
            namespace, taxonomy_key
        )
    )
    assert len(taxonomy_levels_after_deletion.entries) == 2
    assert taxonomy_levels_after_deletion.entries[0].display_name == 'Continent UPDATED'
    assert taxonomy_levels_after_deletion.entries[1].display_name == 'Country'
    continent_node: MetadataTaxonomyNode = (
        client.metadata_taxonomies.create_metadata_taxonomy_node(
            namespace, taxonomy_key, 'Europe', 1
        )
    )
    assert continent_node.display_name == 'Europe'
    assert continent_node.level == 1
    country_node: MetadataTaxonomyNode = (
        client.metadata_taxonomies.create_metadata_taxonomy_node(
            namespace, taxonomy_key, 'Poland', 2, parent_id=continent_node.id
        )
    )
    assert country_node.display_name == 'Poland'
    assert country_node.level == 2
    assert country_node.parent_id == continent_node.id
    delay_in_seconds(5)
    all_nodes: MetadataTaxonomyNodes = (
        client.metadata_taxonomies.get_metadata_taxonomy_nodes(namespace, taxonomy_key)
    )
    assert len(all_nodes.entries) == 2
    updated_country_node: MetadataTaxonomyNode = (
        client.metadata_taxonomies.update_metadata_taxonomy_node(
            namespace, taxonomy_key, country_node.id, display_name='Poland UPDATED'
        )
    )
    assert updated_country_node.display_name == 'Poland UPDATED'
    assert updated_country_node.level == 2
    assert updated_country_node.parent_id == country_node.parent_id
    assert updated_country_node.id == country_node.id
    get_country_node: MetadataTaxonomyNode = (
        client.metadata_taxonomies.get_metadata_taxonomy_node_by_id(
            namespace, taxonomy_key, country_node.id
        )
    )
    assert get_country_node.display_name == 'Poland UPDATED'
    assert get_country_node.id == country_node.id
    metadata_template_key: str = ''.join(['templateKey', get_uuid()])
    metadata_template: MetadataTemplate = (
        client.metadata_templates.create_metadata_template(
            'enterprise',
            metadata_template_key,
            template_key=metadata_template_key,
            fields=[
                CreateMetadataTemplateFields(
                    type=CreateMetadataTemplateFieldsTypeField.TAXONOMY,
                    key='taxonomy',
                    display_name='taxonomy',
                    taxonomy_key=taxonomy_key,
                    namespace=namespace,
                    options_rules=CreateMetadataTemplateFieldsOptionsRulesField(
                        multi_select=True, selectable_levels=[1]
                    ),
                )
            ],
        )
    )
    assert metadata_template.template_key == metadata_template_key
    assert metadata_template.display_name == metadata_template_key
    assert len(metadata_template.fields) == 1
    assert to_string(metadata_template.fields[0].type) == 'taxonomy'
    options: MetadataTaxonomyNodes = (
        client.metadata_taxonomies.get_metadata_template_field_options(
            namespace, metadata_template_key, 'taxonomy'
        )
    )
    assert len(options.entries) == 1
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, metadata_template_key
    )
    client.metadata_taxonomies.delete_metadata_taxonomy_node(
        namespace, taxonomy_key, country_node.id
    )
    client.metadata_taxonomies.delete_metadata_taxonomy_node(
        namespace, taxonomy_key, continent_node.id
    )
    delay_in_seconds(5)
    all_nodes_after_deletion: MetadataTaxonomyNodes = (
        client.metadata_taxonomies.get_metadata_taxonomy_nodes(namespace, taxonomy_key)
    )
    assert len(all_nodes_after_deletion.entries) == 0
    client.metadata_taxonomies.delete_metadata_taxonomy(namespace, taxonomy_key)
