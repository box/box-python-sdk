# NotesManager

- [Convert content to Box Note](#convert-content-to-box-note)

## Convert content to Box Note

Creates a Box Note (`.boxnote` file) from supported source content. See the `content_format` field for supported formats.

This operation is performed by calling function `create_note_convert_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-notes-convert/).

<!-- sample post_notes_convert_v2026.0 -->

```python
client.notes.create_note_convert_v2026_r0(
    markdown_content,
    FolderReferenceV2026R0(id="0"),
    note_name,
    content_format=CreateNoteConvertV2026R0ContentFormat.MARKDOWN,
)
```

### Arguments

- content `str`
  - The content to convert to a note. See the `content_format` field for supported formats.
- content_format `CreateNoteConvertV2026R0ContentFormat`
  - Format of the content to convert.
- parent `FolderReferenceV2026R0`
- name `str`
  - The name for the created note. The `.boxnote` extension is appended automatically.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `NotesConvertResponseV2026R0`.

The note was created successfully.
