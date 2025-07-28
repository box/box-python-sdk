from enum import Enum

from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.items import Items

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData


class GetTrashedItemsDirection(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class GetTrashedItemsSort(str, Enum):
    NAME = 'name'
    DATE = 'date'
    SIZE = 'size'


class TrashedItemsManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_trashed_items(
        self,
        *,
        fields: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        usemarker: Optional[bool] = None,
        marker: Optional[str] = None,
        direction: Optional[GetTrashedItemsDirection] = None,
        sort: Optional[GetTrashedItemsSort] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Items:
        """
                Retrieves the files and folders that have been moved

                to the trash.


                Any attribute in the full files or folders objects can be passed


                in with the `fields` parameter to retrieve those specific


                attributes that are not returned by default.


                This endpoint defaults to use offset-based pagination, yet also supports


                marker-based pagination using the `marker` parameter.

                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param offset: The offset of the item at which to begin the response.

        Queries with offset parameter value
        exceeding 10000 will be rejected
        with a 400 response., defaults to None
                :type offset: Optional[int], optional
                :param usemarker: Specifies whether to use marker-based pagination instead of
        offset-based pagination. Only one pagination method can
        be used at a time.

        By setting this value to true, the API will return a `marker` field
        that can be passed as a parameter to this endpoint to get the next
        page of the response., defaults to None
                :type usemarker: Optional[bool], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param direction: The direction to sort results in. This can be either in alphabetical ascending
        (`ASC`) or descending (`DESC`) order., defaults to None
                :type direction: Optional[GetTrashedItemsDirection], optional
                :param sort: Defines the **second** attribute by which items
        are sorted.

        Items are always sorted by their `type` first, with
        folders listed before files, and files listed
        before web links.

        This parameter is not supported when using marker-based pagination., defaults to None
                :type sort: Optional[GetTrashedItemsSort], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'fields': to_string(fields),
                'limit': to_string(limit),
                'offset': to_string(offset),
                'usemarker': to_string(usemarker),
                'marker': to_string(marker),
                'direction': to_string(direction),
                'sort': to_string(sort),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/folders/trash/items',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Items)
