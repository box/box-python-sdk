# Migration guide from v3 to v4 of the Box Python SDK

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [Installation](#installation)
  - [How to migrate](#how-to-migrate)
- [Supported Environments](#supported-environments)
- [Highlighting the Key Differences](#highlighting-the-key-differences)
  - [Using boxsdk and box_sdk_gen together](#using-boxsdk-and-box_sdk_gen-together)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

The v4 release of the Box Python SDK is a transitional version designed to help developers migrate from
the manually maintained v3 SDK to the modern, auto-generated v10+ SDK.

This release combines two packages into a single artifact:

- `boxsdk` - the manually maintained package from v3.
- `box_sdk_gen` - the new, auto-generated module built from the official OpenAPI specification (and the sole component of the v10 SDK).

This hybrid approach allows you to gradually adopt the new `box_sdk_gen` features
while continuing to use your existing v3 integration, eliminating the need for an immediate full rewrite.

## Installation

To start using v4 of the Box Python SDK, update your project's `boxsdk` dependency to version 4.  
You can find the latest available version on [PyPI](https://pypi.org/project/boxsdk/).

### How to migrate

To upgrade from v3 to v4, bump the version of the `boxsdk` dependency in your `requirements.txt` file or your installation command.

```console
pip install boxsdk~=4.0
```

## Supported Environments

Because v4 of the Box Python SDK consolidates the manually maintained v3 `boxsdk` and the new auto-generated `box_sdk_gen` packages,
it now follows the newer package minimum platform requirements.

Supported Python versions: 3.8+
Note: Python 3.6 and 3.7 are no longer supported.

If your application currently targets an older Python version, update your deployment environment to meet these minimum requirements.

## Highlighting the Key Differences

The `boxsdk` package usage in v4 remains the same as in v3 and is not covered in this document.
If you are migrating code from `boxsdk` to `box_sdk_gen` package, which we recommend,
the key differences between the packages are documented in:

- [Migration guide: boxsdk → box_sdk_gen](./from-boxsdk-to-box_sdk_gen.md)

### Using boxsdk and box_sdk_gen together

After migration to Box Python SDK v4, you can use both the manual Box Python SDK package `boxsdk` and the generated one `box_sdk_gen`.
You just need to import the required classes from the appropriate package depending on which SDK you intend to use.
If both packages contain classes with the same name, you can use type aliases to resolve any naming conflicts.

```python
from boxsdk import JWTAuth, Client
from boxsdk.object.folder import Folder as FolderOld
from box_sdk_gen import BoxJWTAuth, JWTConfig, BoxClient, Folder


def main():
    auth = JWTAuth.from_settings_file("/path/to/settings.json")
    legacy_client = Client(auth)

    jwt_config = JWTConfig.from_config_file(config_file_path="/path/to/settings.json")
    auth = BoxJWTAuth(config=jwt_config)
    new_client = BoxClient(auth=auth)

    folder: FolderOld = legacy_client.folder(folder_id="0").create_subfolder(
        "My Subfolder"
    )
    updated_folder: Folder = new_client.folders.update_folder(
        folder_id=folder.id, name="My Updated Subfolder"
    )
    print(
        f"Created folder with ID {folder.id} has been updated to {updated_folder.name}"
    )


if __name__ == "__main__":
    main()
```
