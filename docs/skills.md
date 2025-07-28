# SkillsManager

- [List Box Skill cards on file](#list-box-skill-cards-on-file)
- [Create Box Skill cards on file](#create-box-skill-cards-on-file)
- [Update Box Skill cards on file](#update-box-skill-cards-on-file)
- [Remove Box Skill cards from file](#remove-box-skill-cards-from-file)
- [Update all Box Skill cards on file](#update-all-box-skill-cards-on-file)

## List Box Skill cards on file

List the Box Skills metadata cards that are attached to a file.

This operation is performed by calling function `get_box_skill_cards_on_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-metadata-global-boxSkillsCards/).

<!-- sample get_files_id_metadata_global_boxSkillsCards -->

```python
client.skills.get_box_skill_cards_on_file(file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `SkillCardsMetadata`.

Returns all the metadata associated with a file.

This API does not support pagination and will therefore always return
all of the metadata associated to the file.

## Create Box Skill cards on file

Applies one or more Box Skills metadata cards to a file.

This operation is performed by calling function `create_box_skill_cards_on_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-files-id-metadata-global-boxSkillsCards/).

<!-- sample post_files_id_metadata_global_boxSkillsCards -->

```python
client.skills.create_box_skill_cards_on_file(file.id, cards_to_create)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- cards `List[Union[KeywordSkillCard, TimelineSkillCard, TranscriptSkillCard, StatusSkillCard]]`
  - A list of Box Skill cards to apply to this file.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `SkillCardsMetadata`.

Returns the instance of the template that was applied to the file,
including the data that was applied to the template.

## Update Box Skill cards on file

Updates one or more Box Skills metadata cards to a file.

This operation is performed by calling function `update_box_skill_cards_on_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-files-id-metadata-global-boxSkillsCards/).

<!-- sample put_files_id_metadata_global_boxSkillsCards -->

```python
client.skills.update_box_skill_cards_on_file(
    file.id,
    [
        UpdateBoxSkillCardsOnFileRequestBody(
            op=UpdateBoxSkillCardsOnFileRequestBodyOpField.REPLACE,
            path="/cards/0",
            value=card_to_update,
        )
    ],
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- request_body `List[UpdateBoxSkillCardsOnFileRequestBody]`
  - Request body of updateBoxSkillCardsOnFile method
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `SkillCardsMetadata`.

Returns the updated metadata template, with the
custom template data included.

## Remove Box Skill cards from file

Removes any Box Skills cards metadata from a file.

This operation is performed by calling function `delete_box_skill_cards_from_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-files-id-metadata-global-boxSkillsCards/).

<!-- sample delete_files_id_metadata_global_boxSkillsCards -->

```python
client.skills.delete_box_skill_cards_from_file(file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the cards are
successfully deleted.

## Update all Box Skill cards on file

An alternative method that can be used to overwrite and update all Box Skill
metadata cards on a file.

This operation is performed by calling function `update_all_skill_cards_on_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-skill-invocations-id/).

_Currently we don't have an example for calling `update_all_skill_cards_on_file` in integration tests_

### Arguments

- skill_id `str`
  - The ID of the skill to apply this metadata for. Example: "33243242"
- status `UpdateAllSkillCardsOnFileStatus`
  - Defines the status of this invocation. Set this to `success` when setting Skill cards.
- metadata `UpdateAllSkillCardsOnFileMetadata`
  - The metadata to set for this skill. This is a list of Box Skills cards. These cards will overwrite any existing Box skill cards on the file.
- file `UpdateAllSkillCardsOnFileFile`
  - The file to assign the cards to.
- file_version `Optional[UpdateAllSkillCardsOnFileFileVersion]`
  - The optional file version to assign the cards to.
- usage `Optional[UpdateAllSkillCardsOnFileUsage]`
  - A descriptor that defines what items are affected by this call. Set this to the default values when setting a card to a `success` state, and leave it out in most other situations.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the card has been successfully updated.
