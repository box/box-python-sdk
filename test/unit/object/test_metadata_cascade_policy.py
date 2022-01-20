# coding: utf-8

import json
import pytest

from boxsdk.config import API
from boxsdk.object.enterprise import Enterprise
from boxsdk.object.folder import Folder
from boxsdk.object.metadata_cascade_policy import MetadataCascadePolicy, CascadePolicyConflictResolution


@pytest.fixture()
def test_cascade_policy(mock_box_session):
    return MetadataCascadePolicy(mock_box_session, 'test_cascade_policy_id')


def test_get(test_cascade_policy, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/metadata_cascade_policies/{test_cascade_policy.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'id': '84113349-794d-445c-b93c-d8481b223434',
        'type': 'metadata_cascade_policy',
        'owner_enterprise': {
            'type': 'enterprise',
            'id': '11111',
        },
        'parent': {
            'type': 'folder',
            'id': '22222',
        },
        'scope': 'enterprise_11111',
        'templateKey': 'testTemplate',
    }

    cascade_policy = test_cascade_policy.get()

    mock_box_session.get.assert_called_once_with(expected_url, params=None, headers=None)
    assert isinstance(cascade_policy, MetadataCascadePolicy)
    enterprise = cascade_policy.owner_enterprise
    assert isinstance(enterprise, Enterprise)
    assert enterprise.object_id == '11111'
    folder = cascade_policy.parent
    assert isinstance(folder, Folder)
    assert folder.object_id == '22222'
    assert cascade_policy.scope == 'enterprise_11111'
    assert cascade_policy.templateKey == 'testTemplate'


def test_delete(test_cascade_policy, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/metadata_cascade_policies/{test_cascade_policy.object_id}'
    mock_box_session.delete.return_value.ok = True

    result = test_cascade_policy.delete()

    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})
    assert result is True


def test_force_apply(test_cascade_policy, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/metadata_cascade_policies/{test_cascade_policy.object_id}/apply'
    expected_body = {
        'conflict_resolution': 'overwrite',
    }
    mock_box_session.post.return_value.ok = True

    result = test_cascade_policy.force_apply(CascadePolicyConflictResolution.OVERWRITE)

    mock_box_session.post.assert_called_once_with(
        expected_url,
        data=json.dumps(expected_body),
        expect_json_response=False
    )
    assert result is True
