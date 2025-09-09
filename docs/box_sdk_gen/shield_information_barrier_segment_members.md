# ShieldInformationBarrierSegmentMembersManager

- [Get shield information barrier segment member by ID](#get-shield-information-barrier-segment-member-by-id)
- [Delete shield information barrier segment member by ID](#delete-shield-information-barrier-segment-member-by-id)
- [List shield information barrier segment members](#list-shield-information-barrier-segment-members)
- [Create shield information barrier segment member](#create-shield-information-barrier-segment-member)

## Get shield information barrier segment member by ID

Retrieves a shield information barrier
segment member by its ID.

This operation is performed by calling function `get_shield_information_barrier_segment_member_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barrier-segment-members-id/).

<!-- sample get_shield_information_barrier_segment_members_id -->

```python
client.shield_information_barrier_segment_members.get_shield_information_barrier_segment_member_by_id(segment_member.id)
```

### Arguments

- shield_information_barrier_segment_member_id `str`
  - The ID of the shield information barrier segment Member. Example: "7815"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierSegmentMember`.

Returns the shield information barrier segment member object.

## Delete shield information barrier segment member by ID

Deletes a shield information barrier
segment member based on provided ID.

This operation is performed by calling function `delete_shield_information_barrier_segment_member_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-shield-information-barrier-segment-members-id/).

<!-- sample delete_shield_information_barrier_segment_members_id -->

```python
client.shield_information_barrier_segment_members.delete_shield_information_barrier_segment_member_by_id(segment_member.id)
```

### Arguments

- shield_information_barrier_segment_member_id `str`
  - The ID of the shield information barrier segment Member. Example: "7815"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response if the
segment member was deleted successfully.

## List shield information barrier segment members

Lists shield information barrier segment members
based on provided segment IDs.

This operation is performed by calling function `get_shield_information_barrier_segment_members`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shield-information-barrier-segment-members/).

<!-- sample get_shield_information_barrier_segment_members -->

```python
client.shield_information_barrier_segment_members.get_shield_information_barrier_segment_members(segment.id)
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

This function returns a value of type `ShieldInformationBarrierSegmentMembers`.

Returns a paginated list of
shield information barrier segment member objects.

## Create shield information barrier segment member

Creates a new shield information barrier segment member.

This operation is performed by calling function `create_shield_information_barrier_segment_member`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-shield-information-barrier-segment-members/).

<!-- sample post_shield_information_barrier_segment_members -->

```python
client.shield_information_barrier_segment_members.create_shield_information_barrier_segment_member(CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegment(id=segment.id, type=CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentTypeField.SHIELD_INFORMATION_BARRIER_SEGMENT), UserBase(id=get_env_var('USER_ID')))
```

### Arguments

- type `Optional[CreateShieldInformationBarrierSegmentMemberType]`
  - A type of the shield barrier segment member.
- shield_information_barrier `Optional[ShieldInformationBarrierBase]`
- shield_information_barrier_segment `CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegment`
  - The `type` and `id` of the requested shield information barrier segment.
- user `UserBase`
  - User to which restriction will be applied.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldInformationBarrierSegmentMember`.

Returns a new shield information barrier segment member object.
