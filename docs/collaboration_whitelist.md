Collaboration Whitelist
=======================

The Collaboration Whitelist API allows you to manage a set of approved domains (e.g. whitelist) that can collaborate with your enterprise. You can also manage whether the whitelisted domains are approved for outbound or inbound collaboration.

It is important to note that the collaboration whitelist functionality is only available to customers with Box Governance.

List Collaboration Whitelist Entries
------------------------------------

To retrieve a list of collaboration whitelist entries, use `collaboration_whitelist().get_entries(limit=None, marker=None, fields=None)`

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

To whitelist a domain for collaboration, use `collaboration_whitelist().add_domain(domain, direction)`.

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

