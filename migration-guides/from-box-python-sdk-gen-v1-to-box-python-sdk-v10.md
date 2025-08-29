# Migration guide from v1 version of the `box-python-sdk-gen` to the v10 version of the `box-pythom-sdk`

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installation](#installation)
  - [How to migrate](#how-to-migrate)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

In order to start using v10 version of the Box Python SDK, you need to change the dependency in your project.
The artifact name has changed from `box-sdk-gen` to `boxsdk`.
You also need to set the version to `10.0.0` or higher. You can find the latest version on [PyPI](https://pypi.org/project/boxsdk/).

### How to migrate

To start using v10 version of Box Python SDK in you Maven project replace the dependency in your `requirements.txt`
or installation command.

**Old (`box-python-sdk-gen-v1`)**

```console
pip install box-sdk-gen
```

**New (`box-python-sdk-v10`)**

```console
pip install boxsdk>=10
```
