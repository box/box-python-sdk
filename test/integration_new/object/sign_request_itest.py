from datetime import datetime

import pytest

from boxsdk import BoxAPIException
from test.integration_new import CLIENT
from test.integration_new.context_managers.box_sign_request import BoxTestSignRequest
from test.integration_new.context_managers.box_test_file import BoxTestFile
from test.integration_new.context_managers.box_test_folder import BoxTestFolder

SIGN_REQUEST_TESTS_DIRECTORY_NAME = 'sign-request-integration-tests'


@pytest.fixture(scope="module", autouse=True)
def parent_folder():
    with BoxTestFolder(name=f'{SIGN_REQUEST_TESTS_DIRECTORY_NAME} {datetime.now()}') as folder:
        yield folder


def test_test_sign_request(parent_folder, small_file_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as test_file:
        file = {
            'id': test_file.object_id,
            'type': test_file.object_type,
        }
        files = [file]
        signer1 = {
            'email': 'signer1@mail.com',
            'signer_group_id': 'reviewer',
        }
        signer2 = {
            'email': 'signer2@mail.com',
            'signer_group_id': 'reviewer',
        }
        signers = [signer1, signer2]

        sign_request = CLIENT.create_sign_request_v2(
            files=files,
            signers=signers,
            parent_folder_id=parent_folder.id
        )

        try:
            assert sign_request.id
            assert len(sign_request.signers) == 3
            signer_group_id = None
            signer_count = 0
            for signer in sign_request.signers:
                if signer['role'] == 'signer':
                    signer_count += 1
                    if signer_group_id is None:
                        signer_group_id = signer['signer_group_id']
                    assert signer['signer_group_id'] == signer_group_id
            assert signer_count == 2
        finally:
            CLIENT.sign_request(sign_request.id).cancel()


def test_webhook_sign_request(parent_folder, small_file_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as test_file:
        file = {
            'id': test_file.object_id,
            'type': test_file.object_type,
        }
        files = [file]
        signer = {
            'email': 'signer@mail.com',
        }
        signers = [signer]

        with BoxTestSignRequest(files=files, signers=signers, parent_folder_id=parent_folder.id) as sign_request:
            webhook_url = 'https://example.com/webhook'
            new_webhook_url = 'https://example.com/new-webhook'

            assert len(sign_request.sign_files['files']) == 1

            sign_file = sign_request.sign_files['files'][0]
            webhook_file = CLIENT.file(file_id=sign_file['id'])
            webhook = CLIENT.create_webhook(
                webhook_file,
                ['SIGN_REQUEST.COMPLETED', 'SIGN_REQUEST.DECLINED', 'SIGN_REQUEST.EXPIRED'],
                webhook_url
            )

            try:
                assert webhook.id
                assert webhook.triggers == ['SIGN_REQUEST.COMPLETED', 'SIGN_REQUEST.DECLINED', 'SIGN_REQUEST.EXPIRED']
                assert webhook.address == webhook_url

                update_data = {
                    'address': new_webhook_url,
                    'triggers': ['SIGN_REQUEST.COMPLETED']
                }
                webhook = webhook.update_info(data=update_data)

                assert webhook.address == new_webhook_url
                assert webhook.triggers == ['SIGN_REQUEST.COMPLETED']
            finally:
                webhook.delete()

            with pytest.raises(BoxAPIException):
                webhook.get()
