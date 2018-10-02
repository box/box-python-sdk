Webhooks
========

Webhooks enable you to attach event triggers to Box files and folders. Event triggers monitor events on Box objects and notify your application when they occur. A webhook notifies your application by sending HTTP requests to a URL of your choosing.

Get Information about Webhook
-----------------------------

To retrieve information about a webhook, use `webhook.get(fields=None)`

```python
webhook_info = client.webhook('1234').get()
```

List all Webhooks
-----------------

To retrieve an iterable of all webhooks in the enterprise, use `client.get_webhooks(limit=None, marker=None, fields=None)`

```python
webhooks = client.get_webhooks()
for webhook in webhooks:
    # Do something
```

Create Webhook
--------------

To create a webhook on a specified target, use `client.create_webhook(target, triggers, address)`

You can create a webhook on either a `file` or a `folder`. For a full list of triggers, see [here](https://developer.box.com/v2.0/reference#webhooks-v2)

```python
folder = client.folder('1111')
created_webhook = client.create_webhook(folder, ['FILE.UPLOADED', 'FILE.PREVIEWED'], 'https://example.com')
```

Delete Webhook
--------------

To delete a webhook, use `webhook.delete()`

```python
client.webhook('1234').delete()
```

Update Webhook
--------------

To update a webhook, use `webhook.update_info(data)`

```python
update_object = {
    triggers: ['FILE.COPIED'],
    address: 'https://newexample.com',
}
updated_webhook = client.webhook('1234').update_info(update_object)
```
