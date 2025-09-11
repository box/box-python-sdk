from typing import Optional

from typing import Dict

from box_sdk_gen.schemas.upload_part_mini import UploadPartMini

from box_sdk_gen.box.errors import BoxSDKError


class UploadPart(UploadPartMini):
    _fields_to_json_mapping: Dict[str, str] = {
        'sha_1': 'sha1',
        **UploadPartMini._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'sha1': 'sha_1',
        **UploadPartMini._json_to_fields_mapping,
    }

    def __init__(
        self,
        *,
        sha_1: Optional[str] = None,
        part_id: Optional[str] = None,
        offset: Optional[int] = None,
        size: Optional[int] = None,
        **kwargs
    ):
        """
                :param sha_1: The SHA1 hash of the chunk., defaults to None
                :type sha_1: Optional[str], optional
                :param part_id: The unique ID of the chunk., defaults to None
                :type part_id: Optional[str], optional
                :param offset: The offset of the chunk within the file
        in bytes. The lower bound of the position
        of the chunk within the file., defaults to None
                :type offset: Optional[int], optional
                :param size: The size of the chunk in bytes., defaults to None
                :type size: Optional[int], optional
        """
        super().__init__(part_id=part_id, offset=offset, size=size, **kwargs)
        self.sha_1 = sha_1
