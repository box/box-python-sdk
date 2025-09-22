from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.collaboration_allowlist_entries import (
    CollaborationAllowlistEntries,
)

from box_sdk_gen.schemas.collaboration_allowlist_entry import (
    CollaborationAllowlistEntry,
)

from box_sdk_gen.managers.collaboration_allowlist_entries import (
    CreateCollaborationWhitelistEntryDirection,
)

from test.box_sdk_gen.test.commons import get_default_client

from box_sdk_gen.internal.utils import get_uuid

client: BoxClient = get_default_client()


def testCollaborationAllowlistEntries():
    allowlist: CollaborationAllowlistEntries = (
        client.collaboration_allowlist_entries.get_collaboration_whitelist_entries()
    )
    assert len(allowlist.entries) >= 0
    domain: str = ''.join([get_uuid(), 'example.com'])
    new_entry: CollaborationAllowlistEntry = (
        client.collaboration_allowlist_entries.create_collaboration_whitelist_entry(
            domain, CreateCollaborationWhitelistEntryDirection.INBOUND
        )
    )
    assert to_string(new_entry.type) == 'collaboration_whitelist_entry'
    assert to_string(new_entry.direction) == 'inbound'
    assert new_entry.domain == domain
    entry: CollaborationAllowlistEntry = (
        client.collaboration_allowlist_entries.get_collaboration_whitelist_entry_by_id(
            new_entry.id
        )
    )
    assert entry.id == new_entry.id
    assert to_string(entry.direction) == to_string(new_entry.direction)
    assert entry.domain == domain
    client.collaboration_allowlist_entries.delete_collaboration_whitelist_entry_by_id(
        entry.id
    )
    with pytest.raises(Exception):
        client.collaboration_allowlist_entries.get_collaboration_whitelist_entry_by_id(
            entry.id
        )
