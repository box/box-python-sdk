from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class LegalHoldPolicyAssignmentFilterField(BaseObject):
    def __init__(self, field: str, value: str, **kwargs):
        """
        :param field: The ID of the metadata template field to filter on.
        :type field: str
        :param value: The value of the metadata template field to filter on.
        :type value: str
        """
        super().__init__(**kwargs)
        self.field = field
        self.value = value
