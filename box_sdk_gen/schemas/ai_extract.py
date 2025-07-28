from typing import List

from typing import Optional

from typing import Union

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_item_base import AiItemBase

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_extract import AiAgentExtract

from box_sdk_gen.box.errors import BoxSDKError


class AiExtract(BaseObject):
    def __init__(
        self,
        prompt: str,
        items: List[AiItemBase],
        *,
        ai_agent: Optional[Union[AiAgentReference, AiAgentExtract]] = None,
        **kwargs
    ):
        """
        :param prompt: The prompt provided to a Large Language Model (LLM) in the request. The prompt can be up to 10000 characters long and it can be an XML or a JSON schema.
        :type prompt: str
        :param items: The items that LLM will process. Currently, you can use files only.
        :type items: List[AiItemBase]
        """
        super().__init__(**kwargs)
        self.prompt = prompt
        self.items = items
        self.ai_agent = ai_agent
