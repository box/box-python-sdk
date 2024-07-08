from datetime import datetime

import pytest

from test.integration_new import CLIENT
from test.integration_new.context_managers.box_test_folder import BoxTestFolder
from test.integration_new.context_managers.box_test_file import BoxTestFile

FOLDER_TESTS_DIRECTORY_NAME = 'folder-integration-tests'


@pytest.fixture(scope='module', autouse=True)
def parent_folder():
    with BoxTestFolder(name=f'{FOLDER_TESTS_DIRECTORY_NAME} {datetime.now()}') as folder:
        yield folder


def test_send_ai_question(parent_folder, small_file_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        items = [{
            'id': file.id,
            'type': 'file',
            'content': 'The sun raises in the east.'
        }]
        answer = CLIENT.send_ai_question(
            items=items,
            prompt='Which direction does the sun raise?',
            mode='single_item_qa'
        )
        assert 'east' in answer['answer'].lower()
        assert answer['completion_reason'] == 'done'


def test_send_ai_text_gen(parent_folder, small_file_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        items = [{
            'id': file.id,
            'type': 'file',
            'content': 'The sun raises in the east.'
        }]
        dialogue_history = [{
            'prompt': 'How does the sun rise?',
            'answer': 'The sun raises in the east.',
            'created_at': '2013-12-12T10:53:43-08:00'
        }, {
            'prompt': 'How many hours does it take for the sun to rise?',
            'answer': 'It takes 24 hours for the sun to rise.',
            'created_at': '2013-12-12T11:20:43-08:00'
        }]
        answer = CLIENT.send_ai_text_gen(
            dialogue_history=dialogue_history,
            items=items,
            prompt='Which direction does the sun raise?'
        )
        assert 'east' in answer['answer'].lower()
        assert answer['completion_reason'] == 'done'
