# WebhooksManager

- [List all webhooks](#list-all-webhooks)
- [Create webhook](#create-webhook)
- [Get webhook](#get-webhook)
- [Update webhook](#update-webhook)
- [Remove webhook](#remove-webhook)
- [Validate a webhook message](#validate-a-webhook-message)

## List all webhooks

Returns all defined webhooks for the requesting application.

This API only returns webhooks that are applied to files or folders that are
owned by the authenticated user. This means that an admin can not see webhooks
created by a service account unless the admin has access to those folders, and
vice versa.

This operation is performed by calling function `get_webhooks`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-webhooks/).

<!-- sample get_webhooks -->

```python
client.webhooks.get_webhooks()
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Webhooks`.

Returns a list of webhooks.

## Create webhook

Creates a webhook.

This operation is performed by calling function `create_webhook`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-webhooks/).

<!-- sample post_webhooks -->

```python
client.webhooks.create_webhook(
    CreateWebhookTarget(id=folder.id, type=CreateWebhookTargetTypeField.FOLDER),
    "https://example.com/new-webhook",
    [CreateWebhookTriggers.FILE_UPLOADED],
)
```

### Arguments

- target `CreateWebhookTarget`
  - The item that will trigger the webhook.
- address `str`
  - The URL that is notified by this webhook.
- triggers `List[CreateWebhookTriggers]`
  - An array of event names that this webhook is to be triggered for.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Webhook`.

Returns the new webhook object.

## Get webhook

Retrieves a specific webhook.

This operation is performed by calling function `get_webhook_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-webhooks-id/).

<!-- sample get_webhooks_id -->

```python
client.webhooks.get_webhook_by_id(webhook.id)
```

### Arguments

- webhook_id `str`
  - The ID of the webhook. Example: "3321123"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Webhook`.

Returns a webhook object.

## Update webhook

Updates a webhook.

This operation is performed by calling function `update_webhook_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-webhooks-id/).

<!-- sample put_webhooks_id -->

```python
client.webhooks.update_webhook_by_id(
    webhook.id, address="https://example.com/updated-webhook"
)
```

### Arguments

- webhook_id `str`
  - The ID of the webhook. Example: "3321123"
- target `Optional[UpdateWebhookByIdTarget]`
  - The item that will trigger the webhook.
- address `Optional[str]`
  - The URL that is notified by this webhook.
- triggers `Optional[List[UpdateWebhookByIdTriggers]]`
  - An array of event names that this webhook is to be triggered for.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Webhook`.

Returns the new webhook object.

## Remove webhook

Deletes a webhook.

This operation is performed by calling function `delete_webhook_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-webhooks-id/).

<!-- sample delete_webhooks_id -->

```python
client.webhooks.delete_webhook_by_id(webhook.id)
```

### Arguments

- webhook_id `str`
  - The ID of the webhook. Example: "3321123"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

An empty response will be returned when the webhook
was successfully deleted.

## Validate a webhook message

Validate a webhook message by verifying the signature and the delivery timestamp

This operation is performed by calling function `validate_message`.

```python
WebhooksManager.validate_message(
    body, headers_with_correct_datetime, primary_key, secondary_key=secondary_key
)
```

### Arguments

- body `str`
  - The request body of the webhook message
- headers `Dict[str, str]`
  - The headers of the webhook message
- primary_key `str`
  - The primary signature to verify the message with
- secondary_key `Optional[str]`
  - The secondary signature to verify the message with
- max_age `Optional[int]`
  - The maximum age of the message in seconds, defaults to 10 minutes

### Returns

This function returns a value of type `bool`.
