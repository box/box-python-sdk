from typing import Union

from box_sdk_gen.schemas.ai_taxonomy_reference import AiTaxonomyReference

from box_sdk_gen.schemas.ai_taxonomy_file_reference import AiTaxonomyFileReference

from box_sdk_gen.box.errors import BoxSDKError

AiTaxonomySource = Union[AiTaxonomyReference, AiTaxonomyFileReference]
