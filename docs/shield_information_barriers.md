# ShieldInformationBarriersManager

- [Get shield information barrier with specified ID](#get-shield-information-barrier-with-specified-id)
- [Add changed status of shield information barrier with specified ID](#add-changed-status-of-shield-information-barrier-with-specified-id)
- [List shield information barriers](#list-shield-information-barriers)
- [Create shield information barrier](#create-shield-information-barrier)

## Get shield information barrier with specified ID

Get shield information barrier based on provided ID.

This operation is performed by calling function `get_shield_information_barrier_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barriers-id/).

<!-- sample get_shield_information_barriers_id -->

```python
client.shield_information_barriers.get_shield_information_barrier_by_id(barrier_id)
```

### Arguments

- shield_information_barrier_id `str`
  - The ID of the shield information barrier. Example: "1910967"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrier`.

Returns the shield information barrier object.

## Add changed status of shield information barrier with specified ID

Change status of shield information barrier with the specified ID.

This operation is performed by calling function `update_shield_information_barrier_status`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-shield-information-barriers-change-status/).

<!-- sample post_shield_information_barriers_change_status -->

```python
client.shield_information_barriers.update_shield_information_barrier_status(
    barrier_id, UpdateShieldInformationBarrierStatusStatus.DISABLED
)
```

### Arguments

- id `str`
  - The ID of the shield information barrier.
- status `UpdateShieldInformationBarrierStatusStatus`
  - The desired status for the shield information barrier.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrier`.

Returns the updated shield information barrier object.

## List shield information barriers

Retrieves a list of shield information barrier objects
for the enterprise of JWT.

This operation is performed by calling function `get_shield_information_barriers`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barriers/).

<!-- sample get_shield_information_barriers -->

```python
client.shield_information_barriers.get_shield_information_barriers()
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarriers`.

Returns a paginated list of
shield information barrier objects,
empty list if currently no barrier.

## Create shield information barrier

Creates a shield information barrier to
separate individuals/groups within the same
firm and prevents confidential information passing between them.

This operation is performed by calling function `create_shield_information_barrier`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-shield-information-barriers/).

<!-- sample post_shield_information_barriers -->

```python
client.shield_information_barriers.create_shield_information_barrier(
    EnterpriseBase(id=enterprise_id)
)
```

### Arguments

- enterprise `EnterpriseBase`
  - The `type` and `id` of enterprise this barrier is under.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrier`.

Returns a new shield information barrier object.
