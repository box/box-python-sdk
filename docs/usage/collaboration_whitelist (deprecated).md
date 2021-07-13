Collaboration Whitelist
=======================

The Collaboration Whitelist API allows you to manage a set of approved domains (i.e. a whitelist) that can collaborate
with your enterprise. You can also manage whether the whitelisted domains are approved for outbound or inbound
collaboration.

It is important to note that the collaboration whitelist functionality is only available to customers with Box Governance.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [List Collaboration Whitelist Entries](#list-collaboration-whitelist-entries)
- [Get Information for Collaboration Whitelist Entry](#get-information-for-collaboration-whitelist-entry)
- [Whitelist a Domain for Collaboration](#whitelist-a-domain-for-collaboration)
- [Remove a Domain from Whitelist](#remove-a-domain-from-whitelist)
- [List Exempt Users](#list-exempt-users)
- [Get Exempt User Information](#get-exempt-user-information)
- [Exempt User from Whitelist](#exempt-user-from-whitelist)
- [Remove User Exemption](#remove-user-exemption)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

List Collaboration Whitelist Entries
------------------------------------

To retrieve a list of collaboration whitelist entries, call
[`collaboration_whitelist.get_entries(limit=None, marker=None, fields=None)`][get_entries].  This method returns a
`BoxObjectCollection` which can iterate over the [`CollaborationWhitelistEntry`][entry_class]
objects in the collection.

<!-- sample get_collaboration_whitelist_entries -->
```python
whitelist_entries = client.collaboration_whitelist().get_entries()
for entry in whitelist_entries:
    direction = entry.direction if entry.direction != 'both' else 'bidirectional'
    print('Domain {0} is whitelisted for {1} collaboration'.format(entry.domain, direction))
```

[get_entries]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_whitelist.CollaborationWhitelist.get_entries
[entry_class]:  https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_whitelist_entry.CollaborationWhitelistEntry

Get Information for Collaboration Whitelist Entry
-------------------------------------------------

To get information about a collaboration whitelist entry, use [`collaboration_whitelist_entry.get(fields=None)`][get].
This method returns a [`CollaborationWhitelistEntry`][entry_class] object with fields populated by data form the API.

<!-- sample get_collaboration_whitelist_entries_id -->
```python
whitelist_entry = client.collaboration_whitelist_entry(entry_id='11111').get()
```

[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Whitelist a Domain for Collaboration
------------------------------------

To whitelist a domain for collaboration, call [`collaboration_whitelist.add_domain(domain, direction)`][add_domain] with
the domain to whitelist and the direction(s) collaboration should be allowed in.  This method returns a
[`CollaborationWhitelistEntry`][entry_class] object representing the newly-whitelisted domain.

You can determine the direction of the whitelist by passing in 'outbound', 'inbound', or 'both'. Outbound collaboration
is defined as a user in your enterprise collaborating on content owned by someone outside your enterprise. Inbound
collaboration is defined as a user outside of your enterprise collaborating on content owned by your enterprise.

<!-- sample post_collaboration_whitelist_entries -->
```python
from boxsdk.object.collaboration_whitelist import WhitelistDirection
domain = 'example.com'
whitelist_entry = client.collaboration_whitelist().add_domain(domain, direction=WhitelistDirection.INBOUND)
```

[add_domain]:  https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_whitelist.CollaborationWhitelist.add_domain

Remove a Domain from Whitelist
------------------------------

To remove a collaboration whitelisted domain, call [`collaboration_whitelist_entry.delete()`][delete].  This will remove
the domain from the whitelist, restricting collaboration to and from users in that domain.  This method returns `True`
to indicate that deletion was successful.

<!-- sample delete_collaboration_whitelist_entries_id -->
```python
client.collaboration_whitelist_entry(entry_id='11111').delete()
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete

List Exempt Users
-----------------

To get all exempt users from the collaboration whitelist, call
[`collaboration_whitelist.get_exemptions(limit=None, marker=None, fields=None)`][get_exemptions].  This method returns
a `BoxObjectCollection` that allows you to iterate over each
[`CollaborationWhitelistExemptTarget`][exemption_class] in the collection.

<!-- sample get_collaboration_whitelist_exempt_targets -->
```python
exemptions = client.collaboration_whitelist().get_exemptions()
for exemption in exemptions:
    print('{0} (ID: {1}) is exempt from the collaboration whitelist'.format(exemption.user.name, exemption.user.id))
```

[get_exemptions]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_whitelist.CollaborationWhitelist.get_exemptions
[exemption_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_whitelist_exempt_target.CollaborationWhitelistExemptTarget

Get Exempt User Information
---------------------------

To get information about an exempted user, call [`collaboration_whitelist_exempt_target.get(fields=None)`][get].  This
method will return a [`CollaborationWhitelistExemptTarget][exemption_class] with fields populated by data from the API.

<!-- sample get_collaboration_whitelist_exempt_targets_id -->
```python
exemption_id = '11111'
exemption = client.collaboration_whitelist_exempt_target(exemption_id).get()
```

Exempt User from Whitelist
--------------------------

To exempt a user from the collaboration whitelist, call [`collaboration_whitelist.add_exemption(user)`][add_exemption]
with the [`User`][user_class] to exempt from the whitelist.  This user will no longer be subject to the collaboration
whitelist, and will be permitted to collaborate with users from any other domain.  This method returns a
[`CollaborationWhitelistExemptTarget`][exemption_class] object representing the exempted user.

<!-- sample post_collaboration_whitelist_exempt_targets -->
```python
user = client.user(user_id='11111')
exemption = client.collaboration_whitelist().add_exemption(user)
```

[add_exemption]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_whitelist.CollaborationWhitelist.add_exemption
[user_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User

Remove User Exemption
---------------------

To remove a user exemption from the collaboration whitelist, call
[`collaboration_whitelist_exempt_target.delete()`][delete].  This will remove the exemption and make the user subject to
the collaboration whitelist again.  This method returns `True` to indicate that deletion was successful.

<!-- sample delete_collaboration_whitelist_exempt_targets_id -->
```python
client.collaboration_whitelist_exempt_target(exemption_id='22222').delete()
```
