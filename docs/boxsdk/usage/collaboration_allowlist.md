Collaboration Allowlist
=======================

The Collaboration Allowlist API allows you to manage a set of approved domains (i.e. a allowlist) that can collaborate
with your enterprise. You can also manage whether the allowlisted domains are approved for outbound or inbound
collaboration.

It is important to note that the collaboration allowlist functionality is only available to customers with Box Governance.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [List Collaboration Allowlist Entries](#list-collaboration-allowlist-entries)
- [Get Information for Collaboration Allowlist Entry](#get-information-for-collaboration-allowlist-entry)
- [Allowlist a Domain for Collaboration](#allowlist-a-domain-for-collaboration)
- [Remove a Domain from Allowlist](#remove-a-domain-from-allowlist)
- [List Exempt Users](#list-exempt-users)
- [Get Exempt User Information](#get-exempt-user-information)
- [Exempt User from Allowlist](#exempt-user-from-allowlist)
- [Remove User Exemption](#remove-user-exemption)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

List Collaboration Allowlist Entries
------------------------------------

To retrieve a list of collaboration allowlist entries, call
[`collaboration_allowlist.get_entries(limit=None, marker=None, fields=None)`][get_entries].  This method returns a
`BoxObjectCollection` which can iterate over the [`CollaborationAllowlistEntry`][entry_class]
objects in the collection.

<!-- sample get_collaboration_allowlist_entries -->
```python
allowlist_entries = client.collaboration_allowlist().get_entries()
for entry in allowlist_entries:
    direction = entry.direction if entry.direction != 'both' else 'bidirectional'
    print(f'Domain {entry.domain} is allowlisted for {direction} collaboration')
```

[get_entries]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_allowlist.CollaborationAllowlist.get_entries
[entry_class]:  https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_allowlist_entry.CollaborationAllowlistEntry

Get Information for Collaboration Allowlist Entry
-------------------------------------------------

To get information about a collaboration allowlist entry, use [`collaboration_allowlist_entry.get(*, fields=None, headers=None, **kwargs)`][get].
This method returns a [`CollaborationAllowlistEntry`][entry_class] object with fields populated by data form the API.

<!-- sample get_collaboration_allowlist_entries_id -->
```python
allowlist_entry = client.collaboration_allowlist_entry(entry_id='11111').get()
```

[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Allowlist a Domain for Collaboration
------------------------------------

To allowlist a domain for collaboration, call [`collaboration_allowlist.add_domain(domain, direction)`][add_domain] with
the domain to allowlist and the direction(s) collaboration should be allowed in.  This method returns a
[`CollaborationAllowlistEntry`][entry_class] object representing the newly-allowlisted domain.

You can determine the direction of the allowlist by passing in 'outbound', 'inbound', or 'both'. Outbound collaboration
is defined as a user in your enterprise collaborating on content owned by someone outside your enterprise. Inbound
collaboration is defined as a user outside of your enterprise collaborating on content owned by your enterprise.

<!-- sample post_collaboration_allowlist_entries -->
```python
from boxsdk.object.collaboration_allowlist import AllowlistDirection
domain = 'example.com'
allowlist_entry = client.collaboration_allowlist().add_domain(domain, direction=AllowlistDirection.INBOUND)
```

[add_domain]:  https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_allowlist.CollaborationAllowlist.add_domain

Remove a Domain from Allowlist
------------------------------

To remove a collaboration allowlisted domain, call [`collaboration_allowlist_entry.delete()`][delete].  This will remove
the domain from the allowlist, restricting collaboration to and from users in that domain.  This method returns `True`
to indicate that deletion was successful.

<!-- sample delete_collaboration_allowlist_entries_id -->
```python
client.collaboration_allowlist_entry(entry_id='11111').delete()
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete

List Exempt Users
-----------------

To get all exempt users from the collaboration allowlist, call
[`collaboration_allowlist.get_exemptions(limit=None, marker=None, fields=None)`][get_exemptions].  This method returns
a `BoxObjectCollection` that allows you to iterate over each
[`CollaborationAllowlistExemptTarget`][exemption_class] in the collection.

<!-- sample get_collaboration_allowlist_exempt_targets -->
```python
exemptions = client.collaboration_allowlist().get_exemptions()
for exemption in exemptions:
    print(f'{exemption.user.name} (ID: {exemption.user.id}) is exempt from the collaboration allowlist')
```

[get_exemptions]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_allowlist.CollaborationAllowlist.get_exemptions
[exemption_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_allowlist_exempt_target.CollaborationAllowlistExemptTarget

Get Exempt User Information
---------------------------

To get information about an exempted user, call [`collaboration_allowlist_exempt_target.get(*, fields=None, headers=None, **kwargs)`][get].
This method will return a [`CollaborationAllowlistExemptTarget][exemption_class] with fields populated by data from the API.

<!-- sample get_collaboration_allowlist_exempt_targets_id -->
```python
exemption_id = '11111'
exemption = client.collaboration_allowlist_exempt_target(exemption_id).get()
```

Exempt User from Allowlist
--------------------------

To exempt a user from the collaboration allowlist, call [`collaboration_allowlist.add_exemption(user)`][add_exemption]
with the [`User`][user_class] to exempt from the allowlist.  This user will no longer be subject to the collaboration
allowlist, and will be permitted to collaborate with users from any other domain.  This method returns a
[`CollaborationAllowlistExemptTarget`][exemption_class] object representing the exempted user.

<!-- sample post_collaboration_allowlist_exempt_targets -->
```python
user = client.user(user_id='11111')
exemption = client.collaboration_allowlist().add_exemption(user)
```

[add_exemption]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration_allowlist.CollaborationAllowlist.add_exemption
[user_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User

Remove User Exemption
---------------------

To remove a user exemption from the collaboration allowlist, call
[`collaboration_allowlist_exempt_target.delete()`][delete].  This will remove the exemption and make the user subject to
the collaboration allowlist again.  This method returns `True` to indicate that deletion was successful.

<!-- sample delete_collaboration_allowlist_exempt_targets_id -->
```python
client.collaboration_allowlist_exempt_target(exemption_id='22222').delete()
```
