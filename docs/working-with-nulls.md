# Handling null values in Box Python SDK

While using Box Python SDK it's important to understand how null values behave. This document provides a general overview of null value behaviour in Box Python SDK to help developers manage data consistently and predictably.

## Understanding null behaviour

The Box Python SDK follows a consistent pattern when handling null values in update operations. This behaviour applies to most endpoints that modify resources such as users, files, folders and metadata. The updating field behaves differently depending on weather you omit it, set it to null, or provide a value:

- Omitting the field: The field won't be included in request and the value will remain unchanged.
- Setting it to null: Setting a field to null, will cause sending HTTP request with field value set to null, what will result in removing its current value or disassociates it from the resource.
- Providing a value: Providing a non-null value assigns or updates the field to that value.

## Example Usage

The client.files.update_file_by_id() method demonstrates null handling when modifying the lock field while updating the file:

```python
import null from box_sdk_gen

def createUpdateFile(client):
    uploaded_file_id = '12345'

    # locking the file
    file_with_lock = client.files.update_file_by_id(
        uploaded_file_id,
        lock=UpdateFileByIdLock(access=UpdateFileByIdLockAccessField.LOCK),
        fields=['lock'],
    )

    # unlocking the file using lock value as null
    file_without_lock = client.files.update_file_by_id(
        uploaded_file_id, lock=null, fields=['lock']
    )
```

## Summary

To summarize, if you omit the field, the field remains unchanged. If you set it to null, it clears/removes the value. If you provide a value to that field, the field gets updated to that specified value.
