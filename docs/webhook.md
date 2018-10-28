Webhooks
========

Webhooks enable you to attach event triggers to Box files and folders. Event triggers monitor events on Box objects and notify your application when they occur. A webhook notifies your application by sending HTTP requests to a URL of your choosing.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Get Information about Webhook](#get-information-about-webhook)
- [List all Webhooks](#list-all-webhooks)
- [Create Webhook](#create-webhook)
- [Delete Webhook](#delete-webhook)
- [Update Webhook](#update-webhook)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get Information about Webhook
-----------------------------

To get a webhook object, first call [`client.webhook(webhook_id)`][webhook] to construct the appropriate [`Webhook`][webhook_class] object, and then calling [`webhook.get(fields=None)`][get] will return the [`Webhook`][webhook_class] object populated with data from the API, leaving the original object unmodified.

```python
webhook = client.webhook('12345').get()
print('Webhooks id is {0} and the address is {1}'.format(webhook.id, webhook.address))
```

[webhook]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.webhook
[webhook_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.webhook.Webhook
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

List all Webhooks
-----------------

To retrieve all webhooks for an enterprise, call [`client.get_webhooks(limit=None, marker=None, fields=None)`][get_webhooks]. This method returns a `BoxObjectCollection` that allows you to iterate over the [`Webhook`][webhook_class] objects in the collection.

```python
webhooks = client.get_webhooks()
for webhook in webhooks:
    print('The webhook id is {0} and the address is {1}'.format(webhook.id, webhook.address))
```

[get_webhooks]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_webhooks
[webhook_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.webhook.Webhook

Create Webhook
--------------

To create a webhook object, call [`client.create_webhook(target_url, name=None, description=None)`][create] will let you create a new webhook object with the specified target url, name, and description. This method will return an updated [`Webhook`][webhook_class] object populated with data from the API, leaving the original object unmodified.

You can create a webhook on either a `file` or a `folder`. For a full list of triggers, see [`here`](https://developer.box.com/v2.0/reference#webhooks-v2)

```python
folder = client.folder('12345')
webhook = client.create_webhook(folder, ['FILE.UPLOADED', 'FILE.PREVIEWED'], 'https://example.com')
print('Webhook id is {0} and the address is {1}'.format(webhook.id, webhook.address))
```

[create]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_webhook
[webhook_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.webhook.Webhook

Delete Webhook
--------------

To delete a webhook, call [`webhook.delete()`][delete]. This method returns `True` to indicate that the deletion was successful.

```python
client.webhook('12345').delete()
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete


Update Webhook
--------------

To update a webhook object, first call [`client.webhook(webhook_id)`][webhook] to construct the appropriate [`Webhook`][webhook_class] object, and then calling [`webhook.update_info(data)`][update_info] with a `dict` of properties to update on the webhook. This method returns a new updated [`Webhook`][webhook_class] object, leaving the original object unmodified.

```python
update_object = {
    triggers: ['FILE.COPIED'],
    address: 'https://newexample.com',
}
webhook = client.webhook('12345').update_info(update_object)
print('Updated the webhook info for triggers: {0} and address: {1}'.format(webhook.triggers, webhook.address))
```

[webhook]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_webhook
[webhook_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.webhook.Webhook

