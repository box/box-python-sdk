from enum import Enum

class SkillsErrorEnum(Enum):
    FILE_PROCESSING_ERROR = 'skills_file_processing_error'
    INVALID_FILE_SIZE = 'skills_invalid_file_size_error'
    INVALID_FILE_FORMAT = 'skills_invalid_file_format_error'
    INVALID_EVENT = 'skills_invalid_event_error'
    NO_INFO_FOUND = 'skills_no_info_found'
    INVOCATIONS_ERROR = 'skills_invocations_error'
    EXTERNAL_AUTH_ERROR = 'skills_external_auth_error.'
    BILLING_ERROR = 'skills_billing_error'
    UNKNOWN = 'skills_unknown_error'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def has(cls, enum):
        return any(enum == item for item in cls)
