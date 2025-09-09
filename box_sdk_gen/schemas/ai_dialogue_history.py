from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class AiDialogueHistory(BaseObject):
    def __init__(
        self,
        *,
        prompt: Optional[str] = None,
        answer: Optional[str] = None,
        created_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
        :param prompt: The prompt previously provided by the client and answered by the LLM., defaults to None
        :type prompt: Optional[str], optional
        :param answer: The answer previously provided by the LLM., defaults to None
        :type answer: Optional[str], optional
        :param created_at: The ISO date formatted timestamp of when the previous answer to the prompt was created., defaults to None
        :type created_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.prompt = prompt
        self.answer = answer
        self.created_at = created_at
