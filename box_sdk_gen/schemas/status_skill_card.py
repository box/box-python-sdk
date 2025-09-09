from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class StatusSkillCardTypeField(str, Enum):
    SKILL_CARD = 'skill_card'


class StatusSkillCardSkillCardTypeField(str, Enum):
    STATUS = 'status'


class StatusSkillCardSkillCardTitleField(BaseObject):
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


class StatusSkillCardStatusCodeField(str, Enum):
    INVOKED = 'invoked'
    PROCESSING = 'processing'
    SUCCESS = 'success'
    TRANSIENT_FAILURE = 'transient_failure'
    PERMANENT_FAILURE = 'permanent_failure'


class StatusSkillCardStatusField(BaseObject):
    def __init__(
        self,
        code: StatusSkillCardStatusCodeField,
        *,
        message: Optional[str] = None,
        **kwargs
    ):
        """
                :param code: A code for the status of this Skill invocation. By
        default each of these will have their own accompanied
        messages. These can be adjusted by setting the `message`
        value on this object.
                :type code: StatusSkillCardStatusCodeField
                :param message: A custom message that can be provided with this status.
        This will be shown in the web app to the end user., defaults to None
                :type message: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.code = code
        self.message = message


class StatusSkillCardSkillTypeField(str, Enum):
    SERVICE = 'service'


class StatusSkillCardSkillField(BaseObject):
    _discriminator = 'type', {'service'}

    def __init__(
        self,
        id: str,
        *,
        type: StatusSkillCardSkillTypeField = StatusSkillCardSkillTypeField.SERVICE,
        **kwargs
    ):
        """
                :param id: A custom identifier that represent the service that
        applied this metadata.
                :type id: str
                :param type: The value will always be `service`., defaults to StatusSkillCardSkillTypeField.SERVICE
                :type type: StatusSkillCardSkillTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class StatusSkillCardInvocationTypeField(str, Enum):
    SKILL_INVOCATION = 'skill_invocation'


class StatusSkillCardInvocationField(BaseObject):
    _discriminator = 'type', {'skill_invocation'}

    def __init__(
        self,
        id: str,
        *,
        type: StatusSkillCardInvocationTypeField = StatusSkillCardInvocationTypeField.SKILL_INVOCATION,
        **kwargs
    ):
        """
                :param id: A custom identifier that represent the instance of
        the service that applied this metadata. For example,
        if your `image-recognition-service` runs on multiple
        nodes, this field can be used to identify the ID of
        the node that was used to apply the metadata.
                :type id: str
                :param type: The value will always be `skill_invocation`., defaults to StatusSkillCardInvocationTypeField.SKILL_INVOCATION
                :type type: StatusSkillCardInvocationTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class StatusSkillCard(BaseObject):
    _discriminator = 'skill_card_type', {'status'}

    def __init__(
        self,
        status: StatusSkillCardStatusField,
        skill: StatusSkillCardSkillField,
        invocation: StatusSkillCardInvocationField,
        *,
        created_at: Optional[DateTime] = None,
        type: StatusSkillCardTypeField = StatusSkillCardTypeField.SKILL_CARD,
        skill_card_type: StatusSkillCardSkillCardTypeField = StatusSkillCardSkillCardTypeField.STATUS,
        skill_card_title: Optional[StatusSkillCardSkillCardTitleField] = None,
        **kwargs
    ):
        """
                :param status: Sets the status of the skill. This can be used to show a message to the user while the Skill is processing the data, or if it was not able to process the file.
                :type status: StatusSkillCardStatusField
                :param skill: The service that applied this metadata.
                :type skill: StatusSkillCardSkillField
                :param invocation: The invocation of this service, used to track
        which instance of a service applied the metadata.
                :type invocation: StatusSkillCardInvocationField
                :param created_at: The optional date and time this card was created at., defaults to None
                :type created_at: Optional[DateTime], optional
                :param type: The value will always be `skill_card`., defaults to StatusSkillCardTypeField.SKILL_CARD
                :type type: StatusSkillCardTypeField, optional
                :param skill_card_type: The value will always be `status`., defaults to StatusSkillCardSkillCardTypeField.STATUS
                :type skill_card_type: StatusSkillCardSkillCardTypeField, optional
                :param skill_card_title: The title of the card., defaults to None
                :type skill_card_title: Optional[StatusSkillCardSkillCardTitleField], optional
        """
        super().__init__(**kwargs)
        self.status = status
        self.skill = skill
        self.invocation = invocation
        self.created_at = created_at
        self.type = type
        self.skill_card_type = skill_card_type
        self.skill_card_title = skill_card_title
