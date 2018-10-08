Collaboration Whitelist
=======================

The Collaboration Whitelist API allows you to manage a set of approved domains (e.g. whitelist) that can collaborate with your enterprise. You can also manage whether the whitelisted domains are approved for outbound or inbound collaboration.

It is important to note that the collaboration whitelist functionality is only available to customers with Box Governance.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Collaboration Whitelist](#collaboration-whitelist)
  - [List Collaboration Whitelist Entries](#list-collaboration-whitelist-entries)
  - [Get Information for Collaboration Whitelist Entry](#get-information-for-collaboration-whitelist-entry)
  - [Whitelist a Domain for Collaboration](#whitelist-a-domain-for-collaboration)
  - [Remove a Domain from Whitelist](#remove-a-domain-from-whitelist)
  - [List Exempt Users](#list-exempt-users)
  - [Get Exempt User Information](#get-exempt-user-information)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

List Collaboration Whitelist Entries
------------------------------------

To retrieve a list of collaboration whitelist entries, use `collaboration_whitelist.get_entries(limit=None, marker=None, fields=None)`

```python
whitelist_entries = client.collaboration_whitelist().get_entries()
for whitelist_entry in whitelist_entries:
    # Do something
```

Get Information for Collaboration Whitelist Entry
-------------------------------------------------

To get information about a collaboration whitelist entry, use `collaboration_whitelist_entry.get(fields=None)`.

```python
collaboration_whitelist_entry_info = client.collaboration_whitelist_entry('11111').get()
```

Whitelist a Domain for Collaboration
------------------------------------

To whitelist a domain for collaboration, use `collaboration_whitelist.add_domain(domain, direction)`.

You can determine the direction of the whitelist by passing in 'outbound', 'inbound', or 'both'. Outbound collaboration is defined as
a user in your enterprise collaborating on content owned by someone outside your enterprise. Inbound collaboration is defined as a user outside of your enterprise collaborating on content owned by your enterprise.

```python
from boxsdk.object.collaboration_whitelist import WhitelistDirection
domain = 'https://example.com'
whitelist_entry = client.collaboration_whitelist().add_domain(domain=domain, direction=WhitelistDirection.INBOUND)
```

Remove a Domain from Whitelist
------------------------------

To remove a collaboration whitelisted domain, use `collaboration_whitelist_entry.delete()`

```python
client.collaboration_whitelist_entry('11111').delete()
```

List Exempt Users
-----------------

To receive an iterable of exempt users from collaboration whitelist, use `collaboration_whitelist.get_exemptions(limit=None, marker=None, fields=None)`.

```python
exempt_users = client.collaboration_whitelist().get_exemptions()
for exempt_user in exempt_users:
    # Do something...
```

Get Exempt User Information
---------------------------

To get information about an exempted user, use `collaboration_whitelist_exempt_target.get(fields=None)`.

```python
exempt_user_info = client.collaboration_whitelist_exempt_target('11111').get()
```

Exempt User from Whitelist
--------------------------

To exempt a user from a collaboration whitelist, use `collaboration_whitelist.add_exemption(user)`.

```python
user = client.user('11111')
exempted_user = client.collaboration_whitelist().add_exemption(user)
```

Remove User from Whitelist
--------------------------

To remove a user from a collaboration whitelist, use `collaboration_whitelist_exempt_target.delete()`.

```python
client.collaboration_whitelist_exempt_target('22222').delete
```
