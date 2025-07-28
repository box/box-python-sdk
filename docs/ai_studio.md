# AiStudioManager

- [List AI agents](#list-ai-agents)
- [Create AI agent](#create-ai-agent)
- [Update AI agent](#update-ai-agent)
- [Get AI agent by agent ID](#get-ai-agent-by-agent-id)
- [Delete AI agent](#delete-ai-agent)

## List AI agents

Lists AI agents based on the provided parameters.

This operation is performed by calling function `get_ai_agents`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-ai-agents/).

<!-- sample get_ai_agents -->

```python
client.ai_studio.get_ai_agents()
```

### Arguments

- mode `Optional[List[str]]`
  - The mode to filter the agent config to return. Possible values are: `ask`, `text_gen`, and `extract`.
- fields `Optional[List[str]]`
  - The fields to return in the response.
- agent_state `Optional[List[str]]`
  - The state of the agents to return. Possible values are: `enabled`, `disabled` and `enabled_for_selected_users`.
- include_box_default `Optional[bool]`
  - Whether to include the Box default agents in the response.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiMultipleAgentResponse`.

A successful response including the agents list.

## Create AI agent

Creates an AI agent. At least one of the following capabilities must be provided: `ask`, `text_gen`, `extract`.

This operation is performed by calling function `create_ai_agent`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-ai-agents/).

<!-- sample post_ai_agents -->

```python
client.ai_studio.create_ai_agent(
    agent_name,
    "enabled",
    ask=AiStudioAgentAsk(access_state="enabled", description="desc1"),
)
```

### Arguments

- type `CreateAiAgentType`
  - The type of agent used to handle queries.
- name `str`
  - The name of the AI Agent.
- access_state `str`
  - The state of the AI Agent. Possible values are: `enabled`, `disabled`, and `enabled_for_selected_users`.
- icon_reference `Optional[str]`
  - The icon reference of the AI Agent. It should have format of the URL `https://cdn01.boxcdn.net/app-assets/aistudio/avatars/<file_name>` where possible values of `file_name` are: `logo_boxAi.png`,`logo_stamp.png`,`logo_legal.png`,`logo_finance.png`,`logo_config.png`,`logo_handshake.png`,`logo_analytics.png`,`logo_classification.png`.
- allowed_entities `Optional[List[AiAgentAllowedEntity]]`
  - List of allowed users or groups.
- ask `Optional[AiStudioAgentAsk]`
- text_gen `Optional[AiStudioAgentTextGen]`
- extract `Optional[AiStudioAgentExtract]`
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiSingleAgentResponseFull`.

Definition of created AI agent.

## Update AI agent

Updates an AI agent.

This operation is performed by calling function `update_ai_agent_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-ai-agents-id/).

<!-- sample put_ai_agents_id -->

```python
client.ai_studio.update_ai_agent_by_id(
    created_agent.id,
    agent_name,
    "enabled",
    ask=AiStudioAgentAsk(access_state="disabled", description="desc2"),
)
```

### Arguments

- agent_id `str`
  - The ID of the agent to update. Example: "1234"
- type `UpdateAiAgentByIdType`
  - The type of agent used to handle queries.
- name `str`
  - The name of the AI Agent.
- access_state `str`
  - The state of the AI Agent. Possible values are: `enabled`, `disabled`, and `enabled_for_selected_users`.
- icon_reference `Optional[str]`
  - The icon reference of the AI Agent. It should have format of the URL `https://cdn01.boxcdn.net/app-assets/aistudio/avatars/<file_name>` where possible values of `file_name` are: `logo_boxAi.png`,`logo_stamp.png`,`logo_legal.png`,`logo_finance.png`,`logo_config.png`,`logo_handshake.png`,`logo_analytics.png`,`logo_classification.png`.
- allowed_entities `Optional[List[AiAgentAllowedEntity]]`
  - List of allowed users or groups.
- ask `Optional[AiStudioAgentAsk]`
- text_gen `Optional[AiStudioAgentTextGen]`
- extract `Optional[AiStudioAgentExtract]`
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiSingleAgentResponseFull`.

Definition of created AI agent.

## Get AI agent by agent ID

Gets an AI Agent using the `agent_id` parameter.

This operation is performed by calling function `get_ai_agent_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-ai-agents-id/).

<!-- sample get_ai_agents_id -->

```python
client.ai_studio.get_ai_agent_by_id(created_agent.id, fields=["ask"])
```

### Arguments

- agent_id `str`
  - The agent id to get. Example: "1234"
- fields `Optional[List[str]]`
  - The fields to return in the response.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiSingleAgentResponseFull`.

A successful response including the agent.

## Delete AI agent

Deletes an AI agent using the provided parameters.

This operation is performed by calling function `delete_ai_agent_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-ai-agents-id/).

<!-- sample delete_ai_agents_id -->

```python
client.ai_studio.delete_ai_agent_by_id(created_agent.id)
```

### Arguments

- agent_id `str`
  - The ID of the agent to delete. Example: "1234"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

A successful response with no content.
