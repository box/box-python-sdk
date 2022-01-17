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
- [Accept or Decline a Terms of Service](#accept-or-decline-a-terms-of-service)
- [Get User Status for a Terms of Service](#get-user-status-for-a-terms-of-service)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Create a Terms of Service
-------------------------

A Terms of Service can be created in an enterprise. Please note that only two can be created. One external
and one managed. If a terms of service already exists please use the update call to change the current
terms of service.

To create a Terms of Service object, calling [`client.create_terms_of_service(status, tos_type, text)`][create] will let 
you create a new [`TermsOfService`][terms_of_service_class] object with the specified status, type, and text. This 
method will return a newly created [`TermsOfService`][terms_of_service_class] object populated with data from the API.

<!-- sample post_terms_of_services -->
```python
from boxsdk.object.terms_of_service import TermsOfServiceType, TermsOfServiceStatus
terms_of_service = client.create_terms_of_service(TermsOfServiceStatus.ENABLED,TermsOfServiceType.MANAGED, 'Example Text')
print(f'Terms of Service status is {terms_of_service.status} and the message is {terms_of_service.text}')
```

[create]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_terms_of_service
[terms_of_service_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.terms_of_service.TermsOfService

Edit a Terms of Service
-----------------------

To update a terms of service object, first call [`terms_of_service.update_info(data=update_object)`][update_info] with
a `dict` of properties to update on the terms of service. This method returns a newly updated [`TermsOfService`][terms_of_service] 
object, leaving the original object unmodified.

<!-- sample put_terms_of_services_id -->
```python
update_object = {'text': 'New Text'}
updated_tos = client.terms_of_service(tos_id='12345').update_info(data=update_object)
print(f'The updated message for your custom terms of service is {updated_tos.text} with ID {updated_tos.id}')
```

[terms_of_service]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.terms_of_service
[terms_of_service_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.terms_of_service.TermsOfService
[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info

Get Terms of Service
--------------------

To get a terms of service object, call [`client.terms_of_service(service_id)`][terms_of_service] to construct the 
appropriate [`TermsOfService`][terms_of_service_class], and then calling [`terms_of_service.get(*, fields=None, headers=None, **kwargs)`][get] 
will return the [`TermsOfService`][terms_of_service_class] object populated with data from the API.

<!-- sample get_terms_of_services_id -->
```python
terms_of_service = client.terms_of_service(tos_id='12345').get()
print(f'Terms of Service ID is {terms_of_service.id} and the message is {terms_of_service.text}')
```

[terms_of_service]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.terms_of_service
[terms_of_service_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.terms_of_service.TermsOfService
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

List Terms of Service
---------------------

To retrieve all terms of service for an enterprise, call 
[`client.get_terms_of_services(limit=None, marker=None, fields=None)`][get_terms_of_services]. This method returns a 
`BoxObjectCollection` that allows you to iterate over the [`TermOfService`][terms_of_service_class] objects in the 
collection.

<!-- sample get_terms_of_services -->
```python
terms_of_services = client.get_terms_of_services()
for terms_of_service in terms_of_services:
    print(f'Terms of Service ID is {terms_of_service.id} and the message is {terms_of_service.text}')
```

[get_terms_of_services]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.terms_of_service

Accept or Decline a Terms of Service
------------------------------------

To accept or decline a terms of service, calling [`terms_of_service.set_user_status(is_accepted, user)`][set_user_status] 
will allow you to create a newly updated [`TermsOfServiceUserStatus`][terms_of_service_user_status_class] object 
populated with data from the API, leaving the original object umodified if a [`TermsOfService`][terms_of_service_class] 
object already exists for a user. If the user does not have a [`TermsOfService`][terms_of_service_class] object 
assigned then [`terms_of_service.set_user_status(is_accepted, user)`][set_user_status] will create a new 
[`TermsOfServiceUserStatus`][terms_of_service_user_status_class] object populated with data from the API.

<!-- sample post_terms_of_service_user_statuses -->
```python
user = client.user(user_id='22222')
user_status = client.terms_of_service(tos_id='12345').set_user_status(is_accepted=True, user=user)
print(f'User status ID is {user_status.id} and the accepted status is {user_status.is_accepted}')
```

It is important to note that regardless of whether the user has taken action on this terms of service. This will create 
and update the user status on the terms of service.

Note that this example will make multiple API calls, if you know that your user has already accepted or decline a 
Terms of Service and you wish to change their status, call [`terms_of_service_user_status.update_info(data=data_to_update)`][update_info] 
with a `dict` of properties to update on the terms of service user status. This method returns a newly updated 
[`TermsOfServiceUserStatus`][terms_of_service_user_status_class] object, leaving the original object unmodified.

<!-- sample put_terms_of_service_user_statuses_id -->
```python
user_status = client.terms_of_service_user_status(tos_user_status_id='12345').update_info(data={'is_accepted': True})
print(f'Terms of Service User Status ID is {user_status.id} and the accepted status is {user_status.is_accepted}')
```

It is important to note that this will accept or decline a custom terms of service for a user. For a user that has taken 
action in this terms of service, this will update their status. If the user has never taken action on this terms of 
service then this will return a 404 Not Found Error.

[terms_of_service_user_status_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.terms_of_service_user_status.TermsOfServiceUserStatus
[user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.user
[set_user_status]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.terms_of_service.TermsOfService.set_user_status
[terms_of_service_user_status]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.terms_of_service_user_status
[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info

Get User Status for a Terms of Service
-------------------------------------

To get a terms of service user status object, first call 
[`client.terms_of_service_user_status(status_id)`][terms_of_service_user_status] 
to construct the appropriate [`TermsOfServiceUserStatus`][terms_of_service_user_status_class] object. Then calling 
[`client.user(user_id)`][user] to construct the user you wish to retrieve a 
[`TermsOfServiceUserStatus`][terms_of_service_user_status_class] object for. Finally, calling 
[`terms_of_service_user_status.get(*, fields=None, headers=None, **kwargs)`][get] will return the 
[`TermsOfServiceUserStatus`][terms_of_service_user_status_class] object populated with data from the API.

<!-- sample get_terms_of_service_user_statuses_id -->
```python
user = client.user(user_id='11111')
user_status = client.terms_of_service(tos_id='12345').get_user_status(user)
print(f'User status ID is {user_status.id} and the accepted status is {user_status.is_accepted}')
```

[user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.user
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get
