# AutomateWorkflowsManager

- [List Automate workflows defined as callable actions](#list-automate-workflows-defined-as-callable-actions)
- [Start Automate workflow](#start-automate-workflow)

## List Automate workflows defined as callable actions

Returns workflow actions from Automate for a folder, using the
`WORKFLOW` action category.

This operation is performed by calling function `get_automate_workflows_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-automate-workflows/).

<!-- sample get_automate_workflows_v2026.0 -->

```python
admin_client.automate_workflows.get_automate_workflows_v2026_r0(workflow_folder_id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AutomateWorkflowsV2026R0`.

Returns workflow actions that can be manually started.

## Start Automate workflow

Starts an Automate workflow manually by using a workflow action ID and file IDs.

This operation is performed by calling function `create_automate_workflow_start_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-automate-workflows-id-start/).

<!-- sample post_automate_workflows_id_start_v2026.0 -->

```python
admin_client.automate_workflows.create_automate_workflow_start_v2026_r0(
    workflow_action.workflow.id, workflow_action.id, [workflow_file_id]
)
```

### Arguments

- workflow_id `str`
  - The ID of the workflow. Example: "12345"
- workflow_action_id `str`
  - The callable action ID used to trigger the selected workflow.
- file_ids `List[str]`
  - The files to process with the selected workflow.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Starts the workflow.
