# ShieldInformationBarrierSegmentsManager

- [Get shield information barrier segment with specified ID](#get-shield-information-barrier-segment-with-specified-id)
- [Delete shield information barrier segment](#delete-shield-information-barrier-segment)
- [Update shield information barrier segment with specified ID](#update-shield-information-barrier-segment-with-specified-id)
- [List shield information barrier segments](#list-shield-information-barrier-segments)
- [Create shield information barrier segment](#create-shield-information-barrier-segment)

## Get shield information barrier segment with specified ID

Retrieves shield information barrier segment based on provided ID..

This operation is performed by calling function `get_shield_information_barrier_segment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barrier-segments-id/).

<!-- sample get_shield_information_barrier_segments_id -->

```python
client.shield_information_barrier_segments.get_shield_information_barrier_segment_by_id(segment_id)
```

### Arguments

- shield_information_barrier_segment_id `str`
  - The ID of the shield information barrier segment. Example: "3423"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierSegment`.

Returns the shield information barrier segment object.

## Delete shield information barrier segment

Deletes the shield information barrier segment
based on provided ID.

This operation is performed by calling function `delete_shield_information_barrier_segment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-shield-information-barrier-segments-id/).

<!-- sample delete_shield_information_barrier_segments_id -->

```python
client.shield_information_barrier_segments.delete_shield_information_barrier_segment_by_id(segment_id)
```

### Arguments

- shield_information_barrier_segment_id `str`
  - The ID of the shield information barrier segment. Example: "3423"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Empty body in response.

## Update shield information barrier segment with specified ID

Updates the shield information barrier segment based on provided ID..

This operation is performed by calling function `update_shield_information_barrier_segment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-shield-information-barrier-segments-id/).

<!-- sample put_shield_information_barrier_segments_id -->

```python
client.shield_information_barrier_segments.update_shield_information_barrier_segment_by_id(segment_id, description=updated_segment_description)
```

### Arguments

- shield_information_barrier_segment_id `str`
  - The ID of the shield information barrier segment. Example: "3423"
- name `Optional[str]`
  - The updated name for the shield information barrier segment.
- description `Optional[str]`
  - The updated description for the shield information barrier segment.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierSegment`.

Returns the updated shield information barrier segment object.

## List shield information barrier segments

Retrieves a list of shield information barrier segment objects
for the specified Information Barrier ID.

This operation is performed by calling function `get_shield_information_barrier_segments`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barrier-segments/).

<!-- sample get_shield_information_barrier_segments -->

```python
client.shield_information_barrier_segments.get_shield_information_barrier_segments(barrier_id)
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

This function returns a value of type `ShieldInformationBarrierSegments`.

Returns a paginated list of shield information barrier segment objects.

## Create shield information barrier segment

Creates a shield information barrier segment.

This operation is performed by calling function `create_shield_information_barrier_segment`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-shield-information-barrier-segments/).

<!-- sample post_shield_information_barrier_segments -->

```python
client.shield_information_barrier_segments.create_shield_information_barrier_segment(ShieldInformationBarrierBase(id=barrier_id, type=ShieldInformationBarrierBaseTypeField.SHIELD_INFORMATION_BARRIER), segment_name, description=segment_description)
```

### Arguments

- shield_information_barrier `ShieldInformationBarrierBase`
- name `str`
  - Name of the shield information barrier segment.
- description `Optional[str]`
  - Description of the shield information barrier segment.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierSegment`.

Returns a new shield information barrier segment object.
