# ShuttleManager

- [List shuttle systems](#list-shuttle-systems)
- [Create shuttle system](#create-shuttle-system)
- [Get shuttle system by ID](#get-shuttle-system-by-id)
- [Update shuttle system](#update-shuttle-system)
- [Delete shuttle system](#delete-shuttle-system)
- [Issue registration token for Windows system](#issue-registration-token-for-windows-system)
- [List shuttle jobs](#list-shuttle-jobs)
- [Create shuttle job](#create-shuttle-job)
- [Get shuttle job by ID](#get-shuttle-job-by-id)
- [Update shuttle job](#update-shuttle-job)
- [Delete shuttle job](#delete-shuttle-job)
- [Start shuttle job](#start-shuttle-job)
- [Stop shuttle job](#stop-shuttle-job)
- [Prepare migration](#prepare-migration)
- [List shuttle runs](#list-shuttle-runs)
- [Get shuttle run by ID](#get-shuttle-run-by-id)
- [List shuttle job schedules](#list-shuttle-job-schedules)
- [Create shuttle job schedule](#create-shuttle-job-schedule)
- [Get shuttle job schedule](#get-shuttle-job-schedule)
- [Update shuttle job schedule](#update-shuttle-job-schedule)
- [Delete shuttle job schedule](#delete-shuttle-job-schedule)
- [List shuttle path mappings](#list-shuttle-path-mappings)
- [Create shuttle path mapping](#create-shuttle-path-mapping)
- [Get shuttle path mapping by ID](#get-shuttle-path-mapping-by-id)
- [Update shuttle path mapping](#update-shuttle-path-mapping)
- [Delete shuttle path mapping](#delete-shuttle-path-mapping)
- [Create shuttle path mapping import](#create-shuttle-path-mapping-import)
- [Create shuttle subject mapping import](#create-shuttle-subject-mapping-import)
- [List shuttle subject mappings](#list-shuttle-subject-mappings)
- [Create shuttle subject mapping](#create-shuttle-subject-mapping)
- [Get shuttle subject mapping by ID](#get-shuttle-subject-mapping-by-id)
- [Update shuttle subject mapping](#update-shuttle-subject-mapping)
- [Delete shuttle subject mapping](#delete-shuttle-subject-mapping)
- [List shuttle discovered subjects](#list-shuttle-discovered-subjects)
- [List shuttle path entries](#list-shuttle-path-entries)
- [List shuttle mapping errors](#list-shuttle-mapping-errors)
- [List shuttle reports](#list-shuttle-reports)
- [Create shuttle report](#create-shuttle-report)
- [Get shuttle report by ID](#get-shuttle-report-by-id)

## List shuttle systems

Returns a paginated list of shuttle systems accessible to the
authenticated user.

This operation is performed by calling function `get_shuttle_systems_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-systems/).

_Currently we don't have an example for calling `get_shuttle_systems_v2026_r0` in integration tests_

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

This function returns a value of type `ShuttleSystemsV2026R0`.

Returns a paginated list of shuttle systems.

## Create shuttle system

Creates a new shuttle system. Only Windows agent systems can be created
through the public API; other system types must be configured through the
Shuttle application.

This operation is performed by calling function `create_shuttle_system_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-systems/).

_Currently we don't have an example for calling `create_shuttle_system_v2026_r0` in integration tests_

### Arguments

- name `str`
  - The display name for the new shuttle system.
- system_type `CreateShuttleSystemV2026R0SystemType`
  - The public system type identifier for the new shuttle system. Only `windows` is currently supported through the public API.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleSystemV2026R0`.

Returns the newly created shuttle system.

## Get shuttle system by ID

Returns details for a single shuttle system identified by its ID,
including its type and connection state.

This operation is performed by calling function `get_shuttle_system_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-systems-id/).

_Currently we don't have an example for calling `get_shuttle_system_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_system_id `str`
  - The unique identifier for the shuttle system. Example: "6a315c0754833bfc5df067bf"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleSystemV2026R0`.

Returns the shuttle system.

## Update shuttle system

Updates the mutable properties of an existing shuttle system identified by
its ID. Only the fields supplied in the request body are changed.

This operation is performed by calling function `update_shuttle_system_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/put-shuttle-systems-id/).

_Currently we don't have an example for calling `update_shuttle_system_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_system_id `str`
  - The unique identifier for the shuttle system. Example: "6a315c0754833bfc5df067bf"
- name `Optional[str]`
  - The updated display name for the shuttle system.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleSystemV2026R0`.

Returns the updated shuttle system.

## Delete shuttle system

Permanently deletes the shuttle system identified by its ID. This does not
affect content that has already been migrated.

This operation is performed by calling function `delete_shuttle_system_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/delete-shuttle-systems-id/).

_Currently we don't have an example for calling `delete_shuttle_system_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_system_id `str`
  - The unique identifier for the shuttle system. Example: "6a315c0754833bfc5df067bf"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the shuttle system was successfully
deleted.

## Issue registration token for Windows system

Issues a new installation token for the Windows shuttle system identified
by its ID. Paste the returned token into the Windows agent installer to
register the agent with this system.

This operation is performed by calling function `create_shuttle_system_issue_registration_token_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-systems-id-issue-registration-token/).

_Currently we don't have an example for calling `create_shuttle_system_issue_registration_token_v2026_r0` in integration tests_

### Arguments

- shuttle_system_id `str`
  - The unique identifier for the shuttle system. Example: "6a315c0754833bfc5df067bf"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleAgentCredentialsV2026R0`.

Returns the agent installation credentials for the Windows system.

## List shuttle jobs

Returns a paginated list of shuttle jobs accessible to the authenticated
user.

This operation is performed by calling function `get_shuttle_jobs_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-jobs/).

_Currently we don't have an example for calling `get_shuttle_jobs_v2026_r0` in integration tests_

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

This function returns a value of type `ShuttleJobsV2026R0`.

Returns a paginated list of shuttle jobs.

## Create shuttle job

Creates a new shuttle job that describes a migration from the given source
system into Box.

This operation is performed by calling function `create_shuttle_job_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-jobs/).

_Currently we don't have an example for calling `create_shuttle_job_v2026_r0` in integration tests_

### Arguments

- name `str`
  - The human-readable name of the shuttle job.
- job_type `CreateShuttleJobV2026R0JobType`
  - The type of work the shuttle job performs.
- source_system_id `str`
  - The unique identifier of the source system to migrate from.
- comment `Optional[str]`
  - An optional free-form comment describing the shuttle job.
- tags `Optional[List[str]]`
  - A list of free-form tags associated with the shuttle job.
- account_mapping `Optional[CreateShuttleJobV2026R0AccountMapping]`
  - The account mapping configuration that controls how source identities and permissions are translated into Box. When this object is omitted, the job is created with `is_enabled` set to `false`.
- settings `Optional[CreateShuttleJobV2026R0Settings]`
  - The tunable settings that control how the shuttle job runs.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleJobV2026R0`.

Returns the newly created shuttle job.

## Get shuttle job by ID

Returns details for a single shuttle job identified by its ID, including
its current state, mapping-preparation state, and configured source system.

This operation is performed by calling function `get_shuttle_job_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-jobs-id/).

_Currently we don't have an example for calling `get_shuttle_job_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_job_id `str`
  - The unique identifier for the shuttle job. Example: "6a3ba68e810d9156194530a1"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleJobV2026R0`.

Returns the shuttle job.

## Update shuttle job

Updates the mutable properties of an existing shuttle job identified by its
ID. Only the fields supplied in the request body are changed.

This operation is performed by calling function `update_shuttle_job_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/put-shuttle-jobs-id/).

_Currently we don't have an example for calling `update_shuttle_job_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_job_id `str`
  - The unique identifier for the shuttle job. Example: "6a3ba68e810d9156194530a1"
- name `Optional[str]`
  - The human-readable name of the shuttle job.
- comment `Optional[str]`
  - An optional free-form comment describing the shuttle job.
- tags `Optional[List[str]]`
  - A list of free-form tags associated with the shuttle job.
- account_mapping `Optional[UpdateShuttleJobByIdV2026R0AccountMapping]`
  - The account mapping configuration that controls how source identities and permissions are translated into Box.
- settings `Optional[UpdateShuttleJobByIdV2026R0Settings]`
  - The tunable settings that control how the shuttle job runs.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleJobV2026R0`.

Returns the updated shuttle job.

## Delete shuttle job

Permanently deletes the shuttle job identified by its ID. This does not
affect content that has already been migrated.

This operation is performed by calling function `delete_shuttle_job_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/delete-shuttle-jobs-id/).

_Currently we don't have an example for calling `delete_shuttle_job_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_job_id `str`
  - The unique identifier for the shuttle job. Example: "6a3ba68e810d9156194530a1"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the shuttle job was successfully deleted.

## Start shuttle job

Starts the job in the given mode. When no body is provided the job runs in
simulation mode.

This operation is performed by calling function `create_shuttle_job_start_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-jobs-id-start/).

_Currently we don't have an example for calling `create_shuttle_job_start_v2026_r0` in integration tests_

### Arguments

- shuttle_job_id `str`
  - The unique identifier for the shuttle job. Example: "6a3ba68e810d9156194530a1"
- mode `Optional[CreateShuttleJobStartV2026R0Mode]`
  - The run mode. Defaults to simulation when omitted.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

The shuttle job was accepted and is being started.

## Stop shuttle job

Stops a running shuttle job identified by its ID. Any work already in
progress is allowed to finish before the job transitions to a stopped
state.

This operation is performed by calling function `create_shuttle_job_stop_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-jobs-id-stop/).

_Currently we don't have an example for calling `create_shuttle_job_stop_v2026_r0` in integration tests_

### Arguments

- shuttle_job_id `str`
  - The unique identifier for the shuttle job. Example: "6a3ba68e810d9156194530a1"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

The shuttle job was accepted and is being stopped.

## Prepare migration

Validates the configured account and path mappings before a transfer. Only
relevant when account mapping is enabled.

This operation is performed by calling function `create_shuttle_job_prepare_migration_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-jobs-id-prepare-migration/).

_Currently we don't have an example for calling `create_shuttle_job_prepare_migration_v2026_r0` in integration tests_

### Arguments

- shuttle_job_id `str`
  - The unique identifier for the shuttle job. Example: "6a3ba68e810d9156194530a1"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

The migration preparation was accepted and is being processed.

## List shuttle runs

Returns a paginated list of runs for the shuttle job identified by
`job_id`.

This operation is performed by calling function `get_shuttle_runs_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-runs/).

_Currently we don't have an example for calling `get_shuttle_runs_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job whose runs to list.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleRunsV2026R0`.

Returns a paginated list of shuttle runs.

## Get shuttle run by ID

Returns details for a single shuttle run identified by its ID, including
its mode, state, timing, and transfer statistics.

This operation is performed by calling function `get_shuttle_run_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-runs-id/).

_Currently we don't have an example for calling `get_shuttle_run_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_run_id `str`
  - The unique identifier for the shuttle run, in the form `{job_id}:{run_number}`. Example: "6a3ba68e810d9156194530a1:42"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleRunV2026R0`.

Returns the shuttle run.

## List shuttle job schedules

Returns a paginated list of schedules for the shuttle job identified by
`job_id`.

This operation is performed by calling function `get_shuttle_job_schedules_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-job-schedules/).

_Currently we don't have an example for calling `get_shuttle_job_schedules_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job whose schedules to list.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleJobSchedulesV2026R0`.

Returns a paginated list of shuttle job schedules.

## Create shuttle job schedule

Creates a schedule that starts runs of the shuttle job identified by
`job_id`. The schedule starts a run either at a wall-clock time or after
another job's run meets a condition. Schedules cannot start a run in
`scan` mode.

This operation is performed by calling function `create_shuttle_job_schedule_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-job-schedules/).

_Currently we don't have an example for calling `create_shuttle_job_schedule_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job this schedule belongs to.
- run_mode `CreateShuttleJobScheduleV2026R0RunMode`
  - The kind of run the schedule starts. `scan` is not a valid schedule run mode.
- state `Optional[CreateShuttleJobScheduleV2026R0State]`
  - Whether the schedule is active. When omitted, defaults to `enabled`.
- description `Optional[str]`
  - An optional human-readable description of the schedule.
- trigger `ShuttleJobScheduleTriggerV2026R0`

- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleJobScheduleV2026R0`.

Returns the newly created shuttle job schedule.

## Get shuttle job schedule

Retrieves the shuttle job schedule identified by its ID.

This operation is performed by calling function `get_shuttle_job_schedule_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-job-schedules-id/).

_Currently we don't have an example for calling `get_shuttle_job_schedule_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_job_schedule_id `str`
  - The unique identifier for the shuttle job schedule. Example: "7c1ba68e810d9156194530b2"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleJobScheduleV2026R0`.

Returns the shuttle job schedule.

## Update shuttle job schedule

Updates the mutable properties of an existing shuttle job schedule
identified by its ID. Only the fields supplied in the request body are
changed. The owning job cannot be changed.

This operation is performed by calling function `update_shuttle_job_schedule_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/put-shuttle-job-schedules-id/).

_Currently we don't have an example for calling `update_shuttle_job_schedule_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_job_schedule_id `str`
  - The unique identifier for the shuttle job schedule. Example: "7c1ba68e810d9156194530b2"
- state `Optional[UpdateShuttleJobScheduleByIdV2026R0State]`
  - Whether the schedule is active.
- run_mode `Optional[UpdateShuttleJobScheduleByIdV2026R0RunMode]`
  - The kind of run the schedule starts. `scan` is not a valid schedule run mode.
- description `Optional[str]`
  - An optional human-readable description of the schedule.
- trigger `Optional[ShuttleJobScheduleTriggerV2026R0]`

- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleJobScheduleV2026R0`.

Returns the updated shuttle job schedule.

## Delete shuttle job schedule

Permanently deletes the shuttle job schedule identified by its ID. This
does not affect runs that have already started.

This operation is performed by calling function `delete_shuttle_job_schedule_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/delete-shuttle-job-schedules-id/).

_Currently we don't have an example for calling `delete_shuttle_job_schedule_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_job_schedule_id `str`
  - The unique identifier for the shuttle job schedule. Example: "7c1ba68e810d9156194530b2"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the shuttle job schedule was
successfully deleted.

## List shuttle path mappings

Returns a paginated list of path mappings for the shuttle job identified
by `job_id`.

This operation is performed by calling function `get_shuttle_path_mappings_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-path-mappings/).

_Currently we don't have an example for calling `get_shuttle_path_mappings_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job whose path mappings to list.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttlePathMappingsV2026R0`.

Returns a paginated list of shuttle path mappings.

## Create shuttle path mapping

Creates a path mapping that connects a source location on the migrated
system to a destination in Box for the given shuttle job.

This operation is performed by calling function `create_shuttle_path_mapping_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-path-mappings/).

_Currently we don't have an example for calling `create_shuttle_path_mapping_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job this mapping belongs to.
- is_path_skipped `Optional[bool]`
  - Whether this source path should be skipped during the migration. Defaults to `false`.
- source `ShuttlePathMappingLocationInputV2026R0`

- target `Optional[ShuttlePathMappingTargetLocationInputV2026R0]`
  - The destination location to migrate to. Omit or set to `null` when the source path is skipped.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttlePathMappingV2026R0`.

Returns the newly created shuttle path mapping.

## Get shuttle path mapping by ID

Returns details for a single shuttle path mapping identified by its ID,
including the source location and destination, if any.

This operation is performed by calling function `get_shuttle_path_mapping_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-path-mappings-id/).

_Currently we don't have an example for calling `get_shuttle_path_mapping_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_path_mapping_id `str`
  - The unique identifier for the shuttle path mapping. Example: "6a3ba7a24ea17bc9461eeacd"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttlePathMappingV2026R0`.

Returns the shuttle path mapping.

## Update shuttle path mapping

Updates the mutable properties of an existing shuttle path mapping
identified by its ID. Only the fields supplied in the request body are
changed.

This operation is performed by calling function `update_shuttle_path_mapping_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/put-shuttle-path-mappings-id/).

_Currently we don't have an example for calling `update_shuttle_path_mapping_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_path_mapping_id `str`
  - The unique identifier for the shuttle path mapping. Example: "6a3ba7a24ea17bc9461eeacd"
- is_path_skipped `Optional[bool]`
  - Whether this source path should be skipped during the migration.
- source `Optional[ShuttlePathMappingLocationInputV2026R0]`

- target `Optional[ShuttlePathMappingTargetLocationInputV2026R0]`
  - The destination location to migrate to. Set to `null` to clear the destination, for example when skipping the source path.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttlePathMappingV2026R0`.

Returns the updated shuttle path mapping.

## Delete shuttle path mapping

Permanently deletes the shuttle path mapping identified by its ID. This
does not affect content that has already been migrated.

This operation is performed by calling function `delete_shuttle_path_mapping_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/delete-shuttle-path-mappings-id/).

_Currently we don't have an example for calling `delete_shuttle_path_mapping_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_path_mapping_id `str`
  - The unique identifier for the shuttle path mapping. Example: "6a3ba7a24ea17bc9461eeacd"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the shuttle path mapping was
successfully deleted.

## Create shuttle path mapping import

Accepts a spreadsheet of path mappings, already stored in Box, and replaces
the job's path mappings.
A file that is not a mapping workbook, or that exceeds the size or row
limits (10 MiB Box download limit; 100,000 mapping rows), returns `400`
synchronously and leaves the job unchanged.
An accepted import always replaces every path mapping on the job. When all
rows are valid the workbook is deployed in full. When any row is invalid
the job ends with no path mappings and `mapping_state` becomes
`paths_import_rejected` until the next import or the next manual
path-mapping change. Row problems are listed by
`GET /shuttle_mapping_errors?job_id=…` with category `path_import`, messages
of the form `Row N: …`, at most 500 entries plus one overflow entry.
Validation and deployment are asynchronous after acceptance. Poll
`GET /shuttle_jobs/{shuttle_job_id}` while `mapping_state` is
`importing_paths`. Only one import may be in flight per job.

This operation is performed by calling function `create_shuttle_path_mapping_import_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-path-mapping-imports/).

_Currently we don't have an example for calling `create_shuttle_path_mapping_import_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job whose path mappings are replaced.
- file_id `str`
  - The unique identifier of the Box file holding the mapping workbook. The file is read as the calling user, so it must live somewhere that user can download from.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

The import was accepted. Validation and deployment continue
asynchronously. Poll `GET /shuttle_jobs/{shuttle_job_id}` until
`mapping_state` is no longer `importing_paths`. A rejected import ends
with `mapping_state` `paths_import_rejected` and an empty path-mapping
list; a successful import moves on to a later mapping-preparation state
such as `paths_ready` or `ready`.

## Create shuttle subject mapping import

Accepts a spreadsheet of subject (user and group) mappings, already stored
in Box, and replaces the job's subject mappings.
A file that is not a subject-mapping workbook, or that exceeds the size or
row limits (10 MiB Box download limit; 50,000 mapping rows), returns `400`
synchronously and leaves the job unchanged.
An accepted import always replaces every subject mapping on the job. When
all rows are valid the workbook is deployed in full. When any row is
invalid the job ends with no subject mappings and `mapping_state` becomes
`subjects_import_rejected` until the next import or the next manual
subject-mapping change. Row problems are listed by
`GET /shuttle_mapping_errors?job_id=…` with category `subject_import`,
messages of the form `Row N: …`, at most 500 entries plus one overflow
entry.
Validation and deployment are asynchronous after acceptance. Poll
`GET /shuttle_jobs/{shuttle_job_id}` while `mapping_state` is
`importing_subjects`. Only one import may be in flight per job. The job
must map subjects (`account_mapping` enabled) and its source scan must be
finished; otherwise the request returns `409`.

Expected workbook format (API clients cannot download the UI template):
sheets `Users` and/or `Groups` (a sheet named `Subjects` is also accepted).
Columns are `Source User <Key>`, `Target User <Key>`, `Skip` on `Users`,
and `Source Group <Key>`, `Target Group <Key>`, `Skip` on `Groups`, where
`<Key>` is the primary identifier for that role and system:

- Users: `Email` for most systems; `ID` for `SharePoint` (2007/2010/2013);
  `Name` for Windows (`windows_union`, stored as the user id).
- Groups: `Name` for most systems; `Email` for Google Drive admin groups.
  Source rows for a template can be taken from
  `GET /shuttle_discovered_subjects`.

This operation is performed by calling function `create_shuttle_subject_mapping_import_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-subject-mapping-imports/).

_Currently we don't have an example for calling `create_shuttle_subject_mapping_import_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job whose subject mappings are replaced.
- file_id `str`
  - The unique identifier of the Box file holding the mapping workbook. The file is read as the calling user, so it must live somewhere that user can download from.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

The import was accepted. Validation and deployment continue
asynchronously. Poll `GET /shuttle_jobs/{shuttle_job_id}` until
`mapping_state` is no longer `importing_subjects`. A rejected import
ends with `mapping_state` `subjects_import_rejected` and an empty
subject-mapping list; a successful import moves on to a later
mapping-preparation state such as `mapping_complete` or `ready`.

## List shuttle subject mappings

Returns a paginated list of subject mappings for the shuttle job identified
by `job_id`.

This operation is performed by calling function `get_shuttle_subject_mappings_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-subject-mappings/).

_Currently we don't have an example for calling `get_shuttle_subject_mappings_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job whose subject mappings to list.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleSubjectMappingsV2026R0`.

Returns a paginated list of shuttle subject mappings.

## Create shuttle subject mapping

Creates a subject mapping that connects a discovered source subject to a
Box user or group for the given shuttle job.

This operation is performed by calling function `create_shuttle_subject_mapping_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-subject-mappings/).

_Currently we don't have an example for calling `create_shuttle_subject_mapping_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job this mapping belongs to.
- discovered_subject_id `str`
  - The unique identifier of the discovered subject to map.
- revision `Optional[int]`
  - The discovery-requirements revision to resolve against. Omit to use the latest revision.
- is_subject_skipped `Optional[bool]`
  - Whether this subject should be skipped during the migration. Defaults to `false`.
- target `Optional[ShuttleTargetSubjectInputV2026R0]`
  - The Box target to map to. Omit or set to `null` when the subject is skipped.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleSubjectMappingV2026R0`.

Returns the newly created shuttle subject mapping.

## Get shuttle subject mapping by ID

Returns details for a single shuttle subject mapping identified by its ID,
including the source subject and Box target, if any.

This operation is performed by calling function `get_shuttle_subject_mapping_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-subject-mappings-id/).

_Currently we don't have an example for calling `get_shuttle_subject_mapping_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_subject_mapping_id `str`
  - The unique identifier for the shuttle subject mapping. Example: "6a3ba7b12ea17bc9461eeace"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleSubjectMappingV2026R0`.

Returns the shuttle subject mapping.

## Update shuttle subject mapping

Updates the mutable properties of an existing shuttle subject mapping
identified by its ID. Only the fields supplied in the request body are
changed.

This operation is performed by calling function `update_shuttle_subject_mapping_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/put-shuttle-subject-mappings-id/).

_Currently we don't have an example for calling `update_shuttle_subject_mapping_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_subject_mapping_id `str`
  - The unique identifier for the shuttle subject mapping. Example: "6a3ba7b12ea17bc9461eeace"
- is_subject_skipped `Optional[bool]`
  - Whether this subject should be skipped during the migration.
- target `Optional[ShuttleTargetSubjectInputV2026R0]`
  - The Box target to map to. Set to `null` only for a skipped subject. Setting it to `null` while the mapping is active fails validation. Updating `is_subject_skipped` alone preserves the existing target.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleSubjectMappingV2026R0`.

Returns the updated shuttle subject mapping.

## Delete shuttle subject mapping

Permanently deletes the shuttle subject mapping identified by its ID.

This operation is performed by calling function `delete_shuttle_subject_mapping_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/delete-shuttle-subject-mappings-id/).

_Currently we don't have an example for calling `delete_shuttle_subject_mapping_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_subject_mapping_id `str`
  - The unique identifier for the shuttle subject mapping. Example: "6a3ba7b12ea17bc9461eeace"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the shuttle subject mapping was
successfully deleted.

## List shuttle discovered subjects

Returns a paginated list of subjects discovered on the source system for
the shuttle job identified by `job_id`.

This operation is performed by calling function `get_shuttle_discovered_subjects_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-discovered-subjects/).

_Currently we don't have an example for calling `get_shuttle_discovered_subjects_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job whose discovered subjects to list.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleDiscoveredSubjectsV2026R0`.

Returns a paginated list of discovered subjects.

## List shuttle path entries

Returns a paginated list of source or target path entries for a shuttle
job. Call with only `job_id` and `side` to list the roots, then browse one
level at a time using `path`, `path_id`, or both. Each entry includes
`path`, `path_id`, `is_directory`, and a `scope` object (`account` or
`shared_space`) so a mapping can be created from that row without extra
browse state. Valid values depend on the selected system.

This operation is performed by calling function `get_shuttle_path_entries_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-path-entries/).

_Currently we don't have an example for calling `get_shuttle_path_entries_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job whose path entries to list.
- side `GetShuttlePathEntriesV2026R0Side`
  - The side of the migration to browse.
- path `Optional[str]`
  - The human-readable parent path whose children are returned. This can be used with or without `path_id`. Omit both, or pass `/` as `path`, to list root entries.
- path_id `Optional[str]`
  - The `path_id` value of the parent entry whose children are returned. This can be used with or without `path`. It distinguishes paths with identical names on systems that support stable identifiers.
- account_email `Optional[str]`
  - The email of the account whose path entries are returned. This is a system-native identifier and is not always an RFC 5322 address.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttlePathEntriesV2026R0`.

Returns a paginated list of shuttle path entries.

## List shuttle mapping errors

Returns a paginated list of mapping errors for a shuttle job. Only the latest
record for each error is returned. The revision field identifies the mapping
revision in which that error was generated.

This operation is performed by calling function `get_shuttle_mapping_errors_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-mapping-errors/).

_Currently we don't have an example for calling `get_shuttle_mapping_errors_v2026_r0` in integration tests_

### Arguments

- job_id `str`
  - The unique identifier of the shuttle job whose mapping errors to list.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleMappingErrorsV2026R0`.

Returns a paginated list of shuttle mapping errors.

## List shuttle reports

Returns a paginated list of reports generated for the shuttle run
identified by `run_id`.

This operation is performed by calling function `get_shuttle_reports_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-reports/).

_Currently we don't have an example for calling `get_shuttle_reports_v2026_r0` in integration tests_

### Arguments

- run_id `str`
  - The unique identifier of the shuttle run whose reports to list.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleReportsV2026R0`.

Returns a paginated list of shuttle reports.

## Create shuttle report

Requests asynchronous generation of a report for a shuttle run. The
report is returned immediately in `pending` or `processing` status.
Poll `GET /shuttle_reports/{shuttle_report_id}` while `status` is
`pending` or `processing`. Stop when `status` is `complete`, `failed`,
`canceled`, or `unknown`. Repeating this request with the same
parameters reuses the existing report instead of creating a duplicate.

This operation is performed by calling function `create_shuttle_report_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-shuttle-reports/).

_Currently we don't have an example for calling `create_shuttle_report_v2026_r0` in integration tests_

### Arguments

- run_id `str`
  - The unique identifier of the shuttle run to generate a report for.
- format `CreateShuttleReportV2026R0Format`
  - The output file format of the report.
- sections `List[str]`
  - The sections to include in the report. Must be a non-empty subset of the run's `available_report_sections`. This is an open list whose set of values is expected to grow; the currently documented values include `files_and_folders`, `event_log`, `transfer_overview`, `source_users`, `target_users`, `source_collaborators`, `target_collaborators`, `source_collaborations`, and `target_collaborations`.
- users_scope `Optional[CreateShuttleReportV2026R0UsersScope]`
  - Which users to include in user-related report sections. Defaults to `migrated` when omitted.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleReportV2026R0`.

The report was accepted for generation. Returns the shuttle report;
generation continues asynchronously. Repeating this request with the
same parameters reuses the existing report instead of creating a
duplicate.

## Get shuttle report by ID

Returns details for a single shuttle report identified by its ID,
including generation status and, once generation finishes, the Box
output reference.

This operation is performed by calling function `get_shuttle_report_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-shuttle-reports-id/).

_Currently we don't have an example for calling `get_shuttle_report_by_id_v2026_r0` in integration tests_

### Arguments

- shuttle_report_id `str`
  - The unique identifier for the shuttle report. Example: "6a3ba8d14f2c91e8370b4d12"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShuttleReportV2026R0`.

Returns the shuttle report.
