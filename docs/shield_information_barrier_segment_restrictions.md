# ShieldInformationBarrierSegmentRestrictionsManager

- [Get shield information barrier segment restriction by ID](#get-shield-information-barrier-segment-restriction-by-id)
- [Delete shield information barrier segment restriction by ID](#delete-shield-information-barrier-segment-restriction-by-id)
- [List shield information barrier segment restrictions](#list-shield-information-barrier-segment-restrictions)
- [Create shield information barrier segment restriction](#create-shield-information-barrier-segment-restriction)

## Get shield information barrier segment restriction by ID

Retrieves a shield information barrier segment
restriction based on provided ID.

This operation is performed by calling function `get_shield_information_barrier_segment_restriction_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barrier-segment-restrictions-id/).

<!-- sample get_shield_information_barrier_segment_restrictions_id -->

```python
client.shield_information_barrier_segment_restrictions.get_shield_information_barrier_segment_restriction_by_id(
    segment_restriction_id
)
```

### Arguments

- shield_information_barrier_segment_restriction_id `str`
  - The ID of the shield information barrier segment Restriction. Example: "4563"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierSegmentRestriction`.

Returns the shield information barrier segment
restriction object.

## Delete shield information barrier segment restriction by ID

Delete shield information barrier segment restriction
based on provided ID.

This operation is performed by calling function `delete_shield_information_barrier_segment_restriction_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-shield-information-barrier-segment-restrictions-id/).

<!-- sample delete_shield_information_barrier_segment_restrictions_id -->

```python
client.shield_information_barrier_segment_restrictions.delete_shield_information_barrier_segment_restriction_by_id(
    segment_restriction_id
)
```

### Arguments

- shield_information_barrier_segment_restriction_id `str`
  - The ID of the shield information barrier segment Restriction. Example: "4563"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Empty body in response.

## List shield information barrier segment restrictions

Lists shield information barrier segment restrictions
based on provided segment ID.

This operation is performed by calling function `get_shield_information_barrier_segment_restrictions`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barrier-segment-restrictions/).

<!-- sample get_shield_information_barrier_segment_restrictions -->

```python
client.shield_information_barrier_segment_restrictions.get_shield_information_barrier_segment_restrictions(
    segment_id
)
```

### Arguments

- shield_information_barrier_segment_id `str`
  - The ID of the shield information barrier segment.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierSegmentRestrictions`.

Returns a paginated list of
shield information barrier segment restriction objects.

## Create shield information barrier segment restriction

Creates a shield information barrier
segment restriction object.

This operation is performed by calling function `create_shield_information_barrier_segment_restriction`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-shield-information-barrier-segment-restrictions/).

<!-- sample post_shield_information_barrier_segment_restrictions -->

```python
client.shield_information_barrier_segment_restrictions.create_shield_information_barrier_segment_restriction(
    CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegment(
        id=segment_id,
        type=CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentTypeField.SHIELD_INFORMATION_BARRIER_SEGMENT,
    ),
    CreateShieldInformationBarrierSegmentRestrictionRestrictedSegment(
        id=segment_to_restrict_id,
        type=CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentTypeField.SHIELD_INFORMATION_BARRIER_SEGMENT,
    ),
    type=CreateShieldInformationBarrierSegmentRestrictionType.SHIELD_INFORMATION_BARRIER_SEGMENT_RESTRICTION,
)
```

### Arguments

- type `CreateShieldInformationBarrierSegmentRestrictionType`
  - The type of the shield barrier segment restriction for this member.
- shield_information_barrier `Optional[ShieldInformationBarrierBase]`
- shield_information_barrier_segment `CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegment`
  - The `type` and `id` of the requested shield information barrier segment.
- restricted_segment `CreateShieldInformationBarrierSegmentRestrictionRestrictedSegment`
  - The `type` and `id` of the restricted shield information barrier segment.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierSegmentRestriction`.

Returns the newly created Shield
Information Barrier Segment Restriction object.
