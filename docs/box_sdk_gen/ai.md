# AiManager

- [Ask question](#ask-question)
- [Generate text](#generate-text)
- [Get AI agent default configuration](#get-ai-agent-default-configuration)
- [Extract metadata (freeform)](#extract-metadata-freeform)
- [Extract metadata (structured)](#extract-metadata-structured)

## Ask question

Sends an AI request to supported LLMs and returns an answer specifically focused on the user's question given the provided context.

This operation is performed by calling function `create_ai_ask`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-ai-ask/).

<!-- sample post_ai_ask -->

```python
client.ai.create_ai_ask(CreateAiAskMode.SINGLE_ITEM_QA, 'Which direction does the Sun rise?', [AiItemAsk(id=file_to_ask.id, type=AiItemAskTypeField.FILE, content='The Sun rises in the east')], ai_agent=ai_ask_agent_basic_text_config)
```

### Arguments

- mode `CreateAiAskMode`
  - Box AI handles text documents with text representations up to 1MB in size, or a maximum of 25 files, whichever comes first. If the text file size exceeds 1MB, the first 1MB of text representation will be processed. Box AI handles image documents with a resolution of 1024 x 1024 pixels, with a maximum of 5 images or 5 pages for multi-page images. If the number of image or image pages exceeds 5, the first 5 images or pages will be processed. If you set mode parameter to `single_item_qa`, the items array can have one element only. Currently Box AI does not support multi-modal requests. If both images and text are sent Box AI will only process the text.
- prompt `str`
  - The prompt provided by the client to be answered by the LLM. The prompt's length is limited to 10000 characters.
- items `List[AiItemAsk]`
  - The items to be processed by the LLM, often files.
- dialogue_history `Optional[List[AiDialogueHistory]]`
  - The history of prompts and answers previously passed to the LLM. This provides additional context to the LLM in generating the response.
- include_citations `Optional[bool]`
  - A flag to indicate whether citations should be returned.
- ai_agent `Optional[AiAskAgent]`
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Optional[AiResponseFull]`.

A successful response including the answer from the LLM.No content is available to answer the question. This is returned when the request item is a hub, but content in the hubs is not indexed. To ensure content in the hub is indexed, make sure Box AI for Hubs in the Admin Console was enabled before hub creation.

## Generate text

Sends an AI request to supported Large Language Models (LLMs) and returns generated text based on the provided prompt.

This operation is performed by calling function `create_ai_text_gen`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-ai-text-gen/).

<!-- sample post_ai_text_gen -->

```python
client.ai.create_ai_text_gen('Paraphrase the documents', [CreateAiTextGenItems(id=file_to_ask.id, type=CreateAiTextGenItemsTypeField.FILE, content='The Earth goes around the Sun. The Sun rises in the east in the morning.')], dialogue_history=[AiDialogueHistory(prompt='What does the earth go around?', answer='The Sun', created_at=date_time_from_string('2021-01-01T00:00:00Z')), AiDialogueHistory(prompt='On Earth, where does the Sun rise?', answer='east', created_at=date_time_from_string('2021-01-01T00:00:00Z'))])
```

### Arguments

- prompt `str`
  - The prompt provided by the client to be answered by the LLM. The prompt's length is limited to 10000 characters.
- items `List[CreateAiTextGenItems]`
  - The items to be processed by the LLM, often files. The array can include **exactly one** element. **Note**: Box AI handles documents with text representations up to 1MB in size. If the file size exceeds 1MB, the first 1MB of text representation will be processed.
- dialogue_history `Optional[List[AiDialogueHistory]]`
  - The history of prompts and answers previously passed to the LLM. This parameter provides the additional context to the LLM when generating the response.
- ai_agent `Optional[AiTextGenAgent]`
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiResponse`.

A successful response including the answer from the LLM.

## Get AI agent default configuration

Get the AI agent default config.

This operation is performed by calling function `get_ai_agent_default_config`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-ai-agent-default/).

<!-- sample get_ai_agent_default -->

```python
client.ai.get_ai_agent_default_config(GetAiAgentDefaultConfigMode.ASK, language='en-US')
```

### Arguments

- mode `GetAiAgentDefaultConfigMode`
  - The mode to filter the agent config to return.
- language `Optional[str]`
  - The ISO language code to return the agent config for. If the language is not supported the default agent config is returned.
- model `Optional[str]`
  - The model to return the default agent config for.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiAgent`.

A successful response including the default agent configuration.
This response can be one of the following four objects:

- AI agent for questions
- AI agent for text generation
- AI agent for freeform metadata extraction
- AI agent for structured metadata extraction.
  The response depends on the agent configuration requested in this endpoint.

## Extract metadata (freeform)

Sends an AI request to supported Large Language Models (LLMs) and extracts metadata in form of key-value pairs.
In this request, both the prompt and the output can be freeform.
Metadata template setup before sending the request is not required.

This operation is performed by calling function `create_ai_extract`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-ai-extract/).

<!-- sample post_ai_extract -->

```python
client.ai.create_ai_extract('firstName, lastName, location, yearOfBirth, company', [AiItemBase(id=file.id)], ai_agent=ai_extract_agent_basic_text_config)
```

### Arguments

- prompt `str`
  - The prompt provided to a Large Language Model (LLM) in the request. The prompt can be up to 10000 characters long and it can be an XML or a JSON schema.
- items `List[AiItemBase]`
  - The items that LLM will process. Currently, you can use files only.
- ai_agent `Optional[AiExtractAgent]`
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiResponse`.

A response including the answer from the LLM.

## Extract metadata (structured)

Sends an AI request to supported Large Language Models (LLMs) and returns extracted metadata as a set of key-value pairs.

To define the extraction structure, provide either a metadata template or a list of fields. To learn more about creating templates, see [Creating metadata templates in the Admin Console](https://support.box.com/hc/en-us/articles/360044194033-Customizing-Metadata-Templates)
or use the [metadata template API](https://developer.box.com/guides/metadata/templates/create).

This endpoint also supports [Enhanced Extract Agent](https://developer.box.com/guides/box-ai/ai-tutorials/extract-metadata-structured#enhanced-extract-agent).

For information about supported file formats and languages, see the [Extract metadata from file (structured)](https://developer.box.com/guides/box-ai/ai-tutorials/extract-metadata-structured) API guide.

This operation is performed by calling function `create_ai_extract_structured`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-ai-extract-structured/).

<!-- sample post_ai_extract_structured -->

```python
client.ai.create_ai_extract_structured([AiItemBase(id=file.id)], fields=[CreateAiExtractStructuredFields(key='firstName', display_name='First name', description='Person first name', prompt='What is the your first name?', type='string'), CreateAiExtractStructuredFields(key='lastName', display_name='Last name', description='Person last name', prompt='What is the your last name?', type='string'), CreateAiExtractStructuredFields(key='dateOfBirth', display_name='Birth date', description='Person date of birth', prompt='What is the date of your birth?', type='date'), CreateAiExtractStructuredFields(key='age', display_name='Age', description='Person age', prompt='How old are you?', type='float'), CreateAiExtractStructuredFields(key='hobby', display_name='Hobby', description='Person hobby', prompt='What is your hobby?', type='multiSelect', options=[CreateAiExtractStructuredFieldsOptionsField(key='guitar'), CreateAiExtractStructuredFieldsOptionsField(key='books')])], ai_agent=ai_extract_structured_agent_basic_text_config)
```

### Arguments

- items `List[AiItemBase]`
  - The items to be processed by the LLM. Currently you can use files only.
- metadata_template `Optional[CreateAiExtractStructuredMetadataTemplate]`
  - The metadata template containing the fields to extract. For your request to work, you must provide either `metadata_template` or `fields`, but not both.
- fields `Optional[List[CreateAiExtractStructuredFields]]`
  - The fields to be extracted from the provided items. For your request to work, you must provide either `metadata_template` or `fields`, but not both.
- include_confidence_score `Optional[bool]`
  - A flag to indicate whether confidence scores for every extracted field should be returned.
- ai_agent `Optional[AiExtractStructuredAgent]`
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiExtractStructuredResponse`.

A successful response including the answer from the LLM.
