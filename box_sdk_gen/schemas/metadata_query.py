from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import Dict

from typing import List

from box_sdk_gen.box.errors import BoxSDKError


class MetadataQueryOrderByDirectionField(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class MetadataQueryOrderByField(BaseObject):
    def __init__(
        self,
        *,
        field_key: Optional[str] = None,
        direction: Optional[MetadataQueryOrderByDirectionField] = None,
        **kwargs
    ):
        """
                :param field_key: The metadata template field to order by.

        The `field_key` represents the `key` value of a field from the
        metadata template being searched for., defaults to None
                :type field_key: Optional[str], optional
                :param direction: The direction to order by, either ascending or descending.

        The `ordering` direction must be the same for each item in the
        array., defaults to None
                :type direction: Optional[MetadataQueryOrderByDirectionField], optional
        """
        super().__init__(**kwargs)
        self.field_key = field_key
        self.direction = direction


class MetadataQuery(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'from_': 'from',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'from': 'from_',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        from_: str,
        ancestor_folder_id: str,
        *,
        query: Optional[str] = None,
        query_params: Optional[Dict] = None,
        order_by: Optional[List[MetadataQueryOrderByField]] = None,
        limit: Optional[int] = None,
        marker: Optional[str] = None,
        fields: Optional[List[str]] = None,
        **kwargs
    ):
        """
                :param from_: Specifies the template used in the query. Must be in the form
        `scope.templateKey`. Not all templates can be used in this field,
        most notably the built-in, Box-provided classification templates
        can not be used in a query.
                :type from_: str
                :param ancestor_folder_id: The ID of the folder that you are restricting the query to. A
        value of zero will return results from all folders you have access
        to. A non-zero value will only return results found in the folder
        corresponding to the ID or in any of its subfolders.
                :type ancestor_folder_id: str
                :param query: The query to perform. A query is a logical expression that is very similar
        to a SQL `SELECT` statement. Values in the search query can be turned into
        parameters specified in the `query_param` arguments list to prevent having
        to manually insert search values into the query string.

        For example, a value of `:amount` would represent the `amount` value in
        `query_params` object., defaults to None
                :type query: Optional[str], optional
                :param query_params: Set of arguments corresponding to the parameters specified in the
        `query`. The type of each parameter used in the `query_params` must match
        the type of the corresponding metadata template field., defaults to None
                :type query_params: Optional[Dict], optional
                :param order_by: A list of template fields and directions to sort the metadata query
        results by.

        The ordering `direction` must be the same for each item in the array., defaults to None
                :type order_by: Optional[List[MetadataQueryOrderByField]], optional
                :param limit: A value between 0 and 100 that indicates the maximum number of results
        to return for a single request. This only specifies a maximum
        boundary and will not guarantee the minimum number of results
        returned., defaults to None
                :type limit: Optional[int], optional
                :param marker: Marker to use for requesting the next page., defaults to None
                :type marker: Optional[str], optional
                :param fields: By default, this endpoint returns only the most basic info about the items for
        which the query matches. This attribute can be used to specify a list of
        additional attributes to return for any item, including its metadata.

        This attribute takes a list of item fields, metadata template identifiers,
        or metadata template field identifiers.

        For example:

        * `created_by` will add the details of the user who created the item to
        the response.
        * `metadata.<scope>.<templateKey>` will return the mini-representation
        of the metadata instance identified by the `scope` and `templateKey`.
        * `metadata.<scope>.<templateKey>.<field>` will return all the mini-representation
        of the metadata instance identified by the `scope` and `templateKey` plus
        the field specified by the `field` name. Multiple fields for the same
        `scope` and `templateKey` can be defined., defaults to None
                :type fields: Optional[List[str]], optional
        """
        super().__init__(**kwargs)
        self.from_ = from_
        self.ancestor_folder_id = ancestor_folder_id
        self.query = query
        self.query_params = query_params
        self.order_by = order_by
        self.limit = limit
        self.marker = marker
        self.fields = fields
