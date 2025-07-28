from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TranscriptSkillCardTypeField(str, Enum):
    SKILL_CARD = 'skill_card'


class TranscriptSkillCardSkillCardTypeField(str, Enum):
    TRANSCRIPT = 'transcript'


class TranscriptSkillCardSkillCardTitleField(BaseObject):
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


class TranscriptSkillCardSkillTypeField(str, Enum):
    SERVICE = 'service'


class TranscriptSkillCardSkillField(BaseObject):
    _discriminator = 'type', {'service'}

    def __init__(
        self,
        id: str,
        *,
        type: TranscriptSkillCardSkillTypeField = TranscriptSkillCardSkillTypeField.SERVICE,
        **kwargs
    ):
        """
                :param id: A custom identifier that represent the service that
        applied this metadata.
                :type id: str
                :param type: The value will always be `service`., defaults to TranscriptSkillCardSkillTypeField.SERVICE
                :type type: TranscriptSkillCardSkillTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class TranscriptSkillCardInvocationTypeField(str, Enum):
    SKILL_INVOCATION = 'skill_invocation'


class TranscriptSkillCardInvocationField(BaseObject):
    _discriminator = 'type', {'skill_invocation'}

    def __init__(
        self,
        id: str,
        *,
        type: TranscriptSkillCardInvocationTypeField = TranscriptSkillCardInvocationTypeField.SKILL_INVOCATION,
        **kwargs
    ):
        """
                :param id: A custom identifier that represent the instance of
        the service that applied this metadata. For example,
        if your `image-recognition-service` runs on multiple
        nodes, this field can be used to identify the ID of
        the node that was used to apply the metadata.
                :type id: str
                :param type: The value will always be `skill_invocation`., defaults to TranscriptSkillCardInvocationTypeField.SKILL_INVOCATION
                :type type: TranscriptSkillCardInvocationTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class TranscriptSkillCardEntriesAppearsField(BaseObject):
    def __init__(self, *, start: Optional[int] = None, **kwargs):
        """
                :param start: The time in seconds when an
        entry should start appearing on a timeline., defaults to None
                :type start: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.start = start


class TranscriptSkillCardEntriesField(BaseObject):
    def __init__(
        self,
        *,
        text: Optional[str] = None,
        appears: Optional[List[TranscriptSkillCardEntriesAppearsField]] = None,
        **kwargs
    ):
        """
                :param text: The text of the entry. This would be the transcribed text assigned
        to the entry on the timeline., defaults to None
                :type text: Optional[str], optional
                :param appears: Defines when a transcribed bit of text appears. This only includes a
        start time and no end time., defaults to None
                :type appears: Optional[List[TranscriptSkillCardEntriesAppearsField]], optional
        """
        super().__init__(**kwargs)
        self.text = text
        self.appears = appears


class TranscriptSkillCard(BaseObject):
    _discriminator = 'skill_card_type', {'transcript'}

    def __init__(
        self,
        skill: TranscriptSkillCardSkillField,
        invocation: TranscriptSkillCardInvocationField,
        entries: List[TranscriptSkillCardEntriesField],
        *,
        created_at: Optional[DateTime] = None,
        type: TranscriptSkillCardTypeField = TranscriptSkillCardTypeField.SKILL_CARD,
        skill_card_type: TranscriptSkillCardSkillCardTypeField = TranscriptSkillCardSkillCardTypeField.TRANSCRIPT,
        skill_card_title: Optional[TranscriptSkillCardSkillCardTitleField] = None,
        duration: Optional[int] = None,
        **kwargs
    ):
        """
                :param skill: The service that applied this metadata.
                :type skill: TranscriptSkillCardSkillField
                :param invocation: The invocation of this service, used to track
        which instance of a service applied the metadata.
                :type invocation: TranscriptSkillCardInvocationField
                :param entries: An list of entries for the card. This represents the individual entries of
        the transcription.
                :type entries: List[TranscriptSkillCardEntriesField]
                :param created_at: The optional date and time this card was created at., defaults to None
                :type created_at: Optional[DateTime], optional
                :param type: The value will always be `skill_card`., defaults to TranscriptSkillCardTypeField.SKILL_CARD
                :type type: TranscriptSkillCardTypeField, optional
                :param skill_card_type: The value will always be `transcript`., defaults to TranscriptSkillCardSkillCardTypeField.TRANSCRIPT
                :type skill_card_type: TranscriptSkillCardSkillCardTypeField, optional
                :param skill_card_title: The title of the card., defaults to None
                :type skill_card_title: Optional[TranscriptSkillCardSkillCardTitleField], optional
                :param duration: An optional total duration in seconds.

        Used with a `skill_card_type` of `transcript` or
        `timeline`., defaults to None
                :type duration: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.skill = skill
        self.invocation = invocation
        self.entries = entries
        self.created_at = created_at
        self.type = type
        self.skill_card_type = skill_card_type
        self.skill_card_title = skill_card_title
        self.duration = duration
