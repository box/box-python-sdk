Terms of Service
================

Terms of Service allows Box Admins to configure a custom Terms of Service for end users to
accept/re-accept/decline for custom applications


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

Accept or Decline a Terms of Service for New User
-------------------------------------------------

For new users you can accept or decline a terms of service by calling `terms_of_service.accept(user=None)` or `terms_of_service.reject(user=None)`.

```python
user = client.user('1234')
user_status = client.terms_of_service.accept(user)
```

You can only create a new user status on a terms of service if the user has never accepted/declined a terms of service.
If they have then you will need to make the update call.

Accept or Decline a Terms of Service for Existing User
------------------------------------------------------

For an existing user you can accept or decline a terms of service by calling `terms_of_service_user_status.accept()` to accept or  `terms_of_service_user_status.reject()` to reject

```python
accepted_user_status = client.terms_of_service_user_status('1234').accept()
```

```python
rejected_user_status = client.terms_of_service_user_status('1234').reject()
```

Get User Status for a Terms of Service
-------------------------------------

You can retrieve an iterable of terms of service status for a user by calling
`terms_of_service.get_user_status(user_id=None)`.

```python
user_id = '5678'
user_status = client.terms_of_service('1234').get_user_status(user_id)
```