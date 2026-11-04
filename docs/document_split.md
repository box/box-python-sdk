# DocumentSplitManager

- [Create Document Split job](#create-document-split-job)
- [List Document Split jobs](#list-document-split-jobs)
- [Get Document Split job by ID](#get-document-split-job-by-id)

## Create Document Split job

Initiates a Document Split job for the supplied source file. The job runs
asynchronously; clients can poll the returned job ID to track progress.

All split-specific input lives under `split_input`. When
`split_input.split_type` is `manual`, provide
`split_input.split_definition` (continuous page ranges; `version` may be
omitted or `v_1`). When `split_input.split_type` is `page_selection`,
provide `split_input.page_selection` (non-linear page segments; `version`
may be omitted or `v_2`). `split_input.prompt` must not be provided for
either of those variants. When `split_input.split_type` is `smart`,
`split_input.prompt` is required and neither
`split_input.split_definition` nor `split_input.page_selection` must be
provided.

This operation is performed by calling function `create_document_split_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-document-splits/).

<!-- sample post_document_splits_v2026.0 -->

```python
client.document_split.create_document_split_v2026_r0(
    file.id,
    folder.id,
    CreateDocumentSplitV2026R0InputSource.API,
    DocumentSplitCreateRequestManualV2026R0(
        split_type=DocumentSplitCreateRequestManualV2026R0SplitTypeField.MANUAL,
        split_definition=[DocumentSplitPageRangeV2026R0(start=1, end=1)],
    ),
    external_id=external_id,
)
```

### Arguments

- source_file_id `str`
  - The ID of the source file to split.
- destination_folder_id `str`
  - The ID of the folder where the resulting files will be uploaded.
- input_source `CreateDocumentSplitV2026R0InputSource`
  - The system that initiated the request, used for analytics and traceability.
- split_input `DocumentSplitCreateRequestTypeV2026R0`

- external_id `Optional[str]`
  - An optional identifier supplied by the caller for this Document Split job. The value is returned on job responses for correlation only. It is not a Box resource ID, is not required to be unique, and cannot be used to look up the job.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DocumentSplitCreateResponseV2026R0`.

The Document Split job was accepted for processing. Returns a reference
to the newly created job.

## List Document Split jobs

Returns a paginated list of Document Split jobs accessible to the
authenticated user.

This operation is performed by calling function `get_document_splits_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-document-splits/).

<!-- sample get_document_splits_v2026.0 -->

```python
client.document_split.get_document_splits_v2026_r0(limit=10)
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DocumentSplitsV2026R0`.

Returns a paginated list of Document Split jobs.

## Get Document Split job by ID

Returns details for a single Document Split job identified by its ID,
including the current status, the input definition, and any output files
produced by the job.

This operation is performed by calling function `get_document_split_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-document-splits-id/).

<!-- sample get_document_splits_id_v2026.0 -->

```python
client.document_split.get_document_split_by_id_v2026_r0(created_document_split.id)
```

### Arguments

- document_split_id `str`
  - The unique identifier for the Document Split job. Example: "1748426"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DocumentSplitV2026R0`.

Returns the Document Split job.
