from box_sdk_gen.internal.utils import to_string

import pytest

from typing import Dict

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.managers.folders import CreateFolderParent

from box_sdk_gen.schemas.webhook import Webhook

from box_sdk_gen.managers.webhooks import CreateWebhookTarget

from box_sdk_gen.managers.webhooks import CreateWebhookTargetTypeField

from box_sdk_gen.managers.webhooks import CreateWebhookTriggers

from box_sdk_gen.schemas.webhooks import Webhooks

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import date_time_to_string

from box_sdk_gen.internal.utils import epoch_seconds_to_date_time

from box_sdk_gen.internal.utils import get_epoch_time_in_seconds

from box_sdk_gen.internal.utils import compute_webhook_signature

from box_sdk_gen.managers.webhooks import WebhooksManager

from test.commons import get_default_client

client: BoxClient = get_default_client()

def testWebhooksCRUD():
    folder: FolderFull = client.folders.create_folder(get_uuid(), CreateFolderParent(id='0'))
    webhook: Webhook = client.webhooks.create_webhook(CreateWebhookTarget(id=folder.id, type=CreateWebhookTargetTypeField.FOLDER), 'https://example.com/new-webhook', [CreateWebhookTriggers.FILE_UPLOADED])
    assert webhook.target.id == folder.id
    assert to_string(webhook.target.type) == 'folder'
    assert len(webhook.triggers) == len(['FILE.UPLOADED'])
    assert webhook.address == 'https://example.com/new-webhook'
    webhooks: Webhooks = client.webhooks.get_webhooks()
    assert len(webhooks.entries) > 0
    webhook_from_api: Webhook = client.webhooks.get_webhook_by_id(webhook.id)
    assert webhook.id == webhook_from_api.id
    assert webhook.target.id == webhook_from_api.target.id
    assert webhook.address == webhook_from_api.address
    updated_webhook: Webhook = client.webhooks.update_webhook_by_id(webhook.id, address='https://example.com/updated-webhook')
    assert updated_webhook.id == webhook.id
    assert updated_webhook.address == 'https://example.com/updated-webhook'
    client.webhooks.delete_webhook_by_id(webhook.id)
    with pytest.raises(Exception):
        client.webhooks.delete_webhook_by_id(webhook.id)
    client.folders.delete_folder_by_id(folder.id)

def testWebhookValidation():
    primary_key: str = 'SamplePrimaryKey'
    secondary_key: str = 'SampleSecondaryKey'
    incorrect_key: str = 'IncorrectKey'
    body: str = '{"type":"webhook_event","webhook":{"id":"1234567890"},"trigger":"FILE.UPLOADED","source":{"id":"1234567890","type":"file","name":"Test.txt"}}'
    body_with_japanese: str = '{"webhook":{"id":"1234567890"},"trigger":"FILE.UPLOADED","source":{"id":"1234567890","type":"file","name":"スクリーンショット 2020-08-05.txt"}}'
    body_with_emoji: str = '{"webhook":{"id":"1234567890"},"trigger":"FILE.UPLOADED","source":{"id":"1234567890","type":"file","name":"😀 2020-08-05.txt"}}'
    body_with_carriage_return: str = '{"webhook":{"id":"1234567890"},"trigger":"FILE.UPLOADED","source":{"id":"1234567890","type":"file","name":"test \r"}}'
    headers: Dict[str, str] = {'box-delivery-id': 'f96bb54b-ee16-4fc5-aa65-8c2d9e5b546f', 'box-delivery-timestamp': '2020-01-01T00:00:00-07:00', 'box-signature-algorithm': 'HmacSHA256', 'box-signature-primary': '6TfeAW3A1PASkgboxxA5yqHNKOwFyMWuEXny/FPD5hI=', 'box-signature-secondary': 'v+1CD1Jdo3muIcbpv5lxxgPglOqMfsNHPV899xWYydo=', 'box-signature-version': '1'}
    headers_with_japanese: Dict = {**headers, 'box-signature-primary': 'LV2uCu+5NJtIHrCXDYgZ0v/PP5THGRuegw3RtdnEyuE='}
    headers_with_emoji: Dict = {**headers, 'box-signature-primary': 'xF/SDZosX4le+v4A0Qn59sZhuD1RqY5KRUKzVMSbh0E='}
    headers_with_carriage_return: Dict = {**headers, 'box-signature-primary': 'SVkbKgy3dEEf2PbbzpNu2lDZS7zZ/aboU7HOZgBGrJk='}
    current_datetime: str = date_time_to_string(epoch_seconds_to_date_time(get_epoch_time_in_seconds()))
    future_datetime: str = date_time_to_string(epoch_seconds_to_date_time(get_epoch_time_in_seconds() + 1200))
    past_datetime: str = date_time_to_string(epoch_seconds_to_date_time(get_epoch_time_in_seconds() - 1200))
    headers_with_correct_datetime: Dict = {**headers, 'box-delivery-timestamp': current_datetime, 'box-signature-primary': compute_webhook_signature(body, {**headers, 'box-delivery-timestamp': current_datetime}, primary_key), 'box-signature-secondary': compute_webhook_signature(body, {**headers, 'box-delivery-timestamp': current_datetime}, secondary_key)}
    headers_with_japanese_with_correct_datetime: Dict = {**headers_with_japanese, 'box-delivery-timestamp': current_datetime, 'box-signature-primary': compute_webhook_signature(body_with_japanese, {**headers_with_japanese, 'box-delivery-timestamp': current_datetime}, primary_key), 'box-signature-secondary': compute_webhook_signature(body_with_japanese, {**headers_with_japanese, 'box-delivery-timestamp': current_datetime}, secondary_key)}
    headers_with_future_datetime: Dict = {**headers, 'box-delivery-timestamp': future_datetime, 'box-signature-primary': compute_webhook_signature(body, {**headers, 'box-delivery-timestamp': future_datetime}, primary_key), 'box-signature-secondary': compute_webhook_signature(body, {**headers, 'box-delivery-timestamp': future_datetime}, secondary_key)}
    headers_with_past_datetime: Dict = {**headers, 'box-delivery-timestamp': past_datetime, 'box-signature-primary': compute_webhook_signature(body, {**headers, 'box-delivery-timestamp': past_datetime}, primary_key), 'box-signature-secondary': compute_webhook_signature(body, {**headers, 'box-delivery-timestamp': past_datetime}, secondary_key)}
    headers_with_wrong_signature_version: Dict = {**headers, 'box-signature-version': '2'}
    headers_with_wrong_signature_algorithm: Dict = {**headers, 'box-signature-algorithm': 'HmacSHA1'}
    assert compute_webhook_signature(body, headers, primary_key) == headers.get('box-signature-primary')
    assert compute_webhook_signature(body, headers, secondary_key) == headers.get('box-signature-secondary')
    assert not compute_webhook_signature(body, headers, incorrect_key) == headers.get('box-signature-primary')
    assert compute_webhook_signature(body_with_japanese, headers_with_japanese, primary_key) == headers_with_japanese.get('box-signature-primary')
    assert compute_webhook_signature(body_with_emoji, headers_with_emoji, primary_key) == headers_with_emoji.get('box-signature-primary')
    assert compute_webhook_signature(body_with_carriage_return, headers_with_carriage_return, primary_key) == headers_with_carriage_return.get('box-signature-primary')
    assert WebhooksManager.validate_message(body, headers_with_correct_datetime, primary_key, secondary_key=secondary_key)
    assert WebhooksManager.validate_message(body, headers_with_correct_datetime, primary_key, secondary_key=incorrect_key)
    assert WebhooksManager.validate_message(body, headers_with_correct_datetime, incorrect_key, secondary_key=secondary_key)
    assert WebhooksManager.validate_message(body, headers_with_correct_datetime, incorrect_key, secondary_key=incorrect_key) == False
    assert WebhooksManager.validate_message(body, headers_with_future_datetime, primary_key, secondary_key=secondary_key) == False
    assert WebhooksManager.validate_message(body, headers_with_past_datetime, primary_key, secondary_key=secondary_key) == False
    assert WebhooksManager.validate_message(body, headers_with_wrong_signature_version, primary_key, secondary_key=secondary_key) == False
    assert WebhooksManager.validate_message(body, headers_with_wrong_signature_algorithm, primary_key, secondary_key=secondary_key) == False
    assert WebhooksManager.validate_message(body_with_japanese, headers_with_japanese_with_correct_datetime, primary_key, secondary_key=secondary_key)
    assert WebhooksManager.validate_message(body_with_japanese, headers_with_japanese_with_correct_datetime, primary_key, secondary_key=incorrect_key)
    assert WebhooksManager.validate_message(body_with_japanese, headers_with_japanese_with_correct_datetime, incorrect_key, secondary_key=secondary_key)
    assert WebhooksManager.validate_message(body_with_japanese, headers_with_japanese, primary_key, secondary_key=secondary_key) == False