from box_sdk_gen.internal.utils import to_string

from typing import Optional

from box_sdk_gen.schemas.ai_single_agent_response_full import AiSingleAgentResponseFull

from box_sdk_gen.schemas.ai_studio_agent_ask import AiStudioAgentAsk

from box_sdk_gen.schemas.ai_multiple_agent_response import AiMultipleAgentResponse

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.ai_response_full import AiResponseFull

from box_sdk_gen.managers.ai import CreateAiAskMode

from box_sdk_gen.schemas.ai_item_ask import AiItemAsk

from box_sdk_gen.schemas.ai_item_ask import AiItemAskTypeField

from box_sdk_gen.box.developer_token_auth import BoxDeveloperTokenAuth

from box_sdk_gen.client import BoxClient

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

client: BoxClient = get_default_client()


def testAiStudioCRUD():
    agent_name: str = get_uuid()
    created_agent: AiSingleAgentResponseFull = client.ai_studio.create_ai_agent(
        agent_name,
        'enabled',
        ask=AiStudioAgentAsk(access_state='enabled', description='desc1'),
    )
    assert created_agent.name == agent_name
    agents: AiMultipleAgentResponse = client.ai_studio.get_ai_agents()
    num_agents: int = len(agents.entries)
    assert to_string(agents.entries[0].type) == 'ai_agent'
    retrieved_agent: AiSingleAgentResponseFull = client.ai_studio.get_ai_agent_by_id(
        created_agent.id, fields=['ask']
    )
    assert retrieved_agent.name == agent_name
    assert to_string(retrieved_agent.access_state) == 'enabled'
    assert to_string(retrieved_agent.ask.access_state) == 'enabled'
    assert retrieved_agent.ask.description == 'desc1'
    updated_agent: AiSingleAgentResponseFull = client.ai_studio.update_ai_agent_by_id(
        created_agent.id,
        agent_name,
        'enabled',
        ask=AiStudioAgentAsk(access_state='disabled', description='desc2'),
    )
    assert to_string(updated_agent.access_state) == 'enabled'
    assert to_string(updated_agent.ask.access_state) == 'disabled'
    assert updated_agent.ask.description == 'desc2'
    client.ai_studio.delete_ai_agent_by_id(created_agent.id)
    agents_after_delete: AiMultipleAgentResponse = client.ai_studio.get_ai_agents()
    assert len(agents_after_delete.entries) == num_agents - 1


def testUseAIAgentReferenceInAIAsk():
    agent_name: str = get_uuid()
    created_agent: AiSingleAgentResponseFull = client.ai_studio.create_ai_agent(
        agent_name,
        'enabled',
        ask=AiStudioAgentAsk(access_state='enabled', description='desc1'),
    )
    file_to_ask: FileFull = upload_new_file()
    response: Optional[AiResponseFull] = client.ai.create_ai_ask(
        CreateAiAskMode.SINGLE_ITEM_QA,
        'Which direction does the Sun rise?',
        [
            AiItemAsk(
                id=file_to_ask.id,
                type=AiItemAskTypeField.FILE,
                content='The Sun rises in the east.',
            )
        ],
        ai_agent=AiAgentReference(id=created_agent.id),
    )
    assert 'east' in response.answer
    assert response.completion_reason == 'done'
    assert len(response.ai_agent_info.models) > 0
    client.files.delete_file_by_id(file_to_ask.id)
    client.ai_studio.delete_ai_agent_by_id(created_agent.id)
