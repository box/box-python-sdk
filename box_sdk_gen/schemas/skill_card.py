from typing import Union

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCard

from box_sdk_gen.schemas.timeline_skill_card import TimelineSkillCard

from box_sdk_gen.schemas.transcript_skill_card import TranscriptSkillCard

from box_sdk_gen.schemas.status_skill_card import StatusSkillCard

from box_sdk_gen.box.errors import BoxSDKError

SkillCard = Union[
    KeywordSkillCard, TimelineSkillCard, TranscriptSkillCard, StatusSkillCard
]
