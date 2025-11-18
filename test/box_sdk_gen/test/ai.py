from typing import Optional

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.ai_agent import AiAgent

from box_sdk_gen.managers.ai import GetAiAgentDefaultConfigMode

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.ai_response_full import AiResponseFull

from box_sdk_gen.managers.ai import CreateAiAskMode

from box_sdk_gen.schemas.ai_item_ask import AiItemAsk

from box_sdk_gen.schemas.ai_item_ask import AiItemAskTypeField

from box_sdk_gen.schemas.ai_response import AiResponse

from box_sdk_gen.managers.ai import CreateAiTextGenItems

from box_sdk_gen.managers.ai import CreateAiTextGenItemsTypeField

from box_sdk_gen.schemas.ai_dialogue_history import AiDialogueHistory

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.ai_item_base import AiItemBase

from box_sdk_gen.schemas.ai_extract_structured_response import (
    AiExtractStructuredResponse,
)

from box_sdk_gen.managers.ai import CreateAiExtractStructuredFields

from box_sdk_gen.managers.ai import CreateAiExtractStructuredFieldsOptionsField

from box_sdk_gen.schemas.metadata_template import MetadataTemplate

from box_sdk_gen.managers.metadata_templates import CreateMetadataTemplateFields

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsTypeField,
)

from box_sdk_gen.managers.metadata_templates import (
    CreateMetadataTemplateFieldsOptionsField,
)

from box_sdk_gen.managers.ai import CreateAiExtractStructuredMetadataTemplate

from box_sdk_gen.managers.metadata_templates import DeleteMetadataTemplateScope

from test.box_sdk_gen.test.commons import get_default_client

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import string_to_byte_stream

from box_sdk_gen.internal.utils import delay_in_seconds

from box_sdk_gen.internal.utils import date_time_from_string

from test.box_sdk_gen.test.commons import upload_new_file

from box_sdk_gen.schemas.ai_agent_ask import AiAgentAsk

from box_sdk_gen.schemas.ai_agent_text_gen import AiAgentTextGen

from box_sdk_gen.schemas.ai_agent_extract import AiAgentExtract

from box_sdk_gen.schemas.ai_agent_extract_structured import AiAgentExtractStructured

client: BoxClient = get_default_client()


def testAskAISingleItem():
    ai_agent_config: AiAgent = client.ai.get_ai_agent_default_config(
        GetAiAgentDefaultConfigMode.ASK, language='en-US'
    )
    ai_ask_agent_config: AiAgentAsk = ai_agent_config
    ai_ask_agent_basic_text_config: AiAgentAsk = AiAgentAsk(
        basic_text=ai_ask_agent_config.basic_text
    )
    file_to_ask: FileFull = upload_new_file()
    response: Optional[AiResponseFull] = client.ai.create_ai_ask(
        CreateAiAskMode.SINGLE_ITEM_QA,
        'Which direction does the Sun rise?',
        [
            AiItemAsk(
                id=file_to_ask.id,
                type=AiItemAskTypeField.FILE,
                content='The Sun rises in the east',
            )
        ],
        ai_agent=ai_ask_agent_basic_text_config,
    )
    assert 'east' in response.answer
    assert response.completion_reason == 'done'
    client.files.delete_file_by_id(file_to_ask.id)


def testAskAIMultipleItems():
    file_to_ask_1: FileFull = upload_new_file()
    file_to_ask_2: FileFull = upload_new_file()
    response: Optional[AiResponseFull] = client.ai.create_ai_ask(
        CreateAiAskMode.MULTIPLE_ITEM_QA,
        'Which direction does the Sun rise?',
        [
            AiItemAsk(
                id=file_to_ask_1.id,
                type=AiItemAskTypeField.FILE,
                content='Earth goes around the Sun',
            ),
            AiItemAsk(
                id=file_to_ask_2.id,
                type=AiItemAskTypeField.FILE,
                content='The Sun rises in the east in the morning',
            ),
        ],
    )
    assert 'east' in response.answer
    assert response.completion_reason == 'done'
    client.files.delete_file_by_id(file_to_ask_1.id)
    client.files.delete_file_by_id(file_to_ask_2.id)


def testAITextGenWithDialogueHistory():
    file_to_ask: FileFull = upload_new_file()
    response: AiResponse = client.ai.create_ai_text_gen(
        'Paraphrase the documents',
        [
            CreateAiTextGenItems(
                id=file_to_ask.id,
                type=CreateAiTextGenItemsTypeField.FILE,
                content='The Earth goes around the Sun. The Sun rises in the east in the morning.',
            )
        ],
        dialogue_history=[
            AiDialogueHistory(
                prompt='What does the earth go around?',
                answer='The Sun',
                created_at=date_time_from_string('2021-01-01T00:00:00Z'),
            ),
            AiDialogueHistory(
                prompt='On Earth, where does the Sun rise?',
                answer='east',
                created_at=date_time_from_string('2021-01-01T00:00:00Z'),
            ),
        ],
    )
    assert 'Sun' in response.answer
    assert response.completion_reason == 'done'
    client.files.delete_file_by_id(file_to_ask.id)


def testGettingAIAskAgentConfig():
    ai_agent_config: AiAgent = client.ai.get_ai_agent_default_config(
        GetAiAgentDefaultConfigMode.ASK, language='en-US'
    )
    assert ai_agent_config.type == 'ai_agent_ask'
    ai_agent_ask_config: AiAgentAsk = ai_agent_config
    assert not ai_agent_ask_config.basic_text.model == ''
    assert not ai_agent_ask_config.basic_text.prompt_template == ''
    assert ai_agent_ask_config.basic_text.num_tokens_for_completion > -1
    assert not ai_agent_ask_config.basic_text.llm_endpoint_params == None
    assert not ai_agent_ask_config.basic_text_multi.model == ''
    assert not ai_agent_ask_config.basic_text_multi.prompt_template == ''
    assert ai_agent_ask_config.basic_text_multi.num_tokens_for_completion > -1
    assert not ai_agent_ask_config.basic_text_multi.llm_endpoint_params == None
    assert not ai_agent_ask_config.long_text.model == ''
    assert not ai_agent_ask_config.long_text.prompt_template == ''
    assert ai_agent_ask_config.long_text.num_tokens_for_completion > -1
    assert not ai_agent_ask_config.long_text.embeddings.model == ''
    assert not ai_agent_ask_config.long_text.embeddings.strategy.id == ''
    assert not ai_agent_ask_config.long_text.llm_endpoint_params == None
    assert not ai_agent_ask_config.long_text_multi.model == ''
    assert not ai_agent_ask_config.long_text_multi.prompt_template == ''
    assert ai_agent_ask_config.long_text_multi.num_tokens_for_completion > -1
    assert not ai_agent_ask_config.long_text_multi.embeddings.model == ''
    assert not ai_agent_ask_config.long_text_multi.embeddings.strategy.id == ''
    assert not ai_agent_ask_config.long_text_multi.llm_endpoint_params == None


def testGettingAITextGenAgentConfig():
    ai_agent_config: AiAgent = client.ai.get_ai_agent_default_config(
        GetAiAgentDefaultConfigMode.TEXT_GEN, language='en-US'
    )
    assert ai_agent_config.type == 'ai_agent_text_gen'
    ai_agent_text_gen_config: AiAgentTextGen = ai_agent_config
    assert not ai_agent_text_gen_config.basic_gen.llm_endpoint_params == None
    assert not ai_agent_text_gen_config.basic_gen.model == ''
    assert not ai_agent_text_gen_config.basic_gen.prompt_template == ''
    assert ai_agent_text_gen_config.basic_gen.num_tokens_for_completion > -1
    assert not ai_agent_text_gen_config.basic_gen.content_template == ''
    assert not ai_agent_text_gen_config.basic_gen.embeddings.model == ''
    assert not ai_agent_text_gen_config.basic_gen.embeddings.strategy.id == ''


def testAIExtract():
    ai_agent_config: AiAgent = client.ai.get_ai_agent_default_config(
        GetAiAgentDefaultConfigMode.EXTRACT, language='en-US'
    )
    ai_extract_agent_config: AiAgentExtract = ai_agent_config
    ai_extract_agent_basic_text_config: AiAgentExtract = AiAgentExtract(
        basic_text=ai_extract_agent_config.basic_text
    )
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=''.join([get_uuid(), '.txt']),
            parent=UploadFileAttributesParentField(id='0'),
        ),
        string_to_byte_stream(
            'My name is John Doe. I live in San Francisco. I was born in 1990. I work at Box.'
        ),
    )
    file: FileFull = uploaded_files.entries[0]
    delay_in_seconds(5)
    response: AiResponse = client.ai.create_ai_extract(
        'firstName, lastName, location, yearOfBirth, company',
        [AiItemBase(id=file.id)],
        ai_agent=ai_extract_agent_basic_text_config,
    )
    expected_response: str = (
        '{"firstName": "John", "lastName": "Doe", "location": "San Francisco", "yearOfBirth": "1990", "company": "Box"}'
    )
    assert response.answer == expected_response
    assert response.completion_reason == 'done'
    client.files.delete_file_by_id(file.id)


def testAIExtractStructuredWithFields():
    ai_agent_config: AiAgent = client.ai.get_ai_agent_default_config(
        GetAiAgentDefaultConfigMode.EXTRACT_STRUCTURED, language='en-US'
    )
    ai_extract_structured_agent_config: AiAgentExtractStructured = ai_agent_config
    ai_extract_structured_agent_basic_text_config: AiAgentExtractStructured = (
        AiAgentExtractStructured(
            basic_text=ai_extract_structured_agent_config.basic_text
        )
    )
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=''.join([get_uuid(), '.txt']),
            parent=UploadFileAttributesParentField(id='0'),
        ),
        string_to_byte_stream(
            'My name is John Doe. I was born in 4th July 1990. I am 34 years old. My hobby is guitar.'
        ),
    )
    file: FileFull = uploaded_files.entries[0]
    delay_in_seconds(5)
    response: AiExtractStructuredResponse = client.ai.create_ai_extract_structured(
        [AiItemBase(id=file.id)],
        fields=[
            CreateAiExtractStructuredFields(
                key='firstName',
                display_name='First name',
                description='Person first name',
                prompt='What is the your first name?',
                type='string',
            ),
            CreateAiExtractStructuredFields(
                key='lastName',
                display_name='Last name',
                description='Person last name',
                prompt='What is the your last name?',
                type='string',
            ),
            CreateAiExtractStructuredFields(
                key='dateOfBirth',
                display_name='Birth date',
                description='Person date of birth',
                prompt='What is the date of your birth?',
                type='date',
            ),
            CreateAiExtractStructuredFields(
                key='age',
                display_name='Age',
                description='Person age',
                prompt='How old are you?',
                type='float',
            ),
            CreateAiExtractStructuredFields(
                key='hobby',
                display_name='Hobby',
                description='Person hobby',
                prompt='What is your hobby?',
                type='multiSelect',
                options=[
                    CreateAiExtractStructuredFieldsOptionsField(key='guitar'),
                    CreateAiExtractStructuredFieldsOptionsField(key='books'),
                ],
            ),
        ],
        ai_agent=ai_extract_structured_agent_basic_text_config,
    )
    assert to_string(response.answer.get('hobby')) == to_string(['guitar'])
    assert to_string(response.answer.get('firstName')) == 'John'
    assert to_string(response.answer.get('lastName')) == 'Doe'
    assert to_string(response.answer.get('dateOfBirth')) == '1990-07-04'
    assert to_string(response.answer.get('age')) == '34'
    assert response.completion_reason == 'done'
    client.files.delete_file_by_id(file.id)


def testAIExtractStructuredWithMetadataTemplate():
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=''.join([get_uuid(), '.txt']),
            parent=UploadFileAttributesParentField(id='0'),
        ),
        string_to_byte_stream(
            'My name is John Doe. I was born in 4th July 1990. I am 34 years old. My hobby is guitar.'
        ),
    )
    file: FileFull = uploaded_files.entries[0]
    delay_in_seconds(5)
    template_key: str = ''.join(['key', get_uuid()])
    template: MetadataTemplate = client.metadata_templates.create_metadata_template(
        'enterprise',
        template_key,
        template_key=template_key,
        fields=[
            CreateMetadataTemplateFields(
                key='firstName',
                display_name='First name',
                description='Person first name',
                type=CreateMetadataTemplateFieldsTypeField.STRING,
            ),
            CreateMetadataTemplateFields(
                key='lastName',
                display_name='Last name',
                description='Person last name',
                type=CreateMetadataTemplateFieldsTypeField.STRING,
            ),
            CreateMetadataTemplateFields(
                key='dateOfBirth',
                display_name='Birth date',
                description='Person date of birth',
                type=CreateMetadataTemplateFieldsTypeField.DATE,
            ),
            CreateMetadataTemplateFields(
                key='age',
                display_name='Age',
                description='Person age',
                type=CreateMetadataTemplateFieldsTypeField.FLOAT,
            ),
            CreateMetadataTemplateFields(
                key='hobby',
                display_name='Hobby',
                description='Person hobby',
                type=CreateMetadataTemplateFieldsTypeField.MULTISELECT,
                options=[
                    CreateMetadataTemplateFieldsOptionsField(key='guitar'),
                    CreateMetadataTemplateFieldsOptionsField(key='books'),
                ],
            ),
        ],
    )
    response: AiExtractStructuredResponse = client.ai.create_ai_extract_structured(
        [AiItemBase(id=file.id)],
        metadata_template=CreateAiExtractStructuredMetadataTemplate(
            template_key=template_key, scope='enterprise'
        ),
    )
    assert to_string(response.answer.get('firstName')) == 'John'
    assert to_string(response.answer.get('lastName')) == 'Doe'
    assert to_string(response.answer.get('dateOfBirth')) == '1990-07-04T00:00:00Z'
    assert to_string(response.answer.get('age')) == '34'
    assert to_string(response.answer.get('hobby')) == to_string(['guitar'])
    assert response.completion_reason == 'done'
    client.metadata_templates.delete_metadata_template(
        DeleteMetadataTemplateScope.ENTERPRISE, template.template_key
    )
    client.files.delete_file_by_id(file.id)
