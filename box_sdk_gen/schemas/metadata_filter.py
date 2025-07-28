from enum import Enum

from typing import Optional

from typing import Dict

from typing import Union

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.metadata_field_filter_float_range import (
    MetadataFieldFilterFloatRange,
)

from box_sdk_gen.schemas.metadata_field_filter_date_range import (
    MetadataFieldFilterDateRange,
)

from box_sdk_gen.box.errors import BoxSDKError


class MetadataFilterScopeField(str, Enum):
    GLOBAL = 'global'
    ENTERPRISE = 'enterprise'
    ENTERPRISE__ENTERPRISE_ID_ = 'enterprise_{enterprise_id}'


class MetadataFilter(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'template_key': 'templateKey',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'templateKey': 'template_key',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        *,
        scope: Optional[MetadataFilterScopeField] = None,
        template_key: Optional[str] = None,
        filters: Optional[
            Dict[
                str,
                Union[
                    str,
                    float,
                    List[str],
                    MetadataFieldFilterFloatRange,
                    MetadataFieldFilterDateRange,
                ],
            ]
        ] = None,
        **kwargs
    ):
        """
                :param scope: Specifies the scope of the template to filter search results by.

        This will be `enterprise_{enterprise_id}` for templates defined
        for use in this enterprise, and `global` for general templates
        that are available to all enterprises using Box., defaults to None
                :type scope: Optional[MetadataFilterScopeField], optional
                :param template_key: The key of the template used to filter search results.

        In many cases the template key is automatically derived
        of its display name, for example `Contract Template` would
        become `contractTemplate`. In some cases the creator of the
        template will have provided its own template key.

        Please [list the templates for an enterprise][list], or
        get all instances on a [file][file] or [folder][folder]
        to inspect a template's key.

        [list]: e://get-metadata-templates-enterprise
        [file]: e://get-files-id-metadata
        [folder]: e://get-folders-id-metadata, defaults to None
                :type template_key: Optional[str], optional
                :param filters: Specifies which fields on the template to filter the search
        results by. When more than one field is specified, the query
        performs a logical `AND` to ensure that the instance of the
        template matches each of the fields specified., defaults to None
                :type filters: Optional[Dict[str, Union[str, float, List[str], MetadataFieldFilterFloatRange, MetadataFieldFilterDateRange]]], optional
        """
        super().__init__(**kwargs)
        self.scope = scope
        self.template_key = template_key
        self.filters = filters
