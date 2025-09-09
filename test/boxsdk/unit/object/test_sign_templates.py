import pytest

from boxsdk.config import API
from boxsdk.object.sign_template import SignTemplate


@pytest.fixture(scope='module')
def mock_sign_template_response():
    mock_sign_template = {
        "id": "93153068-5420-467b-b8ef-8e54bfb7be42",
        "type": "sign-template",
        "name": "important-file.pdf",
        "email_message": "Please sign this document.\n\nKind regards",
        "email_subject": (
            "Box User (boxuser@box.com) has requested your signature on a document"
        ),
        "parent_folder": {
            "id": "123456789",
            "etag": "0",
            "type": "folder",
            "sequence_id": "0",
            "name": "My Sign Requests",
        },
        "auto_expire_days": "null",
        "source_files": [
            {
                "id": "123456",
                "etag": "0",
                "type": "file",
                "sequence_id": "0",
                "sha1": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "file_version": {
                    "id": "123456",
                    "type": "file_version",
                    "sha1": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                },
            }
        ],
        "are_email_settings_locked": "false",
        "are_fields_locked": "false",
        "are_files_locked": "false",
        "are_options_locked": "false",
        "are_recipients_locked": "false",
        "signers": [
            {
                "email": "",
                "label": "",
                "public_id": "AAQXQXJZ4",
                "role": "final_copy_reader",
                "is_in_person": "false",
                "order": 1,
                "inputs": [],
            },
            {
                "email": "",
                "label": "",
                "public_id": "13XQXJZ4",
                "role": "signer",
                "is_in_person": "false",
                "order": 1,
                "inputs": [
                    {
                        "document_tag_id": None,
                        "id": "0260f921-3b52-477f-ae74-0b0b0b0b0b0b",
                        "type": "signature",
                        "text_value": None,
                        "is_required": True,
                        "coordinates": {
                            "x": 0.27038464059712,
                            "y": 0.10051756244533624,
                        },
                        "dimensions": {
                            "width": 0.23570031566618235,
                            "height": 0.04781003891921971,
                        },
                        "date_value": None,
                        "page_index": 0,
                        "checkbox_value": None,
                        "document_id": "2fdf9003-d798-40ee-be7f-0b0b0b0b0b0b",
                        "content_type": "signature",
                        "dropdown_choices": None,
                        "group_id": None,
                        "label": None,
                    }
                ],
            },
        ],
        "ready_sign_link": None,
        "custom_branding": None,
        "days_valid": 0,
        "additional_info": {
            "non_editable": [],
            "required": {"signers": [["email"], ["email"]]},
        },
    }
    return mock_sign_template


def test_get_sign_template(
    test_sign_template, mock_box_session, mock_sign_template_response
):
    expected_url = f'{API.BASE_API_URL}/sign_templates/{test_sign_template.object_id}'
    mock_box_session.get.return_value.json.return_value = mock_sign_template_response

    sign_template = test_sign_template.get()

    mock_box_session.get.assert_called_once_with(
        expected_url, headers=None, params=None
    )

    assert isinstance(sign_template, SignTemplate)

    assert sign_template.id == '93153068-5420-467b-b8ef-8e54bfb7be42'
    assert sign_template.name == 'important-file.pdf'
    assert sign_template.email_message == 'Please sign this document.\n\nKind regards'
