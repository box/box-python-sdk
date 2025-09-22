from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.sign_request import SignRequest

from box_sdk_gen.schemas.file_base import FileBase

from box_sdk_gen.schemas.sign_request_create_signer import SignRequestCreateSigner

from box_sdk_gen.schemas.sign_request_create_signer import (
    SignRequestCreateSignerRoleField,
)

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.sign_request_prefill_tag import SignRequestPrefillTag

from box_sdk_gen.schemas.sign_requests import SignRequests

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import date_from_string

from box_sdk_gen.internal.utils import date_to_string

from test.box_sdk_gen.test.commons import upload_new_file

from test.box_sdk_gen.test.commons import create_new_folder

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testCreateGetCancelAndListSignRequest():
    signer_email: str = ''.join([get_uuid(), '@box.com'])
    file_to_sign: FileFull = upload_new_file()
    destination_folder: FolderFull = create_new_folder()
    created_sign_request: SignRequest = client.sign_requests.create_sign_request(
        [
            SignRequestCreateSigner(
                email=signer_email,
                suppress_notifications=True,
                declined_redirect_url='https://www.box.com',
                embed_url_external_user_id='123',
                is_in_person=False,
                login_required=False,
                password='password',
                role=SignRequestCreateSignerRoleField.SIGNER,
            )
        ],
        source_files=[FileBase(id=file_to_sign.id)],
        parent_folder=FolderMini(id=destination_folder.id),
        is_document_preparation_needed=False,
        redirect_url='https://www.box.com',
        declined_redirect_url='https://www.box.com',
        are_text_signatures_enabled=True,
        email_subject='Sign this document',
        email_message='Please sign this document',
        are_reminders_enabled=True,
        name='Sign Request',
        prefill_tags=[
            SignRequestPrefillTag(
                date_value=date_from_string('2035-01-01'), document_tag_id='0'
            )
        ],
        days_valid=30,
        external_id='123',
        external_system_name='BoxSignIntegration',
    )
    assert created_sign_request.are_reminders_enabled == True
    assert created_sign_request.are_text_signatures_enabled == True
    assert created_sign_request.days_valid == 30
    assert created_sign_request.declined_redirect_url == 'https://www.box.com'
    assert created_sign_request.email_message == 'Please sign this document'
    assert created_sign_request.email_subject == 'Sign this document'
    assert created_sign_request.external_id == '123'
    assert created_sign_request.external_system_name == 'BoxSignIntegration'
    assert created_sign_request.is_document_preparation_needed == False
    assert created_sign_request.name == 'Sign Request.pdf'
    assert created_sign_request.redirect_url == 'https://www.box.com'
    assert created_sign_request.sign_files.files[0].name == created_sign_request.name
    assert created_sign_request.signers[1].email == signer_email
    assert created_sign_request.signers[1].suppress_notifications == True
    assert (
        created_sign_request.signers[1].declined_redirect_url == 'https://www.box.com'
    )
    assert created_sign_request.signers[1].embed_url_external_user_id == '123'
    assert created_sign_request.signers[1].is_in_person == False
    assert created_sign_request.signers[1].login_required == False
    assert to_string(created_sign_request.signers[1].role) == 'signer'
    assert created_sign_request.parent_folder.id == destination_folder.id
    assert (
        date_to_string(created_sign_request.prefill_tags[0].date_value) == '2035-01-01'
    )
    new_sign_request: SignRequest = client.sign_requests.get_sign_request_by_id(
        created_sign_request.id
    )
    assert new_sign_request.sign_files.files[0].name == created_sign_request.name
    assert new_sign_request.signers[1].email == signer_email
    assert new_sign_request.parent_folder.id == destination_folder.id
    cancelled_sign_request: SignRequest = client.sign_requests.cancel_sign_request(
        created_sign_request.id
    )
    assert to_string(cancelled_sign_request.status) == 'cancelled'
    sign_requests: SignRequests = client.sign_requests.get_sign_requests()
    assert to_string(sign_requests.entries[0].type) == 'sign-request'
    client.folders.delete_folder_by_id(destination_folder.id, recursive=True)
    client.files.delete_file_by_id(file_to_sign.id)


def testCreateSignRequestWithSignerGroupId():
    signer_1_email: str = ''.join([get_uuid(), '@box.com'])
    signer_2_email: str = ''.join([get_uuid(), '@box.com'])
    file_to_sign: FileFull = upload_new_file()
    destination_folder: FolderFull = create_new_folder()
    created_sign_request: SignRequest = client.sign_requests.create_sign_request(
        [
            SignRequestCreateSigner(email=signer_1_email, signer_group_id='user'),
            SignRequestCreateSigner(email=signer_2_email, signer_group_id='user'),
        ],
        source_files=[FileBase(id=file_to_sign.id)],
        parent_folder=FolderMini(id=destination_folder.id),
    )
    assert len(created_sign_request.signers) == 3
    assert not created_sign_request.signers[1].signer_group_id == None
    assert (
        created_sign_request.signers[1].signer_group_id
        == created_sign_request.signers[2].signer_group_id
    )
    client.folders.delete_folder_by_id(destination_folder.id, recursive=True)
    client.files.delete_file_by_id(file_to_sign.id)
