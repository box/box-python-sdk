from enum import Enum

from typing import List

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_ask import AiAgentAsk

from box_sdk_gen.schemas.ai_item_ask import AiItemAsk

from box_sdk_gen.schemas.ai_dialogue_history import AiDialogueHistory

from box_sdk_gen.schemas.ai_ask_agent import AiAskAgent

from box_sdk_gen.box.errors import BoxSDKError


class AiAskModeField(str, Enum):
    MULTIPLE_ITEM_QA = 'multiple_item_qa'
    SINGLE_ITEM_QA = 'single_item_qa'


class AiAsk(BaseObject):
    def __init__(
        self,
        mode: AiAskModeField,
        prompt: str,
        items: List[AiItemAsk],
        *,
        dialogue_history: Optional[List[AiDialogueHistory]] = None,
        include_citations: Optional[bool] = None,
        ai_agent: Optional[AiAskAgent] = None,
        **kwargs
    ):
        """
                :param mode: Box AI handles text documents with text representations up to 1MB in size, or a maximum of 25 files,
        whichever comes first. If the text file size exceeds 1MB, the first 1MB of text representation will be processed.
        Box AI handles image documents with a resolution of 1024 x 1024 pixels, with a maximum of 5 images or 5 pages
        for multi-page images. If the number of image or image pages exceeds 5, the first 5 images or pages will
        be processed. If you set mode parameter to `single_item_qa`, the items array can have one element only.
        Currently Box AI does not support multi-modal requests. If both images and text are sent Box AI will only
        process the text.
                :type mode: AiAskModeField
                :param prompt: The prompt provided by the client to be answered by the LLM.
        The prompt's length is limited to 10000 characters.
                :type prompt: str
                :param items: The items to be processed by the LLM, often files.
                :type items: List[AiItemAsk]
                :param dialogue_history: The history of prompts and answers previously passed to the LLM. This provides additional context to the LLM in generating the response., defaults to None
                :type dialogue_history: Optional[List[AiDialogueHistory]], optional
                :param include_citations: A flag to indicate whether citations should be returned., defaults to None
                :type include_citations: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.mode = mode
        self.prompt = prompt
        self.items = items
        self.dialogue_history = dialogue_history
        self.include_citations = include_citations
        self.ai_agent = ai_agent
