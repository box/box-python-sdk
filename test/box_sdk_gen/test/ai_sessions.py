import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.v2026_r0.ai_sessions_v2026_r0 import AiSessionsV2026R0

from box_sdk_gen.managers.ai_sessions import GetAiSessionsV2026R0Source

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testAiSessionsWithNonExistentIdV2026R0():
    ai_session_id: str = '123456'
    ai_sessions: AiSessionsV2026R0 = client.ai_sessions.get_ai_sessions_v2026_r0(
        GetAiSessionsV2026R0Source.API
    )
    assert len(ai_sessions.entries) >= 0
    with pytest.raises(Exception):
        client.ai_sessions.delete_ai_session_by_id_v2026_r0(ai_session_id)
