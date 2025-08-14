from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCard

from box_sdk_gen.schemas.timeline_skill_card import TimelineSkillCard

from box_sdk_gen.schemas.transcript_skill_card import TranscriptSkillCard

from box_sdk_gen.schemas.status_skill_card import StatusSkillCard

from box_sdk_gen.schemas.skill_card import SkillCard

from box_sdk_gen.box.errors import BoxSDKError


class SkillCardsMetadata(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'can_edit': '$canEdit',
        'id': '$id',
        'parent': '$parent',
        'scope': '$scope',
        'template': '$template',
        'type': '$type',
        'type_version': '$typeVersion',
        'version': '$version',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        '$canEdit': 'can_edit',
        '$id': 'id',
        '$parent': 'parent',
        '$scope': 'scope',
        '$template': 'template',
        '$type': 'type',
        '$typeVersion': 'type_version',
        '$version': 'version',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        *,
        can_edit: Optional[bool] = None,
        id: Optional[str] = None,
        parent: Optional[str] = None,
        scope: Optional[str] = None,
        template: Optional[str] = None,
        type: Optional[str] = None,
        type_version: Optional[int] = None,
        version: Optional[int] = None,
        cards: Optional[List[SkillCard]] = None,
        **kwargs
    ):
        """
                :param can_edit: Whether the user can edit this metadata., defaults to None
                :type can_edit: Optional[bool], optional
                :param id: A UUID to identify the metadata object., defaults to None
                :type id: Optional[str], optional
                :param parent: An ID for the parent folder., defaults to None
                :type parent: Optional[str], optional
                :param scope: An ID for the scope in which this template
        has been applied., defaults to None
                :type scope: Optional[str], optional
                :param template: The name of the template., defaults to None
                :type template: Optional[str], optional
                :param type: A unique identifier for the "type" of this instance. This is an internal
        system property and should not be used by a client application., defaults to None
                :type type: Optional[str], optional
                :param type_version: The last-known version of the template of the object. This is an internal
        system property and should not be used by a client application., defaults to None
                :type type_version: Optional[int], optional
                :param version: The version of the metadata object. Starts at 0 and increases every time
        a user-defined property is modified., defaults to None
                :type version: Optional[int], optional
                :param cards: A list of Box Skill cards that have been applied to this file., defaults to None
                :type cards: Optional[List[SkillCard]], optional
        """
        super().__init__(**kwargs)
        self.can_edit = can_edit
        self.id = id
        self.parent = parent
        self.scope = scope
        self.template = template
        self.type = type
        self.type_version = type_version
        self.version = version
        self.cards = cards
