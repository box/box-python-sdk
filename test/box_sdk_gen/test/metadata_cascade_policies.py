from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.managers.metadata_templates import CreateMetadataTemplateFields

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsTypeField,
)

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.metadata_cascade_policy import MetadataCascadePolicy

from box_sdk_gen.managers.metadata_cascade_policies import (
    CreateMetadataCascadePolicyScope,
)

from box_sdk_gen.schemas.metadata_cascade_policies import MetadataCascadePolicies

from box_sdk_gen.managers.metadata_cascade_policies import (
    ApplyMetadataCascadePolicyConflictResolution,
)

from box_sdk_gen.managers.folder_metadata import CreateFolderMetadataByIdScope

from box_sdk_gen.managers.metadata_templates import DeleteMetadataTemplateScope

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import to_string

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import create_new_folder

from test.box_sdk_gen.test.commons import upload_new_file

client: BoxClient = get_default_client()


def testMetadataCascadePolicies():
    template_key: str = ''.join(['key', get_uuid()])
    client.metadata_templates.create_metadata_template(
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
    folder: FolderFull = create_new_folder()
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    cascade_policy: MetadataCascadePolicy = (
        client.metadata_cascade_policies.create_metadata_cascade_policy(
            folder.id, CreateMetadataCascadePolicyScope.ENTERPRISE, template_key
        )
    )
    assert to_string(cascade_policy.type) == 'metadata_cascade_policy'
    assert to_string(cascade_policy.owner_enterprise.type) == 'enterprise'
    assert to_string(cascade_policy.owner_enterprise.id) == enterprise_id
    assert to_string(cascade_policy.parent.type) == 'folder'
    assert cascade_policy.parent.id == folder.id
    assert to_string(cascade_policy.scope) == ''.join(['enterprise_', enterprise_id])
    assert cascade_policy.template_key == template_key
    cascade_policy_id: str = cascade_policy.id
    policy_from_the_api: MetadataCascadePolicy = (
        client.metadata_cascade_policies.get_metadata_cascade_policy_by_id(
            cascade_policy_id
        )
    )
    assert cascade_policy_id == policy_from_the_api.id
    policies: MetadataCascadePolicies = (
        client.metadata_cascade_policies.get_metadata_cascade_policies(folder.id)
    )
    assert len(policies.entries) == 1
    with pytest.raises(Exception):
        client.metadata_cascade_policies.apply_metadata_cascade_policy(
            cascade_policy_id, ApplyMetadataCascadePolicyConflictResolution.OVERWRITE
        )
    client.folder_metadata.create_folder_metadata_by_id(
        folder.id,
        CreateFolderMetadataByIdScope.ENTERPRISE,
        template_key,
        {'testName': 'xyz'},
    )
    client.metadata_cascade_policies.apply_metadata_cascade_policy(
        cascade_policy_id, ApplyMetadataCascadePolicyConflictResolution.OVERWRITE
    )
    client.metadata_cascade_policies.delete_metadata_cascade_policy_by_id(
        cascade_policy_id
    )
    with pytest.raises(Exception):
        client.metadata_cascade_policies.get_metadata_cascade_policy_by_id(
            cascade_policy_id
        )
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template_key
    )
    client.folders.delete_folder_by_id(folder.id)
