from typing import Union

from typing import List

from box_sdk_gen.schemas.metadata_field_filter_float_range import (
    MetadataFieldFilterFloatRange,
)

from box_sdk_gen.schemas.metadata_field_filter_date_range import (
    MetadataFieldFilterDateRange,
)

from box_sdk_gen.box.errors import BoxSDKError

MetadataFilterValue = Union[
    str, float, List[str], MetadataFieldFilterFloatRange, MetadataFieldFilterDateRange
]
