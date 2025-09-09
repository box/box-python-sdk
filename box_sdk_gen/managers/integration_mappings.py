from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.integration_mapping_partner_item_slack import (
    IntegrationMappingPartnerItemSlack,
)

from box_sdk_gen.schemas.integration_mapping_partner_item_teams_create_request import (
    IntegrationMappingPartnerItemTeamsCreateRequest,
)

from box_sdk_gen.schemas.integration_mappings import IntegrationMappings

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.integration_mapping import IntegrationMapping

from box_sdk_gen.schemas.integration_mapping_slack_create_request import (
    IntegrationMappingSlackCreateRequest,
)

from box_sdk_gen.schemas.integration_mapping_box_item_slack import (
    IntegrationMappingBoxItemSlack,
)

from box_sdk_gen.schemas.integration_mapping_slack_options import (
    IntegrationMappingSlackOptions,
)

from box_sdk_gen.schemas.integration_mappings_teams import IntegrationMappingsTeams

from box_sdk_gen.schemas.integration_mapping_teams import IntegrationMappingTeams

from box_sdk_gen.schemas.integration_mapping_teams_create_request import (
    IntegrationMappingTeamsCreateRequest,
)

from box_sdk_gen.schemas.folder_reference import FolderReference

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


class GetSlackIntegrationMappingPartnerItemType(str, Enum):
    CHANNEL = 'channel'


class GetSlackIntegrationMappingBoxItemType(str, Enum):
    FOLDER = 'folder'


class GetTeamsIntegrationMappingPartnerItemType(str, Enum):
    CHANNEL = 'channel'
    TEAM = 'team'


class GetTeamsIntegrationMappingBoxItemType(str, Enum):
    FOLDER = 'folder'


class IntegrationMappingsManager:
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

    def get_slack_integration_mapping(
        self,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        partner_item_type: Optional[GetSlackIntegrationMappingPartnerItemType] = None,
        partner_item_id: Optional[str] = None,
        box_item_id: Optional[str] = None,
        box_item_type: Optional[GetSlackIntegrationMappingBoxItemType] = None,
        is_manually_created: Optional[bool] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> IntegrationMappings:
        """
                Lists [Slack integration mappings](https://support.box.com/hc/en-us/articles/4415585987859-Box-as-the-Content-Layer-for-Slack) in a users' enterprise.

                You need Admin or Co-Admin role to


                use this endpoint.

                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param partner_item_type: Mapped item type, for which the mapping should be returned., defaults to None
                :type partner_item_type: Optional[GetSlackIntegrationMappingPartnerItemType], optional
                :param partner_item_id: ID of the mapped item,
        for which the mapping should be returned., defaults to None
                :type partner_item_id: Optional[str], optional
                :param box_item_id: Box item ID, for which the mappings should be returned., defaults to None
                :type box_item_id: Optional[str], optional
                :param box_item_type: Box item type, for
        which the mappings should be returned., defaults to None
                :type box_item_type: Optional[GetSlackIntegrationMappingBoxItemType], optional
                :param is_manually_created: Whether the mapping has been manually created., defaults to None
                :type is_manually_created: Optional[bool], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'marker': to_string(marker),
                'limit': to_string(limit),
                'partner_item_type': to_string(partner_item_type),
                'partner_item_id': to_string(partner_item_id),
                'box_item_id': to_string(box_item_id),
                'box_item_type': to_string(box_item_type),
                'is_manually_created': to_string(is_manually_created),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/integration_mappings/slack',
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
        return deserialize(response.data, IntegrationMappings)

    def create_slack_integration_mapping(
        self,
        partner_item: IntegrationMappingPartnerItemSlack,
        box_item: IntegrationMappingBoxItemSlack,
        *,
        options: Optional[IntegrationMappingSlackOptions] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> IntegrationMapping:
        """
        Creates a [Slack integration mapping](https://support.box.com/hc/en-us/articles/4415585987859-Box-as-the-Content-Layer-for-Slack)

        by mapping a Slack channel to a Box item.


        You need Admin or Co-Admin role to


        use this endpoint.

        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'partner_item': partner_item,
            'box_item': box_item,
            'options': options,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/integration_mappings/slack',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, IntegrationMapping)

    def update_slack_integration_mapping_by_id(
        self,
        integration_mapping_id: str,
        *,
        box_item: Optional[IntegrationMappingBoxItemSlack] = None,
        options: Optional[IntegrationMappingSlackOptions] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> IntegrationMapping:
        """
                Updates a [Slack integration mapping](https://support.box.com/hc/en-us/articles/4415585987859-Box-as-the-Content-Layer-for-Slack).

                Supports updating the Box folder ID and options.


                You need Admin or Co-Admin role to


                use this endpoint.

                :param integration_mapping_id: An ID of an integration mapping.
        Example: "11235432"
                :type integration_mapping_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'box_item': box_item, 'options': options}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/integration_mappings/slack/',
                        to_string(integration_mapping_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, IntegrationMapping)

    def delete_slack_integration_mapping_by_id(
        self,
        integration_mapping_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a [Slack integration mapping](https://support.box.com/hc/en-us/articles/4415585987859-Box-as-the-Content-Layer-for-Slack).

                You need Admin or Co-Admin role to


                use this endpoint.

                :param integration_mapping_id: An ID of an integration mapping.
        Example: "11235432"
                :type integration_mapping_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/integration_mappings/slack/',
                        to_string(integration_mapping_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def get_teams_integration_mapping(
        self,
        *,
        partner_item_type: Optional[GetTeamsIntegrationMappingPartnerItemType] = None,
        partner_item_id: Optional[str] = None,
        box_item_id: Optional[str] = None,
        box_item_type: Optional[GetTeamsIntegrationMappingBoxItemType] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> IntegrationMappingsTeams:
        """
                Lists [Teams integration mappings](https://support.box.com/hc/en-us/articles/360044681474-Using-Box-for-Teams) in a users' enterprise.

                You need Admin or Co-Admin role to


                use this endpoint.

                :param partner_item_type: Mapped item type, for which the mapping should be returned., defaults to None
                :type partner_item_type: Optional[GetTeamsIntegrationMappingPartnerItemType], optional
                :param partner_item_id: ID of the mapped item,
        for which the mapping should be returned., defaults to None
                :type partner_item_id: Optional[str], optional
                :param box_item_id: Box item ID, for which the mappings should be returned., defaults to None
                :type box_item_id: Optional[str], optional
                :param box_item_type: Box item type, for
        which the mappings should be returned., defaults to None
                :type box_item_type: Optional[GetTeamsIntegrationMappingBoxItemType], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'partner_item_type': to_string(partner_item_type),
                'partner_item_id': to_string(partner_item_id),
                'box_item_id': to_string(box_item_id),
                'box_item_type': to_string(box_item_type),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/integration_mappings/teams',
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
        return deserialize(response.data, IntegrationMappingsTeams)

    def create_teams_integration_mapping(
        self,
        partner_item: IntegrationMappingPartnerItemTeamsCreateRequest,
        box_item: FolderReference,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> IntegrationMappingTeams:
        """
        Creates a [Teams integration mapping](https://support.box.com/hc/en-us/articles/360044681474-Using-Box-for-Teams)

        by mapping a Teams channel to a Box item.


        You need Admin or Co-Admin role to


        use this endpoint.

        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'partner_item': partner_item, 'box_item': box_item}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/integration_mappings/teams',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, IntegrationMappingTeams)

    def update_teams_integration_mapping_by_id(
        self,
        integration_mapping_id: str,
        *,
        box_item: Optional[FolderReference] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> IntegrationMappingTeams:
        """
                Updates a [Teams integration mapping](https://support.box.com/hc/en-us/articles/360044681474-Using-Box-for-Teams).

                Supports updating the Box folder ID and options.


                You need Admin or Co-Admin role to


                use this endpoint.

                :param integration_mapping_id: An ID of an integration mapping.
        Example: "11235432"
                :type integration_mapping_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'box_item': box_item}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/integration_mappings/teams/',
                        to_string(integration_mapping_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, IntegrationMappingTeams)

    def delete_teams_integration_mapping_by_id(
        self,
        integration_mapping_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a [Teams integration mapping](https://support.box.com/hc/en-us/articles/360044681474-Using-Box-for-Teams).

                You need Admin or Co-Admin role to


                use this endpoint.

                :param integration_mapping_id: An ID of an integration mapping.
        Example: "11235432"
                :type integration_mapping_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/integration_mappings/teams/',
                        to_string(integration_mapping_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None
