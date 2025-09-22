from typing import List

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCardTypeField

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCardSkillCardTypeField

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCardSkillCardTitleField

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCardSkillField

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCardSkillTypeField

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCardInvocationField

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCardInvocationTypeField

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCardEntriesField

from box_sdk_gen.schemas.skill_cards_metadata import SkillCardsMetadata

from box_sdk_gen.managers.skills import UpdateBoxSkillCardsOnFileRequestBody

from box_sdk_gen.managers.skills import UpdateBoxSkillCardsOnFileRequestBodyOpField

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCard

client: BoxClient = get_default_client()


def test_skills_cards_CRUD():
    file: FileFull = upload_new_file()
    skill_id: str = get_uuid()
    invocation_id: str = get_uuid()
    title_message: str = 'License Plates'
    card_to_create: KeywordSkillCard = KeywordSkillCard(
        type=KeywordSkillCardTypeField.SKILL_CARD,
        skill_card_type=KeywordSkillCardSkillCardTypeField.KEYWORD,
        skill_card_title=KeywordSkillCardSkillCardTitleField(
            code='license-plates', message=title_message
        ),
        skill=KeywordSkillCardSkillField(
            id=skill_id, type=KeywordSkillCardSkillTypeField.SERVICE
        ),
        invocation=KeywordSkillCardInvocationField(
            id=invocation_id, type=KeywordSkillCardInvocationTypeField.SKILL_INVOCATION
        ),
        entries=[KeywordSkillCardEntriesField(text='DN86 BOX')],
    )
    cards_to_create: List[KeywordSkillCard] = [card_to_create]
    skill_cards_metadata: SkillCardsMetadata = (
        client.skills.create_box_skill_cards_on_file(file.id, cards_to_create)
    )
    assert len(skill_cards_metadata.cards) == 1
    keyword_skill_card: KeywordSkillCard = skill_cards_metadata.cards[0]
    assert keyword_skill_card.skill.id == skill_id
    assert keyword_skill_card.skill_card_title.message == title_message
    updated_title_message: str = 'Updated License Plates'
    card_to_update: KeywordSkillCard = KeywordSkillCard(
        type=KeywordSkillCardTypeField.SKILL_CARD,
        skill_card_type=KeywordSkillCardSkillCardTypeField.KEYWORD,
        skill_card_title=KeywordSkillCardSkillCardTitleField(
            code='license-plates', message=updated_title_message
        ),
        skill=KeywordSkillCardSkillField(
            id=skill_id, type=KeywordSkillCardSkillTypeField.SERVICE
        ),
        invocation=KeywordSkillCardInvocationField(
            id=invocation_id, type=KeywordSkillCardInvocationTypeField.SKILL_INVOCATION
        ),
        entries=[KeywordSkillCardEntriesField(text='DN86 BOX')],
    )
    updated_skill_cards_metadata: SkillCardsMetadata = (
        client.skills.update_box_skill_cards_on_file(
            file.id,
            [
                UpdateBoxSkillCardsOnFileRequestBody(
                    op=UpdateBoxSkillCardsOnFileRequestBodyOpField.REPLACE,
                    path='/cards/0',
                    value=card_to_update,
                )
            ],
        )
    )
    updated_keyword_skill_card: KeywordSkillCard = updated_skill_cards_metadata.cards[0]
    assert updated_keyword_skill_card.skill.id == skill_id
    assert updated_keyword_skill_card.skill_card_title.message == updated_title_message
    received_skill_cards_metadata: SkillCardsMetadata = (
        client.skills.get_box_skill_cards_on_file(file.id)
    )
    received_keyword_skill_card: KeywordSkillCard = received_skill_cards_metadata.cards[
        0
    ]
    assert received_keyword_skill_card.skill.id == skill_id
    client.skills.delete_box_skill_cards_from_file(file.id)
    client.files.delete_file_by_id(file.id)
