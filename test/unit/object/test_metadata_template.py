import json

from boxsdk.config import API
from boxsdk.object.metadata_template import MetadataTemplate, MetadataField, MetadataFieldType


def test_get(test_metadata_template, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/metadata_templates/{test_metadata_template.scope}/{test_metadata_template.template_key}/schema'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'metadata_template',
        'scope': 'enterprise',
        'displayName': 'Vendor Contract',
        'hidden': True,
        'fields': [
            {
                'type': 'date',
                'displayName': 'Birthday',
                'key': 'bday',
            },
            {
                'type': 'enum',
                'displayName': 'State',
                'options': [
                    {'key': 'CA'},
                    {'key': 'TX'},
                    {'key': 'NY'},
                ],
            },
        ],
        'templateKey': 'vContract',
    }

    template = test_metadata_template.get()

    mock_box_session.get.assert_called_once_with(expected_url, params=None, headers=None)
    assert isinstance(template, MetadataTemplate)
    assert template.object_id is None
    assert template.displayName == 'Vendor Contract'
    fields = template.fields
    assert len(fields) == 2
    field = fields[0]
    assert isinstance(field, dict)
    assert field['type'] == 'date'
    assert field['key'] == 'bday'


def test_delete(test_metadata_template, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/metadata_templates/{test_metadata_template.scope}/{test_metadata_template.template_key}/schema'
    mock_box_session.delete.return_value.ok = True

    result = test_metadata_template.delete()

    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})
    assert result is True


def test_update_info(test_metadata_template, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/metadata_templates/{test_metadata_template.scope}/{test_metadata_template.template_key}/schema'
    updates = test_metadata_template.start_update()
    updates.add_enum_option('state', 'WI')
    updates.add_field(MetadataField(MetadataFieldType.STRING, 'Name'))
    updates.reorder_enum_options('state', ['CA', 'NY', 'TX', 'WI'])
    updates.reorder_fields(['bday', 'name', 'state'])
    updates.edit_field('state', MetadataField(None, 'State of Residency'))
    updates.edit_enum_option_key('state', 'WI', 'WY')
    updates.remove_enum_option('state', 'NY')
    updates.remove_field('bday')
    updates.edit_template({'hidden': False})

    expected_body = [
        {
            'op': 'addEnumOption',
            'fieldKey': 'state',
            'data': {'key': 'WI'},
        },
        {
            'op': 'addField',
            'data': {
                'type': 'string',
                'displayName': 'Name',
            },
        },
        {
            'op': 'reorderEnumOptions',
            'fieldKey': 'state',
            'enumOptionKeys': ['CA', 'NY', 'TX', 'WI'],
        },
        {
            'op': 'reorderFields',
            'fieldKeys': ['bday', 'name', 'state'],
        },
        {
            'op': 'editField',
            'fieldKey': 'state',
            'data': {
                'displayName': 'State of Residency',
            },
        },
        {
            'op': 'editEnumOption',
            'fieldKey': 'state',
            'enumOptionKey': 'WI',
            'data': {
                'key': 'WY',
            },
        },
        {
            'op': 'removeEnumOption',
            'fieldKey': 'state',
            'enumOptionKey': 'NY',
        },
        {
            'op': 'removeField',
            'fieldKey': 'bday',
        },
        {
            'op': 'editTemplate',
            'data': {'hidden': False},
        },
    ]

    mock_box_session.put.return_value.json.return_value = {
        'type': 'metadata_template',
        'scope': 'enterprise',
        'displayName': 'Vendor Contract',
        'hidden': False,
        'fields': [
            {
                'type': 'string',
                'key': 'name',
                'displayName': 'Name',
            },
            {
                'type': 'enum',
                'key': 'state',
                'displayName': 'State of Residency',
                'options': [
                    {'key': 'CA'},
                    {'key': 'TX'},
                    {'key': 'WY'},
                ],
            },
        ],
        'templateKey': 'vContract',
    }

    updated_template = test_metadata_template.update_info(updates=updates)

    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_body), headers=None, params=None)
    assert isinstance(updated_template, MetadataTemplate)
    assert updated_template.hidden is False
    assert updated_template.object_id is None
    fields = updated_template.fields
    assert len(fields) == 2
    field = fields[1]
    assert field['type'] == 'enum'
    assert field['displayName'] == 'State of Residency'
    assert len(field['options']) == 3
    assert field['options'][2]['key'] == 'WY'
