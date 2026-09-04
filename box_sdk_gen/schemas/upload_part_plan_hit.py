from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class UploadPartPlanHit(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'sha_512': 'sha512',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'sha512': 'sha_512',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(self, offset: int, size: int, sha_512: str, part_id: str, **kwargs):
        """
                :param offset: The offset of the chunk within the file
        in bytes. The lower bound of the position
        of the chunk within the file.
                :type offset: int
                :param size: The size of the chunk in bytes.
                :type size: int
                :param sha_512: The `SHA-512` hash of the chunk.
                :type sha_512: str
                :param part_id: The unique ID of the chunk.
                :type part_id: str
        """
        super().__init__(**kwargs)
        self.offset = offset
        self.size = size
        self.sha_512 = sha_512
        self.part_id = part_id
