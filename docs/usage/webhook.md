Webhooks
========

Webhooks enable you to attach event triggers to Box files and folders. Event triggers monitor events on Box objects and 
notify your application when they occur. A webhook notifies your application by sending HTTP requests to a URL of your 
choosing.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Get Information about Webhook](#get-information-about-webhook)
- [List all Webhooks](#list-all-webhooks)
- [Create Webhook](#create-webhook)
- [Delete Webhook](#delete-webhook)
- [Update Webhook](#update-webhook)
- [Validate Webhook Message](#validate-webhook-message)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get Information about Webhook
-----------------------------

To get a webhook object, first call [`client.webhook(webhook_id)`][webhook] to construct the appropriate 
[`Webhook`][webhook_class] object, and then calling [`webhook.get(fields=None)`][get] will return the 
[`Webhook`][webhook_class] object populated with data from the API.

```python
webhook = client.webhook(webhook_id='12345').get()
print('Webhooks ID is {0} and the address is {1}'.format(webhook.id, webhook.address))
```

[webhook]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.webhook
[webhook_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.webhook.Webhook
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

List all Webhooks
-----------------

To retrieve all webhooks for an enterprise, call [`client.get_webhooks(limit=None, marker=None, fields=None)`][get_webhooks]. 
This method returns a `BoxObjectCollection` that allows you to iterate over the [`Webhook`][webhook_class] objects in 
the collection.

```python
webhooks = client.get_webhooks()
for webhook in webhooks:
    print('The webhook ID is {0} and the address is {1}'.format(webhook.id, webhook.address))
```

[get_webhooks]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_webhooks
[webhook_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.webhook.Webhook

Create Webhook
--------------

To create a webhook object, call [`client.create_webhook(target_url, name=None, description=None)`][create] will let 
you create a new webhook object with the specified target url, name, and description. This method will return an updated 
[`Webhook`][webhook_class] object populated with data from the API, leaving the original object unmodified.

```python
folder = client.folder(folder_id='12345')
webhook = client.create_webhook(folder, ['FILE.UPLOADED', 'FILE.PREVIEWED'], 'https://example.com')
print('Webhook ID is {0} and the address is {1}'.format(webhook.id, webhook.address))
```

[create]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_webhook
[webhook_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.webhook.Webhook

Delete Webhook
--------------

To delete a webhook, call [`webhook.delete()`][delete]. This method returns `True` to indicate that the deletion was 
successful.

```python
client.webhook(webhook_id='12345').delete()
print('The webhook was successfully deleted!')
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete


Update Webhook
--------------

To update a webhook object, first call [`client.webhook(webhook_id)`][webhook] to construct the appropriate [`Webhook`][webhook_class] 
object, and then calling [`webhook.update_info(data)`][update_info] with a `dict` of properties to update on the 
webhook. This method returns a new updated [`Webhook`][webhook_class] object, leaving the original object unmodified.

```python
update_object = {
    'triggers': ['FILE.COPIED'],
    'address': 'https://newexample.com',
}
webhook = client.webhook(webhook_id='12345').update_info(update_object)
print('Updated the webhook info for triggers: {0} and address: {1}'.format(webhook.triggers, webhook.address))
```

[webhook]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_webhook
[webhook_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.webhook.Webhook
[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info

Validate Webhook Message
------------------------

When you receive a webhook message from Box, you should validate it by calling 
[`Webhook.validate_message(body, headers, primary_key, secondary_key)`][validate_webhook]. This will protect your
application against attacks. Verification ensures that the notifications were actually sent by Box and not by a
malicious party and that the contents of the notification haven't been changed.

```python
body = b'{"webhook":{"id":"1234567890"},"trigger":"FILE.UPLOADED","source":{"id":"1234567890","type":"file","name":"Test.txt"}}'
headers = {
    'box-delivery-id': 'f96bb54b-ee16-4fc5-aa65-8c2d9e5b546f',
    'box-delivery-timestamp': '2020-01-01T00:00:00-07:00',
    'box-signature-algorithm': 'HmacSHA256',
    'box-signature-primary': '4KvFa5/unRL8aaqOlnbInTwkOmieZkn1ZVzsAJuRipE=',
    'box-signature-secondary': 'yxxwBNk7tFyQSy95/VNKAf1o+j8WMPJuo/KcFc7OS0Q=',
    'box-signature-version': '1',
}
is_validated = Webhook.validate_message(body, headers, primary_key, secondary_key)
print('The webhook message is validated to: {0}'.format(is_validated))
```

[validated_webhook]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.webhook.Webhook.validate_message
