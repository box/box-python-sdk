# ShieldInformationBarrierReportsManager

- [List shield information barrier reports](#list-shield-information-barrier-reports)
- [Create shield information barrier report](#create-shield-information-barrier-report)
- [Get shield information barrier report by ID](#get-shield-information-barrier-report-by-id)

## List shield information barrier reports

Lists shield information barrier reports.

This operation is performed by calling function `get_shield_information_barrier_reports`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barrier-reports/).

<!-- sample get_shield_information_barrier_reports -->

```python
client.shield_information_barrier_reports.get_shield_information_barrier_reports(
    barrier_id
)
```

### Arguments

- shield_information_barrier_id `str`
  - The ID of the shield information barrier.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierReports`.

Returns a paginated list of shield information barrier report objects.

## Create shield information barrier report

Creates a shield information barrier report for a given barrier.

This operation is performed by calling function `create_shield_information_barrier_report`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-shield-information-barrier-reports/).

<!-- sample post_shield_information_barrier_reports -->

```python
client.shield_information_barrier_reports.create_shield_information_barrier_report(
    shield_information_barrier=ShieldInformationBarrierBase(
        id=barrier_id,
        type=ShieldInformationBarrierBaseTypeField.SHIELD_INFORMATION_BARRIER,
    )
)
```

### Arguments

- shield_information_barrier `Optional[ShieldInformationBarrierBase]`
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierReport`.

Returns the shield information barrier report information object.

## Get shield information barrier report by ID

Retrieves a shield information barrier report by its ID.

This operation is performed by calling function `get_shield_information_barrier_report_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barrier-reports-id/).

<!-- sample get_shield_information_barrier_reports_id -->

```python
client.shield_information_barrier_reports.get_shield_information_barrier_report_by_id(
    created_report.id
)
```

### Arguments

- shield_information_barrier_report_id `str`
  - The ID of the shield information barrier Report. Example: "3423"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierReport`.

Returns the shield information barrier report object.
