AI
==

AI allows to send an intelligence request to supported large language models and returns an answer based on the provided prompt and items.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Send AI request](#send-ai-request)
- [Send AI text generation request](#send-ai-text-generation-request)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Send AI request
------------------------

Calling the [`client.send_ai_question(items, prompt, mode)`][send-ai-question] method will send an AI request to the supported large language models. The `items` parameter is a list of items to be processed by the LLM, often files. The `prompt` provided by the client to be answered by the LLM. The prompt's length is limited to 10000 characters. The `mode`  specifies if this request is for a single or multiple items. If you select `single_item_qa` the items array can have one element only. Selecting `multiple_item_qa` allows you to provide up to 25 items.



<!-- sample post_ai_ask -->
```python
items = [{
    "id": "1582915952443",
    "type": "file",
    "content": "More information about public APIs"
}]
answer = client.send_ai_question(
    items=items, 
    prompt="What is this file?",
    mode="single_item_qa"
)
print(answer)
```

NOTE: The AI endpoint may return a 412 status code if you use for your request a file which has just been updated to the box.
It usually takes a few seconds for the file to be indexed and available for the AI endpoint.

[send-ai-question]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.send_ai_question

Send AI text generation request
------------------------

Calling the [`client.send_ai_text_gen(dialogue_history, items, prompt)`][send-ai-text-gen] method will send an AI text generation request to the supported large language models. The `dialogue_history` parameter is history of prompts and answers previously passed to the LLM. This provides additional context to the LLM in generating the response. The `items` parameter is a list of items to be processed by the LLM, often files. The `prompt` provided by the client to be answered by the LLM. The prompt's length is limited to 10000 characters.

<!-- sample post_ai_text_gen -->
```python
items = [{
    "id": "1582915952443",
    "type": "file",
    "content": "More information about public APIs"
}]
dialogue_history = [{
        "prompt": "Make my email about public APIs sound more professional",
        "answer": "Here is the first draft of your professional email about public APIs",
        "created_at": "2013-12-12T10:53:43-08:00"
    },
    {
        "prompt": "Can you add some more information?",
        "answer": "Public API schemas provide necessary information to integrate with APIs...",
        "created_at": "2013-12-12T11:20:43-08:00"
}]
answer = client.send_ai_text_gen(
    dialogue_history=dialogue_history,
    items=items,
    prompt="Write an email to a client about the importance of public APIs."
)
print(answer)
```

[send-ai-text-gen]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.send_ai_text_gen
