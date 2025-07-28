from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import Union

from box_sdk_gen.schemas.file import File

from box_sdk_gen.schemas.folder import Folder

from box_sdk_gen.schemas.event import Event

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class SkillInvocationTypeField(str, Enum):
    SKILL_INVOCATION = 'skill_invocation'


class SkillInvocationSkillTypeField(str, Enum):
    SKILL = 'skill'


class SkillInvocationSkillField(BaseObject):
    _discriminator = 'type', {'skill'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[SkillInvocationSkillTypeField] = None,
        name: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this skill., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `skill`., defaults to None
        :type type: Optional[SkillInvocationSkillTypeField], optional
        :param name: The name of the skill., defaults to None
        :type name: Optional[str], optional
        :param api_key: The client ID of the application., defaults to None
        :type api_key: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name
        self.api_key = api_key


class SkillInvocationTokenReadTokenTypeField(str, Enum):
    BEARER = 'bearer'


class SkillInvocationTokenReadField(BaseObject):
    def __init__(
        self,
        *,
        access_token: Optional[str] = None,
        expires_in: Optional[int] = None,
        token_type: Optional[SkillInvocationTokenReadTokenTypeField] = None,
        restricted_to: Optional[str] = None,
        **kwargs
    ):
        """
                :param access_token: The requested access token., defaults to None
                :type access_token: Optional[str], optional
                :param expires_in: The time in seconds by which this token will expire., defaults to None
                :type expires_in: Optional[int], optional
                :param token_type: The type of access token returned., defaults to None
                :type token_type: Optional[SkillInvocationTokenReadTokenTypeField], optional
                :param restricted_to: The permissions that this access token permits,
        providing a list of resources (files, folders, etc)
        and the scopes permitted for each of those resources., defaults to None
                :type restricted_to: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.restricted_to = restricted_to


class SkillInvocationTokenWriteTokenTypeField(str, Enum):
    BEARER = 'bearer'


class SkillInvocationTokenWriteField(BaseObject):
    def __init__(
        self,
        *,
        access_token: Optional[str] = None,
        expires_in: Optional[int] = None,
        token_type: Optional[SkillInvocationTokenWriteTokenTypeField] = None,
        restricted_to: Optional[str] = None,
        **kwargs
    ):
        """
                :param access_token: The requested access token., defaults to None
                :type access_token: Optional[str], optional
                :param expires_in: The time in seconds by which this token will expire., defaults to None
                :type expires_in: Optional[int], optional
                :param token_type: The type of access token returned., defaults to None
                :type token_type: Optional[SkillInvocationTokenWriteTokenTypeField], optional
                :param restricted_to: The permissions that this access token permits,
        providing a list of resources (files, folders, etc)
        and the scopes permitted for each of those resources., defaults to None
                :type restricted_to: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.restricted_to = restricted_to


class SkillInvocationTokenField(BaseObject):
    def __init__(
        self,
        *,
        read: Optional[SkillInvocationTokenReadField] = None,
        write: Optional[SkillInvocationTokenWriteField] = None,
        **kwargs
    ):
        """
        :param read: The basics of an access token., defaults to None
        :type read: Optional[SkillInvocationTokenReadField], optional
        :param write: The basics of an access token., defaults to None
        :type write: Optional[SkillInvocationTokenWriteField], optional
        """
        super().__init__(**kwargs)
        self.read = read
        self.write = write


class SkillInvocationStatusStateField(str, Enum):
    INVOKED = 'invoked'
    PROCESSING = 'processing'
    SUCCESS = 'success'
    TRANSIENT_FAILURE = 'transient_failure'
    PERMANENT_FAILURE = 'permanent_failure'


class SkillInvocationStatusField(BaseObject):
    def __init__(
        self,
        *,
        state: Optional[SkillInvocationStatusStateField] = None,
        message: Optional[str] = None,
        error_code: Optional[str] = None,
        additional_info: Optional[str] = None,
        **kwargs
    ):
        """
                :param state: The state of this event.

        * `invoked` - Triggered the skill with event details to start
          applying skill on the file.
        * `processing` - Currently processing.
        * `success` - Completed processing with a success.
        * `transient_failure` - Encountered an issue which can be
          retried.
        * `permanent_failure` -  Encountered a permanent issue and
          retry would not help., defaults to None
                :type state: Optional[SkillInvocationStatusStateField], optional
                :param message: Status information., defaults to None
                :type message: Optional[str], optional
                :param error_code: Error code information, if error occurred., defaults to None
                :type error_code: Optional[str], optional
                :param additional_info: Additional status information., defaults to None
                :type additional_info: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.state = state
        self.message = message
        self.error_code = error_code
        self.additional_info = additional_info


class SkillInvocationEnterpriseTypeField(str, Enum):
    ENTERPRISE = 'enterprise'


class SkillInvocationEnterpriseField(BaseObject):
    _discriminator = 'type', {'enterprise'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[SkillInvocationEnterpriseTypeField] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this enterprise., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `enterprise`., defaults to None
        :type type: Optional[SkillInvocationEnterpriseTypeField], optional
        :param name: The name of the enterprise., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name


class SkillInvocation(BaseObject):
    _discriminator = 'type', {'skill_invocation'}

    def __init__(
        self,
        *,
        type: Optional[SkillInvocationTypeField] = None,
        id: Optional[str] = None,
        skill: Optional[SkillInvocationSkillField] = None,
        token: Optional[SkillInvocationTokenField] = None,
        status: Optional[SkillInvocationStatusField] = None,
        created_at: Optional[DateTime] = None,
        trigger: Optional[str] = None,
        enterprise: Optional[SkillInvocationEnterpriseField] = None,
        source: Optional[Union[File, Folder]] = None,
        event: Optional[Event] = None,
        **kwargs
    ):
        """
        :param type: The value will always be `skill_invocation`., defaults to None
        :type type: Optional[SkillInvocationTypeField], optional
        :param id: Unique identifier for the invocation request., defaults to None
        :type id: Optional[str], optional
        :param token: The read-only and read-write access tokens for this item., defaults to None
        :type token: Optional[SkillInvocationTokenField], optional
        :param status: The details status of this event., defaults to None
        :type status: Optional[SkillInvocationStatusField], optional
        :param created_at: The time this invocation was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param trigger: Action that triggered the invocation., defaults to None
        :type trigger: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.skill = skill
        self.token = token
        self.status = status
        self.created_at = created_at
        self.trigger = trigger
        self.enterprise = enterprise
        self.source = source
        self.event = event
