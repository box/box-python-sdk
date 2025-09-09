from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.integration_mapping_teams import IntegrationMappingTeams

from box_sdk_gen.box.errors import BoxSDKError


class IntegrationMappingsTeams(BaseObject):
    def __init__(
        self, *, entries: Optional[List[IntegrationMappingTeams]] = None, **kwargs
    ):
        """
        :param entries: A list of integration mappings., defaults to None
        :type entries: Optional[List[IntegrationMappingTeams]], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
