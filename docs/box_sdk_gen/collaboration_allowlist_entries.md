# CollaborationAllowlistEntriesManager

- [List allowed collaboration domains](#list-allowed-collaboration-domains)
- [Add domain to list of allowed collaboration domains](#add-domain-to-list-of-allowed-collaboration-domains)
- [Get allowed collaboration domain](#get-allowed-collaboration-domain)
- [Remove domain from list of allowed collaboration domains](#remove-domain-from-list-of-allowed-collaboration-domains)

## List allowed collaboration domains

Returns the list domains that have been deemed safe to create collaborations
for within the current enterprise.

This operation is performed by calling function `get_collaboration_whitelist_entries`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-collaboration-whitelist-entries/).

<!-- sample get_collaboration_whitelist_entries -->

```python
client.collaboration_allowlist_entries.get_collaboration_whitelist_entries()
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `CollaborationAllowlistEntries`.

Returns a collection of domains that are allowed for collaboration.

## Add domain to list of allowed collaboration domains

Creates a new entry in the list of allowed domains to allow
collaboration for.

This operation is performed by calling function `create_collaboration_whitelist_entry`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-collaboration-whitelist-entries/).

<!-- sample post_collaboration_whitelist_entries -->

```python
client.collaboration_allowlist_entries.create_collaboration_whitelist_entry(domain, CreateCollaborationWhitelistEntryDirection.INBOUND)
```

### Arguments

- domain `str`
  - The domain to add to the list of allowed domains.
- direction `CreateCollaborationWhitelistEntryDirection`
  - The direction in which to allow collaborations.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `CollaborationAllowlistEntry`.

Returns a new entry on the list of allowed domains.

## Get allowed collaboration domain

Returns a domain that has been deemed safe to create collaborations
for within the current enterprise.

This operation is performed by calling function `get_collaboration_whitelist_entry_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-collaboration-whitelist-entries-id/).

<!-- sample get_collaboration_whitelist_entries_id -->

```python
client.collaboration_allowlist_entries.get_collaboration_whitelist_entry_by_id(new_entry.id)
```

### Arguments

- collaboration_whitelist_entry_id `str`
  - The ID of the entry in the list. Example: "213123"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `CollaborationAllowlistEntry`.

Returns an entry on the list of allowed domains.

## Remove domain from list of allowed collaboration domains

Removes a domain from the list of domains that have been deemed safe to create
collaborations for within the current enterprise.

This operation is performed by calling function `delete_collaboration_whitelist_entry_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-collaboration-whitelist-entries-id/).

<!-- sample delete_collaboration_whitelist_entries_id -->

```python
client.collaboration_allowlist_entries.delete_collaboration_whitelist_entry_by_id(entry.id)
```

### Arguments

- collaboration_whitelist_entry_id `str`
  - The ID of the entry in the list. Example: "213123"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

A blank response is returned if the entry was
successfully deleted.
