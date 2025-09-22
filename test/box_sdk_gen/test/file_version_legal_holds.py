import pytest

from box_sdk_gen.schemas.file_version_legal_holds import FileVersionLegalHolds

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.client import BoxClient

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testGetFileVersionLegalHolds():
    policy_id: str = '1234567890'
    file_version_legal_holds: FileVersionLegalHolds = (
        client.file_version_legal_holds.get_file_version_legal_holds(policy_id)
    )
    file_version_legal_holds_count: int = len(file_version_legal_holds.entries)
    assert file_version_legal_holds_count >= 0


def testGetFileVersionLegalHoldById():
    file_version_legal_hold_id: str = '987654321'
    with pytest.raises(Exception):
        client.file_version_legal_holds.get_file_version_legal_hold_by_id(
            file_version_legal_hold_id
        )
