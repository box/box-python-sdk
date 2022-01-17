Sign Requests
==================

Sign Requests are used to request e-signatures on documents from signers.  
A Sign Request can refer to one or more Box Files and can be sent to one or more Box Sign Request Signers.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Create Sign Request](#create-sign-request)
- [Get all Sign Requests](#get-all-sign-requests)
- [Get Sign Request by ID](#get-sign-request-by-id)
- [Cancel Sign Request](#cancel-sign-request)
- [Resend Sign Request](#resend-sign-request)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Create Sign Request
------------------------

The [`client.create_sign_request(files, signers, parent_folder_id, prefill_tags=None, are_reminders_enabled=None, are_text_signatures_enabled=None, days_valid=None, email_message=None, email_subject=None, external_id=None, is_document_preparation_needed=None)`][create-sign-request]
method will create a Sign Request. You need to provide at least one file (from which the signing document will be created) and at least one signer to receive the Sign Request.

<!-- sample post_sign_requests -->
```python
from boxsdk.object.sign_request import SignRequest

source_file = {
    'id': '12345',
    'type': 'file'
}
files = [source_file]

signer = {
    'name': 'John Doe',
    'email': 'signer@mail.com' 
}
signers = [signer]

parent_folder_id = '123456789'
new_sign_request = client.create_sign_request(files, signers, parent_folder_id)
print(f'(Sign Request ID: {new_sign_request.id})')
```

If you set ```isDocumentPreparationNeeded``` flag to true, you need to visit ```prepareUrl``` before the Sign Request will be sent. 
For more information on ```isDocumentPreparationNeeded``` and the other parameters available, please refer to the [developer documentation](https://developer.box.com/guides/sign-request/).

[create-sign-request]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_sign_request

Get All Sign Requests
------------------------

Calling the [`client.get_sign_requests()`][get-all-sign-requests]
will return an iterable that will page through all the Sign Requests. This method offers `limit` and `fields` parameters. The `limit` parameter specifies the maximum number of items to be returned in a single response. The `fields` parameter is used to specify what additional properties should be returned on the return object. For more information on what `fields` are available, please refer to the [developer documentation](https://developer.box.com/guides/sign-request/).

<!-- sample get_sign_requests -->
```python
from boxsdk.object.sign_request import SignRequest

sign_requests = client.get_sign_requests()
for sign_request in sign_requests:
    print(f'(Sign Request ID: {sign_request.id})')
```

[get-all-sign-requests]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_sign_requests

Get Sign Request by ID
------------------------

Calling [`client.sign_request(sign_request_id)`][get-sign-request-by-id] will return an object
containing information about the Sign Request.
The `fields` parameter is used to specify what additional properties should be returned in the return object.

<!-- sample get_sign_requests_id -->
```python
from boxsdk.object.sign_request import SignRequest

sign_request = client.sign_request(sign_request_id='12345').get()
print(f'Sign Request ID is {sign_request.id}')
```

[get-sign-request-by-id]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.sign_request

Cancel Sign Request
------------------------

Calling [`sign_requests.cancel()`][cancel-sign-request] will cancel a created Sign Request.

<!-- sample post_sign_requests_id_cancel -->
```python
from boxsdk.object.sign_request import SignRequest

sign_request = client.sign_request(sign_request_id='12345')
cancelled_sign_request = sign_request.cancel()
print(f'Cancelled Sign Request status is {cancelled_sign_request.status}')
```

[cancel-sign-request]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy.SignRequest.cancel

Resend Sign Request
------------------------

Calling [`sign_requests.resend()`][resend-sign-request] will resend a Sign Request to all signers that have not signed it yet.
There is an 10-minute cooling-off period between re-sending reminder emails.

<!-- sample post_sign_requests_id_resend -->
```python
from boxsdk.object.sign_request import SignRequest

sign_request = client.sign_request(sign_request_id='12345')
sign_request.resend()
```

[resend-sign-request]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy.SignRequest.resend
