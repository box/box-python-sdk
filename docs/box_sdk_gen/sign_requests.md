# SignRequestsManager

- [Cancel Box Sign request](#cancel-box-sign-request)
- [Resend Box Sign request](#resend-box-sign-request)
- [Get Box Sign request by ID](#get-box-sign-request-by-id)
- [List Box Sign requests](#list-box-sign-requests)
- [Create Box Sign request](#create-box-sign-request)

## Cancel Box Sign request

Cancels a sign request.

This operation is performed by calling function `cancel_sign_request`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-sign-requests-id-cancel/).

<!-- sample post_sign_requests_id_cancel -->

```python
client.sign_requests.cancel_sign_request(created_sign_request.id)
```

### Arguments

- sign_request_id `str`
  - The ID of the signature request. Example: "33243242"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `SignRequest`.

Returns a Sign Request object.

## Resend Box Sign request

Resends a signature request email to all outstanding signers.

This operation is performed by calling function `resend_sign_request`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-sign-requests-id-resend/).

_Currently we don't have an example for calling `resend_sign_request` in integration tests_

### Arguments

- sign_request_id `str`
  - The ID of the signature request. Example: "33243242"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the API call was successful.
The email notifications will be sent asynchronously.

## Get Box Sign request by ID

Gets a sign request by ID.

This operation is performed by calling function `get_sign_request_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-sign-requests-id/).

<!-- sample get_sign_requests_id -->

```python
client.sign_requests.get_sign_request_by_id(created_sign_request.id)
```

### Arguments

- sign_request_id `str`
  - The ID of the signature request. Example: "33243242"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `SignRequest`.

Returns a signature request.

## List Box Sign requests

Gets signature requests created by a user. If the `sign_files` and/or
`parent_folder` are deleted, the signature request will not return in the list.

This operation is performed by calling function `get_sign_requests`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-sign-requests/).

<!-- sample get_sign_requests -->

```python
client.sign_requests.get_sign_requests()
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- senders `Optional[List[str]]`
  - A list of sender emails to filter the signature requests by sender. If provided, `shared_requests` must be set to `true`.
- shared_requests `Optional[bool]`
  - If set to `true`, only includes requests that user is not an owner, but user is a collaborator. Collaborator access is determined by the user access level of the sign files of the request. Default is `false`. Must be set to `true` if `senders` are provided.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `SignRequests`.

Returns a collection of sign requests.

## Create Box Sign request

Creates a signature request. This involves preparing a document for signing and
sending the signature request to signers.

This operation is performed by calling function `create_sign_request`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-sign-requests/).

<!-- sample post_sign_requests -->

```python
client.sign_requests.create_sign_request([SignRequestCreateSigner(email=signer_email, suppress_notifications=True, declined_redirect_url='https://www.box.com', embed_url_external_user_id='123', is_in_person=False, login_required=False, password='password', role=SignRequestCreateSignerRoleField.SIGNER)], source_files=[FileBase(id=file_to_sign.id)], parent_folder=FolderMini(id=destination_folder.id), is_document_preparation_needed=False, redirect_url='https://www.box.com', declined_redirect_url='https://www.box.com', are_text_signatures_enabled=True, email_subject='Sign this document', email_message='Please sign this document', are_reminders_enabled=True, name='Sign Request', prefill_tags=[SignRequestPrefillTag(date_value=date_from_string('2035-01-01'), document_tag_id='0')], days_valid=30, external_id='123', external_system_name='BoxSignIntegration')
```

### Arguments

- source_files `Optional[List[FileBase]]`
  - List of files to create a signing document from. This is currently limited to ten files. Only the ID and type fields are required for each file.
- signature_color `Optional[CreateSignRequestSignatureColor]`
  - Force a specific color for the signature (blue, black, or red).
- signers `List[SignRequestCreateSigner]`
  - Array of signers for the signature request. 35 is the max number of signers permitted. **Note**: It may happen that some signers belong to conflicting [segments](r://shield-information-barrier-segment-member) (user groups). This means that due to the security policies, users are assigned to segments to prevent exchanges or communication that could lead to ethical conflicts. In such a case, an attempt to send the sign request will result in an error. Read more about [segments and ethical walls](https://support.box.com/hc/en-us/articles/9920431507603-Understanding-Information-Barriers#h_01GFVJEHQA06N7XEZ4GCZ9GFAQ).
- parent_folder `Optional[FolderMini]`
- is_document_preparation_needed `Optional[bool]`
  - Indicates if the sender should receive a `prepare_url` in the response to complete document preparation using the UI.
- redirect_url `Optional[str]`
  - When specified, the signature request will be redirected to this url when a document is signed.
- declined_redirect_url `Optional[str]`
  - The uri that a signer will be redirected to after declining to sign a document.
- are_text_signatures_enabled `Optional[bool]`
  - Disables the usage of signatures generated by typing (text).
- email_subject `Optional[str]`
  - Subject of sign request email. This is cleaned by sign request. If this field is not passed, a default subject will be used.
- email_message `Optional[str]`
  - Message to include in sign request email. The field is cleaned through sanitization of specific characters. However, some html tags are allowed. Links included in the message are also converted to hyperlinks in the email. The message may contain the following html tags including `a`, `abbr`, `acronym`, `b`, `blockquote`, `code`, `em`, `i`, `ul`, `li`, `ol`, and `strong`. Be aware that when the text to html ratio is too high, the email may end up in spam filters. Custom styles on these tags are not allowed. If this field is not passed, a default message will be used.
- are_reminders_enabled `Optional[bool]`
  - Reminds signers to sign a document on day 3, 8, 13 and 18. Reminders are only sent to outstanding signers.
- name `Optional[str]`
  - Name of the signature request.
- prefill_tags `Optional[List[SignRequestPrefillTag]]`
  - When a document contains sign-related tags in the content, you can prefill them using this `prefill_tags` by referencing the 'id' of the tag as the `external_id` field of the prefill tag.
- days_valid `Optional[int]`
  - Set the number of days after which the created signature request will automatically expire if not completed. By default, we do not apply any expiration date on signature requests, and the signature request does not expire.
- external_id `Optional[str]`
  - This can be used to reference an ID in an external system that the sign request is related to.
- template_id `Optional[str]`
  - When a signature request is created from a template this field will indicate the id of that template.
- external_system_name `Optional[str]`
  - Used as an optional system name to appear in the signature log next to the signers who have been assigned the `embed_url_external_id`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `SignRequest`.

Returns a Box Sign request object.
