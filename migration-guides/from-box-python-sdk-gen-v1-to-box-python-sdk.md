# Migration guide from v1 version of the `box-python-sdk-gen` to the `box-python-sdk`

Note: This guide applies only to migrations targeting Box Python SDK v4.X.Y or v10.X.Y.
It does not apply to other major versions (e.g., v5.X, v11.X).

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [Installation](#installation)
  - [How to migrate](#how-to-migrate)
- [Usage](#usage)
  - [Using the Box Python SDK v10](#using-the-box-python-sdk-v10)
  - [Using the Box Python SDK v4](#using-the-box-python-sdk-v4)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

From the `box-python-sdk-gen` you can migrate either to v4 or v10 of the Box Python SDK.
Your choice should depend on whether you want to continue using the manually maintained SDK (Box Python SDK v3) alongside the generated one or not.

The v4 version of the Box Python SDK consolidates both the legacy SDK package `boxsdk` and the generated one `box_sdk_gen`.

- If previously you were using both artifacts `boxsdk` v3 and `box-sdk-gen` v1, migrate to v4 version of the Box Python SDK which consolidates `boxsdk` and `box_sdk_gen` packages.
- If you were only using the generated artifact `box-sdk-gen`, migrate to v10 version of the Box Python SDK which contains only the generated `box_sdk_gen` package.

| Scenario                                     | Your current usage                                 | Recommended target | Packages included in target                   | Why this choice                                                          | Notes                                                                                |
| -------------------------------------------- | -------------------------------------------------- | ------------------ | --------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Using both manual and generated SDK together | `boxsdk` v3 + `box-sdk-gen` v1 in the same project | v4.X.Y             | `boxsdk` (manual) + `box_sdk_gen` (generated) | Keep existing v3 code while adopting new features from the generated SDK | Run both modules side-by-side; use type aliases to avoid name conflicts if necessary |
| Using only the generated SDK                 | `box-sdk-gen` v1 only                              | v10.X.Y            | `box_sdk_gen` (generated) only                | Clean upgrade path with no legacy module; simpler dependency surface     | Best when you don’t need the manual `boxsdk` package                                 |

## Installation

In order to start using v4 or v10 version of the Box Python SDK, you need to change the dependency in your project.
The artifact name has changed from `box-sdk-gen` to `boxsdk`.
You also need to set the version to `4` if you are migrating to v4 or `10` if you are migrating to v10.
You can find the latest version of each major version on [PyPI](https://pypi.org/project/boxsdk/).

### How to migrate

To start using v4 or v10 version of Box Python SDK in your project, replace the dependency in your `requirements.txt`
or installation command.

**Old (`box-python-sdk-gen-v1`)**

```console
pip install box-sdk-gen
```

**New (`box-python-sdk-v10`)**

```console
pip install boxsdk>=10
```

**New (`box-python-sdk-v4`)**

```console
pip install boxsdk~=4.0
```

## Usage

### Using the Box Python SDK v10

After migration from `box-sdk-gen` to the `boxsdk` v10, you can still use the `box_sdk_gen` package in the same way as before.
To access the client for interacting with the Box API, simply import `BoxClient` and any other necessary classes from the `box_sdk_gen` package.

```python
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth

auth: BoxDeveloperTokenAuth = BoxDeveloperTokenAuth(
    token="INSERT YOUR DEVELOPER TOKEN HERE"
)
client: BoxClient = BoxClient(auth=auth)
for item in client.folders.get_folder_items("0").entries:
    print(item.name)
```

### Using the Box Python SDK v4

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
    updated_folder: Folder = new_client.folders.update_folder_by_id(
        folder_id=folder.id, name="My Updated Subfolder"
    )
    print(
        f"Created folder with ID {folder.id} has been updated to {updated_folder.name}"
    )


if __name__ == "__main__":
    main()
```
