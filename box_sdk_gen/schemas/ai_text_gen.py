from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Union

from box_sdk_gen.schemas.ai_dialogue_history import AiDialogueHistory

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_text_gen import AiAgentTextGen

from box_sdk_gen.box.errors import BoxSDKError


class AiTextGenItemsTypeField(str, Enum):
    FILE = 'file'


class AiTextGenItemsField(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        id: str,
        *,
        type: AiTextGenItemsTypeField = AiTextGenItemsTypeField.FILE,
        content: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The ID of the item.
        :type id: str
        :param type: The type of the item., defaults to AiTextGenItemsTypeField.FILE
        :type type: AiTextGenItemsTypeField, optional
        :param content: The content to use as context for generating new text or editing existing text., defaults to None
        :type content: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.content = content


class AiTextGen(BaseObject):
    def __init__(
        self,
        prompt: str,
        items: List[AiTextGenItemsField],
        *,
        dialogue_history: Optional[List[AiDialogueHistory]] = None,
        ai_agent: Optional[Union[AiAgentReference, AiAgentTextGen]] = None,
        **kwargs
    ):
        """
                :param prompt: The prompt provided by the client to be answered by the LLM. The prompt's length is limited to 10000 characters.
                :type prompt: str
                :param items: The items to be processed by the LLM, often files.
        The array can include **exactly one** element.

        **Note**: Box AI handles documents with text representations up to 1MB in size.
        If the file size exceeds 1MB, the first 1MB of text representation will be processed.
                :type items: List[AiTextGenItemsField]
                :param dialogue_history: The history of prompts and answers previously passed to the LLM. This parameter provides the additional context to the LLM when generating the response., defaults to None
                :type dialogue_history: Optional[List[AiDialogueHistory]], optional
        """
        super().__init__(**kwargs)
        self.prompt = prompt
        self.items = items
        self.dialogue_history = dialogue_history
        self.ai_agent = ai_agent
