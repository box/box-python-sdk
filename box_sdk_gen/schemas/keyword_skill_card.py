from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class KeywordSkillCardTypeField(str, Enum):
    SKILL_CARD = 'skill_card'


class KeywordSkillCardSkillCardTypeField(str, Enum):
    KEYWORD = 'keyword'


class KeywordSkillCardSkillCardTitleField(BaseObject):
    def __init__(self, message: str, *, code: Optional[str] = None, **kwargs):
        """
        :param message: The actual title to show in the UI.
        :type message: str
        :param code: An optional identifier for the title., defaults to None
        :type code: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.message = message
        self.code = code


class KeywordSkillCardSkillTypeField(str, Enum):
    SERVICE = 'service'


class KeywordSkillCardSkillField(BaseObject):
    _discriminator = 'type', {'service'}

    def __init__(
        self,
        id: str,
        *,
        type: KeywordSkillCardSkillTypeField = KeywordSkillCardSkillTypeField.SERVICE,
        **kwargs
    ):
        """
                :param id: A custom identifier that represent the service that
        applied this metadata.
                :type id: str
                :param type: The value will always be `service`., defaults to KeywordSkillCardSkillTypeField.SERVICE
                :type type: KeywordSkillCardSkillTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class KeywordSkillCardInvocationTypeField(str, Enum):
    SKILL_INVOCATION = 'skill_invocation'


class KeywordSkillCardInvocationField(BaseObject):
    _discriminator = 'type', {'skill_invocation'}

    def __init__(
        self,
        id: str,
        *,
        type: KeywordSkillCardInvocationTypeField = KeywordSkillCardInvocationTypeField.SKILL_INVOCATION,
        **kwargs
    ):
        """
                :param id: A custom identifier that represent the instance of
        the service that applied this metadata. For example,
        if your `image-recognition-service` runs on multiple
        nodes, this field can be used to identify the ID of
        the node that was used to apply the metadata.
                :type id: str
                :param type: The value will always be `skill_invocation`., defaults to KeywordSkillCardInvocationTypeField.SKILL_INVOCATION
                :type type: KeywordSkillCardInvocationTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class KeywordSkillCardEntriesField(BaseObject):
    def __init__(self, *, text: Optional[str] = None, **kwargs):
        """
        :param text: The text of the keyword., defaults to None
        :type text: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.text = text


class KeywordSkillCard(BaseObject):
    _discriminator = 'skill_card_type', {'keyword'}

    def __init__(
        self,
        skill: KeywordSkillCardSkillField,
        invocation: KeywordSkillCardInvocationField,
        entries: List[KeywordSkillCardEntriesField],
        *,
        created_at: Optional[DateTime] = None,
        type: KeywordSkillCardTypeField = KeywordSkillCardTypeField.SKILL_CARD,
        skill_card_type: KeywordSkillCardSkillCardTypeField = KeywordSkillCardSkillCardTypeField.KEYWORD,
        skill_card_title: Optional[KeywordSkillCardSkillCardTitleField] = None,
        **kwargs
    ):
        """
                :param skill: The service that applied this metadata.
                :type skill: KeywordSkillCardSkillField
                :param invocation: The invocation of this service, used to track
        which instance of a service applied the metadata.
                :type invocation: KeywordSkillCardInvocationField
                :param entries: An list of entries in the metadata card.
                :type entries: List[KeywordSkillCardEntriesField]
                :param created_at: The optional date and time this card was created at., defaults to None
                :type created_at: Optional[DateTime], optional
                :param type: The value will always be `skill_card`., defaults to KeywordSkillCardTypeField.SKILL_CARD
                :type type: KeywordSkillCardTypeField, optional
                :param skill_card_type: The value will always be `keyword`., defaults to KeywordSkillCardSkillCardTypeField.KEYWORD
                :type skill_card_type: KeywordSkillCardSkillCardTypeField, optional
                :param skill_card_title: The title of the card., defaults to None
                :type skill_card_title: Optional[KeywordSkillCardSkillCardTitleField], optional
        """
        super().__init__(**kwargs)
        self.skill = skill
        self.invocation = invocation
        self.entries = entries
        self.created_at = created_at
        self.type = type
        self.skill_card_type = skill_card_type
        self.skill_card_title = skill_card_title
