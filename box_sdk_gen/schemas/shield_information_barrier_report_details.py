from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShieldInformationBarrierReportDetailsDetailsField(BaseObject):
    def __init__(self, *, folder_id: Optional[str] = None, **kwargs):
        """
        :param folder_id: Folder ID for locating this report., defaults to None
        :type folder_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.folder_id = folder_id


class ShieldInformationBarrierReportDetails(BaseObject):
    def __init__(
        self,
        *,
        details: Optional[ShieldInformationBarrierReportDetailsDetailsField] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.details = details
