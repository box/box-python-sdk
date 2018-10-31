Terms of Service
================

Terms of Service allows Box Admins to configure a custom Terms of Service for end users to
accept/re-accept/decline for custom applications

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Create a Terms of Service](#create-a-terms-of-service)
- [Edit a Terms of Service](#edit-a-terms-of-service)
- [Get Terms of Service](#get-terms-of-service)
- [List Terms of Service](#list-terms-of-service)
- [Update User Status on Terms of Service](#update-user-status-on-terms-of-service)
- [Accept or Decline a Terms of Service](#accept-or-decline-a-terms-of-service)
- [Get User Status for a Terms of Service](#get-user-status-for-a-terms-of-service)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Create a Terms of Service
-------------------------

A terms of service can be created in an enterprise. Please note that only two can be created. One external
and one managed. If a terms of service already exists please use the update call to change the current
terms of service.

You can create a custom terms of service by using `client.create_terms_of_service(status, tos_type, text)`.

```python
from boxsdk.object.terms_of_service import TermsOfServiceType, TermsOfServiceStatus
terms_of_service = client.create_terms_of_service(TermsOfServiceStatus.ENABLED, TermsOfServiceType.MANAGED, 'Example Text')
```

Edit a Terms of Service
-----------------------

To update a terms of service, use `terms_of_service.update_info()`.

```python
tos_id = '1234'
update_object = {'text': 'New Text'}
updated_tos = client.terms_of_service(tos_id).update_info(update_object)
```

Get Terms of Service
--------------------

To retrieve information about a terms of service, use `terms_of_service.get()`.

```python
tos_id = '1234'
terms_of_service = client.terms_of_service(tos_id).get()
```

List Terms of Service
---------------------

You can retrieve an iterable of terms of service in your enterprise by calling `client.get_terms_of_services(tos_type=None, limit=None)`.

```python
terms_of_services = client.get_terms_of_services()
for terms_of_service in terms_of_services:
    # Do something
```

Update User Status on Terms of Service
--------------------------------------

To update user status on a terms of service call the `terms_of_service_user_status.update_info(update_object)` method.

```python
user_status = client.terms_of_service_user_status('12345').update_info({'is_accepted': True})
```

It is important to note that this will accept or decline a custom terms of service for a user. For a user that has taken action in this terms of service, this will update their status. If the user has never taken action on this terms of service then this will return a 404 Not Found Error.

Accept or Decline a Terms of Service
------------------------------------

To create user/terms of service association and accept/decline call the  `terms_of_service.set_user_status(is_accepted, user=None)` method.

```python
user = client.user('22222')
user_status = client.terms_of_service('11111').set_user_status(is_accepted=True, user=user)
```

It is important to note that regardless of whether the user has taken action on this terms of service. This will create and update the user status on the terms of service.

Get User Status for a Terms of Service
-------------------------------------

You can retrieve a terms of service status for a user by calling
`terms_of_service.get_user_status(user)`.

```python
user = client.user('11111')
user_status = client.terms_of_service('1234').get_user_status(user)
```