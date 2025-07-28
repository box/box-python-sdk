from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TimelineSkillCardTypeField(str, Enum):
    SKILL_CARD = 'skill_card'


class TimelineSkillCardSkillCardTypeField(str, Enum):
    TIMELINE = 'timeline'


class TimelineSkillCardSkillCardTitleField(BaseObject):
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


class TimelineSkillCardSkillTypeField(str, Enum):
    SERVICE = 'service'


class TimelineSkillCardSkillField(BaseObject):
    _discriminator = 'type', {'service'}

    def __init__(
        self,
        id: str,
        *,
        type: TimelineSkillCardSkillTypeField = TimelineSkillCardSkillTypeField.SERVICE,
        **kwargs
    ):
        """
                :param id: A custom identifier that represent the service that
        applied this metadata.
                :type id: str
                :param type: The value will always be `service`., defaults to TimelineSkillCardSkillTypeField.SERVICE
                :type type: TimelineSkillCardSkillTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class TimelineSkillCardInvocationTypeField(str, Enum):
    SKILL_INVOCATION = 'skill_invocation'


class TimelineSkillCardInvocationField(BaseObject):
    _discriminator = 'type', {'skill_invocation'}

    def __init__(
        self,
        id: str,
        *,
        type: TimelineSkillCardInvocationTypeField = TimelineSkillCardInvocationTypeField.SKILL_INVOCATION,
        **kwargs
    ):
        """
                :param id: A custom identifier that represent the instance of
        the service that applied this metadata. For example,
        if your `image-recognition-service` runs on multiple
        nodes, this field can be used to identify the ID of
        the node that was used to apply the metadata.
                :type id: str
                :param type: The value will always be `skill_invocation`., defaults to TimelineSkillCardInvocationTypeField.SKILL_INVOCATION
                :type type: TimelineSkillCardInvocationTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class TimelineSkillCardEntriesAppearsField(BaseObject):
    def __init__(
        self, *, start: Optional[int] = None, end: Optional[int] = None, **kwargs
    ):
        """
                :param start: The time in seconds when an
        entry should start appearing on a timeline., defaults to None
                :type start: Optional[int], optional
                :param end: The time in seconds when an
        entry should stop appearing on a timeline., defaults to None
                :type end: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.start = start
        self.end = end


class TimelineSkillCardEntriesField(BaseObject):
    def __init__(
        self,
        *,
        text: Optional[str] = None,
        appears: Optional[List[TimelineSkillCardEntriesAppearsField]] = None,
        image_url: Optional[str] = None,
        **kwargs
    ):
        """
                :param text: The text of the entry. This would be the display
        name for an item being placed on the timeline, for example the name
        of the person who was detected in a video., defaults to None
                :type text: Optional[str], optional
                :param appears: Defines a list of timestamps for when this item should appear on the
        timeline., defaults to None
                :type appears: Optional[List[TimelineSkillCardEntriesAppearsField]], optional
                :param image_url: The image to show on a for an entry that appears
        on a timeline. This image URL is required for every entry.

        The image will be shown in a
        list of items (for example faces), and clicking
        the image will show the user where that entry
        appears during the duration of this entry., defaults to None
                :type image_url: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.text = text
        self.appears = appears
        self.image_url = image_url


class TimelineSkillCard(BaseObject):
    _discriminator = 'skill_card_type', {'timeline'}

    def __init__(
        self,
        skill: TimelineSkillCardSkillField,
        invocation: TimelineSkillCardInvocationField,
        entries: List[TimelineSkillCardEntriesField],
        *,
        created_at: Optional[DateTime] = None,
        type: TimelineSkillCardTypeField = TimelineSkillCardTypeField.SKILL_CARD,
        skill_card_type: TimelineSkillCardSkillCardTypeField = TimelineSkillCardSkillCardTypeField.TIMELINE,
        skill_card_title: Optional[TimelineSkillCardSkillCardTitleField] = None,
        duration: Optional[int] = None,
        **kwargs
    ):
        """
                :param skill: The service that applied this metadata.
                :type skill: TimelineSkillCardSkillField
                :param invocation: The invocation of this service, used to track
        which instance of a service applied the metadata.
                :type invocation: TimelineSkillCardInvocationField
                :param entries: A list of entries on the timeline.
                :type entries: List[TimelineSkillCardEntriesField]
                :param created_at: The optional date and time this card was created at., defaults to None
                :type created_at: Optional[DateTime], optional
                :param type: The value will always be `skill_card`., defaults to TimelineSkillCardTypeField.SKILL_CARD
                :type type: TimelineSkillCardTypeField, optional
                :param skill_card_type: The value will always be `timeline`., defaults to TimelineSkillCardSkillCardTypeField.TIMELINE
                :type skill_card_type: TimelineSkillCardSkillCardTypeField, optional
                :param skill_card_title: The title of the card., defaults to None
                :type skill_card_title: Optional[TimelineSkillCardSkillCardTitleField], optional
                :param duration: An total duration in seconds of the timeline., defaults to None
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
