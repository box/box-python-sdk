Sign Templates
==============

Sign Templates are reusable templates that can be used to create Sign Requests. For now, Sign Templates can only be created through the Box web application.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Get All Sign Templates](#get-all-sign-templates)
- [Get Sign Template by ID](#get-sign-template-by-id)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get All Sign Templates
----------------------

Calling the [`client.get_sign_templates()`][get-all-sign-templates] method will return an iterable that will page through all the Sign Templates. This method offers `limit` parameter. The `limit` parameter specifies the maximum number of items to be returned in a single response.

<!-- sample get_sign_templates -->
```python
sign_templates = client.get_sign_templates()
for sign_template in sign_templates:
    print(f'(Sign Template ID: {sign_template.id})')
```

[get-all-sign-templates]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_sign_templates

Get Sign Template by ID
-----------------------

Calling the [`client.get_sign_template(template_id)`][get-sign-template] method will return a Sign Template object.

<!-- sample get_sign_template -->
```python
sign_template = client.get_sign_template('12345')
print(f'(Sign Template ID: {sign_template.id})')
```

[get-sign-template]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_sign_template
