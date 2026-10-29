from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathMappingImportCreateRequestV2026R0(BaseObject):
    def __init__(self, job_id: str, file_id: str, **kwargs):
        """
                :param job_id: The unique identifier of the shuttle job whose path mappings are
        replaced.
                :type job_id: str
                :param file_id: The unique identifier of the Box file holding the mapping workbook. The
        file is read as the calling user, so it must live somewhere that user can
        download from.
                :type file_id: str
        """
        super().__init__(**kwargs)
        self.job_id = job_id
        self.file_id = file_id
