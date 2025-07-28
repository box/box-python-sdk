from enum import Enum

from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.schemas.group_base import GroupBase

from box_sdk_gen.schemas.ai_agent_allowed_entity import AiAgentAllowedEntity

from box_sdk_gen.schemas.ai_studio_agent_ask import AiStudioAgentAsk

from box_sdk_gen.schemas.ai_studio_agent_text_gen import AiStudioAgentTextGen

from box_sdk_gen.schemas.ai_studio_agent_extract import AiStudioAgentExtract

from box_sdk_gen.schemas.ai_multiple_agent_response import AiMultipleAgentResponse

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.ai_single_agent_response_full import AiSingleAgentResponseFull

from box_sdk_gen.schemas.create_ai_agent import CreateAiAgent

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData


class CreateAiAgentType(str, Enum):
    AI_AGENT = 'ai_agent'


class UpdateAiAgentByIdType(str, Enum):
    AI_AGENT = 'ai_agent'


class AiStudioManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_ai_agents(
        self,
        *,
        mode: Optional[List[str]] = None,
        fields: Optional[List[str]] = None,
        agent_state: Optional[List[str]] = None,
        include_box_default: Optional[bool] = None,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> AiMultipleAgentResponse:
        """
        Lists AI agents based on the provided parameters.
        :param mode: The mode to filter the agent config to return. Possible values are: `ask`, `text_gen`, and `extract`., defaults to None
        :type mode: Optional[List[str]], optional
        :param fields: The fields to return in the response., defaults to None
        :type fields: Optional[List[str]], optional
        :param agent_state: The state of the agents to return. Possible values are: `enabled`, `disabled` and `enabled_for_selected_users`., defaults to None
        :type agent_state: Optional[List[str]], optional
        :param include_box_default: Whether to include the Box default agents in the response., defaults to None
        :type include_box_default: Optional[bool], optional
        :param marker: Defines the position marker at which to begin returning results., defaults to None
        :type marker: Optional[str], optional
        :param limit: The maximum number of items to return per page., defaults to None
        :type limit: Optional[int], optional
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'mode': to_string(mode),
                'fields': to_string(fields),
                'agent_state': to_string(agent_state),
                'include_box_default': to_string(include_box_default),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/ai_agents']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, AiMultipleAgentResponse)

    def create_ai_agent(
        self,
        name: str,
        access_state: str,
        *,
        type: CreateAiAgentType = CreateAiAgentType.AI_AGENT,
        icon_reference: Optional[str] = None,
        allowed_entities: Optional[List[AiAgentAllowedEntity]] = None,
        ask: Optional[AiStudioAgentAsk] = None,
        text_gen: Optional[AiStudioAgentTextGen] = None,
        extract: Optional[AiStudioAgentExtract] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> AiSingleAgentResponseFull:
        """
                Creates an AI agent. At least one of the following capabilities must be provided: `ask`, `text_gen`, `extract`.
                :param name: The name of the AI Agent.
                :type name: str
                :param access_state: The state of the AI Agent. Possible values are: `enabled`, `disabled`, and `enabled_for_selected_users`.
                :type access_state: str
                :param type: The type of agent used to handle queries., defaults to CreateAiAgentType.AI_AGENT
                :type type: CreateAiAgentType, optional
                :param icon_reference: The icon reference of the AI Agent. It should have format of the URL `https://cdn01.boxcdn.net/app-assets/aistudio/avatars/<file_name>`
        where possible values of `file_name` are: `logo_boxAi.png`,`logo_stamp.png`,`logo_legal.png`,`logo_finance.png`,`logo_config.png`,`logo_handshake.png`,`logo_analytics.png`,`logo_classification.png`., defaults to None
                :type icon_reference: Optional[str], optional
                :param allowed_entities: List of allowed users or groups., defaults to None
                :type allowed_entities: Optional[List[AiAgentAllowedEntity]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'type': type,
            'name': name,
            'access_state': access_state,
            'icon_reference': icon_reference,
            'allowed_entities': allowed_entities,
            'ask': ask,
            'text_gen': text_gen,
            'extract': extract,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/ai_agents']
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, AiSingleAgentResponseFull)

    def update_ai_agent_by_id(
        self,
        agent_id: str,
        name: str,
        access_state: str,
        *,
        type: UpdateAiAgentByIdType = UpdateAiAgentByIdType.AI_AGENT,
        icon_reference: Optional[str] = None,
        allowed_entities: Optional[List[AiAgentAllowedEntity]] = None,
        ask: Optional[AiStudioAgentAsk] = None,
        text_gen: Optional[AiStudioAgentTextGen] = None,
        extract: Optional[AiStudioAgentExtract] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> AiSingleAgentResponseFull:
        """
                Updates an AI agent.
                :param agent_id: The ID of the agent to update.
        Example: "1234"
                :type agent_id: str
                :param name: The name of the AI Agent.
                :type name: str
                :param access_state: The state of the AI Agent. Possible values are: `enabled`, `disabled`, and `enabled_for_selected_users`.
                :type access_state: str
                :param type: The type of agent used to handle queries., defaults to UpdateAiAgentByIdType.AI_AGENT
                :type type: UpdateAiAgentByIdType, optional
                :param icon_reference: The icon reference of the AI Agent. It should have format of the URL `https://cdn01.boxcdn.net/app-assets/aistudio/avatars/<file_name>`
        where possible values of `file_name` are: `logo_boxAi.png`,`logo_stamp.png`,`logo_legal.png`,`logo_finance.png`,`logo_config.png`,`logo_handshake.png`,`logo_analytics.png`,`logo_classification.png`., defaults to None
                :type icon_reference: Optional[str], optional
                :param allowed_entities: List of allowed users or groups., defaults to None
                :type allowed_entities: Optional[List[AiAgentAllowedEntity]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'type': type,
            'name': name,
            'access_state': access_state,
            'icon_reference': icon_reference,
            'allowed_entities': allowed_entities,
            'ask': ask,
            'text_gen': text_gen,
            'extract': extract,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/ai_agents/',
                        to_string(agent_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, AiSingleAgentResponseFull)

    def get_ai_agent_by_id(
        self,
        agent_id: str,
        *,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> AiSingleAgentResponseFull:
        """
                Gets an AI Agent using the `agent_id` parameter.
                :param agent_id: The agent id to get.
        Example: "1234"
                :type agent_id: str
                :param fields: The fields to return in the response., defaults to None
                :type fields: Optional[List[str]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/ai_agents/',
                        to_string(agent_id),
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, AiSingleAgentResponseFull)

    def delete_ai_agent_by_id(
        self, agent_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes an AI agent using the provided parameters.
                :param agent_id: The ID of the agent to delete.
        Example: "1234"
                :type agent_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/ai_agents/',
                        to_string(agent_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None
