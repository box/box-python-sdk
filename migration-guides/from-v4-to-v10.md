# Migration guide from v4 to v10 version of `boxsdk`

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [Installation](#installation)
- [Supported Environments](#supported-environments)
- [Migration Scope and Module Compatibility](#migration-scope-and-module-compatibility)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

Version 10 of the Box Python SDK is a modern, fully auto-generated SDK built entirely from the `box_sdk_gen` package.  
In version 4, the SDK included two packages side by side: the manually maintained `boxsdk` and the generated `box_sdk_gen`.  
Starting with version 10, the `boxsdk` package has been removed, and only the `box_sdk_gen` package remains.

If you are migrating code from `boxsdk` to `box_sdk_gen` package, detailed instructions are available in the dedicated  
[Migration guide: migrate from `boxsdk` to `box_sdk_gen` package](./from-boxsdk-to-box_sdk_gen.md).

## Installation

To install v10 version of Box Python SDK use command:

```console
pip install boxsdk>=10
```

Starting with v10, the legacy `boxsdk` package is no longer included.
Installing v10 provides only the `box_sdk_gen` package.

## Supported Environments

Both v4 and v10 of the Box Python SDK share the same Python version requirement: Python 3.8 or higher.  
No changes to your environment are needed when upgrading from v4 to v10.

## Migration Scope and Module Compatibility

If your project only uses the `box_sdk_gen` package from v4, no code changes are required to migrate to v10.  
The generated `box_sdk_gen` package is the same in both v4 and v10.

If your project still includes code that uses the legacy `boxsdk` module, follow the dedicated guide to update it:  
[Migration guide: migrate from `boxsdk` to `box_sdk_gen` package](./from-boxsdk-to-box_sdk_gen.md).
