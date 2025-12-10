from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.schemas.ai_item_ask import AiItemAsk

from box_sdk_gen.schemas.ai_dialogue_history import AiDialogueHistory

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_ask import AiAgentAsk

from box_sdk_gen.schemas.ai_ask_agent import AiAskAgent

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.ai_agent_text_gen import AiAgentTextGen

from box_sdk_gen.schemas.ai_text_gen_agent import AiTextGenAgent

from box_sdk_gen.schemas.ai_agent_extract import AiAgentExtract

from box_sdk_gen.schemas.ai_agent_extract_structured import AiAgentExtractStructured

from box_sdk_gen.schemas.ai_item_base import AiItemBase

from box_sdk_gen.schemas.ai_extract_agent import AiExtractAgent

from box_sdk_gen.schemas.ai_extract_structured_agent import AiExtractStructuredAgent

from box_sdk_gen.schemas.ai_response_full import AiResponseFull

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.ai_ask import AiAsk

from box_sdk_gen.schemas.ai_response import AiResponse

from box_sdk_gen.schemas.ai_text_gen import AiTextGen

from box_sdk_gen.schemas.ai_agent import AiAgent

from box_sdk_gen.schemas.ai_extract import AiExtract

from box_sdk_gen.schemas.ai_extract_structured_response import (
    AiExtractStructuredResponse,
)

from box_sdk_gen.schemas.ai_extract_structured import AiExtractStructured

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.serialization.json import sd_to_json


class CreateAiAskMode(str, Enum):
    MULTIPLE_ITEM_QA = 'multiple_item_qa'
    SINGLE_ITEM_QA = 'single_item_qa'


class CreateAiTextGenItemsTypeField(str, Enum):
    FILE = 'file'


class CreateAiTextGenItems(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        id: str,
        *,
        type: CreateAiTextGenItemsTypeField = CreateAiTextGenItemsTypeField.FILE,
        content: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The ID of the item.
        :type id: str
        :param type: The type of the item., defaults to CreateAiTextGenItemsTypeField.FILE
        :type type: CreateAiTextGenItemsTypeField, optional
        :param content: The content to use as context for generating new text or editing existing text., defaults to None
        :type content: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.content = content


class GetAiAgentDefaultConfigMode(str, Enum):
    ASK = 'ask'
    TEXT_GEN = 'text_gen'
    EXTRACT = 'extract'
    EXTRACT_STRUCTURED = 'extract_structured'


class CreateAiExtractStructuredMetadataTemplateTypeField(str, Enum):
    METADATA_TEMPLATE = 'metadata_template'


class CreateAiExtractStructuredMetadataTemplate(BaseObject):
    _discriminator = 'type', {'metadata_template'}

    def __init__(
        self,
        *,
        template_key: Optional[str] = None,
        type: Optional[CreateAiExtractStructuredMetadataTemplateTypeField] = None,
        scope: Optional[str] = None,
        **kwargs
    ):
        """
                :param template_key: The name of the metadata template., defaults to None
                :type template_key: Optional[str], optional
                :param type: Value is always `metadata_template`., defaults to None
                :type type: Optional[CreateAiExtractStructuredMetadataTemplateTypeField], optional
                :param scope: The scope of the metadata template that can either be global or
        enterprise.
        * The **global** scope is used for templates that are
        available to any Box enterprise.
        * The **enterprise** scope represents templates created within a specific enterprise,
          containing the ID of that enterprise., defaults to None
                :type scope: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.template_key = template_key
        self.type = type
        self.scope = scope


class CreateAiExtractStructuredFieldsOptionsField(BaseObject):
    def __init__(self, key: str, **kwargs):
        """
        :param key: A unique identifier for the field.
        :type key: str
        """
        super().__init__(**kwargs)
        self.key = key


class CreateAiExtractStructuredFields(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'display_name': 'displayName',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'displayName': 'display_name',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        key: str,
        *,
        description: Optional[str] = None,
        display_name: Optional[str] = None,
        prompt: Optional[str] = None,
        type: Optional[str] = None,
        options: Optional[List[CreateAiExtractStructuredFieldsOptionsField]] = None,
        **kwargs
    ):
        """
        :param key: A unique identifier for the field.
        :type key: str
        :param description: A description of the field., defaults to None
        :type description: Optional[str], optional
        :param display_name: The display name of the field., defaults to None
        :type display_name: Optional[str], optional
        :param prompt: The context about the key that may include how to find and format it., defaults to None
        :type prompt: Optional[str], optional
        :param type: The type of the field. It include but is not limited to string, float, date, enum, and multiSelect., defaults to None
        :type type: Optional[str], optional
        :param options: A list of options for this field. This is most often used in combination with the enum and multiSelect field types., defaults to None
        :type options: Optional[List[CreateAiExtractStructuredFieldsOptionsField]], optional
        """
        super().__init__(**kwargs)
        self.key = key
        self.description = description
        self.display_name = display_name
        self.prompt = prompt
        self.type = type
        self.options = options


class AiManager:
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

    def create_ai_ask(
        self,
        mode: CreateAiAskMode,
        prompt: str,
        items: List[AiItemAsk],
        *,
        dialogue_history: Optional[List[AiDialogueHistory]] = None,
        include_citations: Optional[bool] = None,
        ai_agent: Optional[AiAskAgent] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Optional[AiResponseFull]:
        """
                Sends an AI request to supported LLMs and returns an answer specifically focused on the user's question given the provided context.
                :param mode: Box AI handles text documents with text representations up to 1MB in size, or a maximum of 25 files,
        whichever comes first. If the text file size exceeds 1MB, the first 1MB of text representation will be processed.
        Box AI handles image documents with a resolution of 1024 x 1024 pixels, with a maximum of 5 images or 5 pages
        for multi-page images. If the number of image or image pages exceeds 5, the first 5 images or pages will
        be processed. If you set mode parameter to `single_item_qa`, the items array can have one element only.
        Currently Box AI does not support multi-modal requests. If both images and text are sent Box AI will only
        process the text.
                :type mode: CreateAiAskMode
                :param prompt: The prompt provided by the client to be answered by the LLM.
        The prompt's length is limited to 10000 characters.
                :type prompt: str
                :param items: The items to be processed by the LLM, often files.
                :type items: List[AiItemAsk]
                :param dialogue_history: The history of prompts and answers previously passed to the LLM. This provides additional context to the LLM in generating the response., defaults to None
                :type dialogue_history: Optional[List[AiDialogueHistory]], optional
                :param include_citations: A flag to indicate whether citations should be returned., defaults to None
                :type include_citations: Optional[bool], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'mode': mode,
            'prompt': prompt,
            'items': items,
            'dialogue_history': dialogue_history,
            'include_citations': include_citations,
            'ai_agent': ai_agent,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/ai/ask']),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        if to_string(response.status) == '204':
            return None
        return deserialize(response.data, AiResponseFull)

    def create_ai_text_gen(
        self,
        prompt: str,
        items: List[CreateAiTextGenItems],
        *,
        dialogue_history: Optional[List[AiDialogueHistory]] = None,
        ai_agent: Optional[AiTextGenAgent] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> AiResponse:
        """
                Sends an AI request to supported Large Language Models (LLMs) and returns generated text based on the provided prompt.
                :param prompt: The prompt provided by the client to be answered by the LLM. The prompt's length is limited to 10000 characters.
                :type prompt: str
                :param items: The items to be processed by the LLM, often files.
        The array can include **exactly one** element.

        **Note**: Box AI handles documents with text representations up to 1MB in size.
        If the file size exceeds 1MB, the first 1MB of text representation will be processed.
                :type items: List[CreateAiTextGenItems]
                :param dialogue_history: The history of prompts and answers previously passed to the LLM. This parameter provides the additional context to the LLM when generating the response., defaults to None
                :type dialogue_history: Optional[List[AiDialogueHistory]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'prompt': prompt,
            'items': items,
            'dialogue_history': dialogue_history,
            'ai_agent': ai_agent,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/ai/text_gen']
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
        return deserialize(response.data, AiResponse)

    def get_ai_agent_default_config(
        self,
        mode: GetAiAgentDefaultConfigMode,
        *,
        language: Optional[str] = None,
        model: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> AiAgent:
        """
                Get the AI agent default config.
                :param mode: The mode to filter the agent config to return.
                :type mode: GetAiAgentDefaultConfigMode
                :param language: The ISO language code to return the agent config for.
        If the language is not supported the default agent config is returned., defaults to None
                :type language: Optional[str], optional
                :param model: The model to return the default agent config for., defaults to None
                :type model: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'mode': to_string(mode),
                'language': to_string(language),
                'model': to_string(model),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/ai_agent_default']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, AiAgent)

    def create_ai_extract(
        self,
        prompt: str,
        items: List[AiItemBase],
        *,
        ai_agent: Optional[AiExtractAgent] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> AiResponse:
        """
        Sends an AI request to supported Large Language Models (LLMs) and extracts metadata in form of key-value pairs.

        In this request, both the prompt and the output can be freeform.


        Metadata template setup before sending the request is not required.

        :param prompt: The prompt provided to a Large Language Model (LLM) in the request. The prompt can be up to 10000 characters long and it can be an XML or a JSON schema.
        :type prompt: str
        :param items: The items that LLM will process. Currently, you can use files only.
        :type items: List[AiItemBase]
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'prompt': prompt, 'items': items, 'ai_agent': ai_agent}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/ai/extract']
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
        return deserialize(response.data, AiResponse)

    def create_ai_extract_structured(
        self,
        items: List[AiItemBase],
        *,
        metadata_template: Optional[CreateAiExtractStructuredMetadataTemplate] = None,
        fields: Optional[List[CreateAiExtractStructuredFields]] = None,
        ai_agent: Optional[AiExtractStructuredAgent] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> AiExtractStructuredResponse:
        """
                Sends an AI request to supported Large Language Models (LLMs) and returns extracted metadata as a set of key-value pairs.

                To define the extraction structure, provide either a metadata template or a list of fields. To learn more about creating templates, see [Creating metadata templates in the Admin Console](https://support.box.com/hc/en-us/articles/360044194033-Customizing-Metadata-Templates)


                or use the [metadata template API](g://metadata/templates/create).


                This endpoint also supports [Enhanced Extract Agent](g://box-ai/ai-tutorials/extract-metadata-structured/#enhanced-extract-agent).


                For information about supported file formats and languages, see the [Extract metadata from file (structured)](g://box-ai/ai-tutorials/extract-metadata-structured) API guide.

                :param items: The items to be processed by the LLM. Currently you can use files only.
                :type items: List[AiItemBase]
                :param metadata_template: The metadata template containing the fields to extract.
        For your request to work, you must provide either `metadata_template` or `fields`, but not both., defaults to None
                :type metadata_template: Optional[CreateAiExtractStructuredMetadataTemplate], optional
                :param fields: The fields to be extracted from the provided items.
        For your request to work, you must provide either `metadata_template` or `fields`, but not both., defaults to None
                :type fields: Optional[List[CreateAiExtractStructuredFields]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'items': items,
            'metadata_template': metadata_template,
            'fields': fields,
            'ai_agent': ai_agent,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/ai/extract_structured',
                    ]
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
        return deserialize(response.data, AiExtractStructuredResponse)
