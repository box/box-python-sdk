# WorkflowsManager

- [List workflows](#list-workflows)
- [Starts workflow based on request body](#starts-workflow-based-on-request-body)

## List workflows

Returns list of workflows that act on a given `folder ID`, and
have a flow with a trigger type of `WORKFLOW_MANUAL_START`.

You application must be authorized to use the `Manage Box Relay` application
scope within the developer console in to use this endpoint.

This operation is performed by calling function `get_workflows`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-workflows/).

<!-- sample get_workflows -->

```python
admin_client.workflows.get_workflows(workflow_folder_id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`.
- trigger_type `Optional[str]`
  - Type of trigger to search for.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Workflows`.

Returns the workflow.

## Starts workflow based on request body

Initiates a flow with a trigger type of `WORKFLOW_MANUAL_START`.

You application must be authorized to use the `Manage Box Relay` application
scope within the developer console.

This operation is performed by calling function `start_workflow`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-workflows-id-start/).

<!-- sample post_workflows_id_start -->

```python
admin_client.workflows.start_workflow(workflow_to_run.id, StartWorkflowFlow(type='flow', id=workflow_to_run.flows[0].id), [StartWorkflowFiles(type=StartWorkflowFilesTypeField.FILE, id=workflow_file_id)], StartWorkflowFolder(type=StartWorkflowFolderTypeField.FOLDER, id=workflow_folder_id), type=StartWorkflowType.WORKFLOW_PARAMETERS)
```

### Arguments

- workflow_id `str`
  - The ID of the workflow. Example: "12345"
- type `Optional[StartWorkflowType]`
  - The type of the parameters object.
- flow `StartWorkflowFlow`
  - The flow that will be triggered.
- files `List[StartWorkflowFiles]`
  - The array of files for which the workflow should start. All files must be in the workflow's configured folder.
- folder `StartWorkflowFolder`
  - The folder object for which the workflow is configured.
- outcomes `Optional[List[Outcome]]`
  - A configurable outcome the workflow should complete.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Starts the workflow.
