<p align="center">
  <img src="https://github.com/box/sdks/blob/master/images/box-dev-logo.png" alt= “box-dev-logo” width="30%" height="50%">
</p>

# Box Python SDK v10

[![Project Status](http://opensource.box.com/badges/active.svg)](http://opensource.box.com/badges)
![build](https://github.com/box/box-python-sdk/actions/workflows/build.yml/badge.svg?branch=sdk-gen)
[![PyPI version](https://badge.fury.io/py/boxsdk.svg)](https://badge.fury.io/py/boxsdk)
[![image](https://img.shields.io/pypi/dm/boxsdk.svg)](https://pypi.python.org/pypi/boxsdk)
![Platform](https://img.shields.io/badge/python-3.8+-blue)
[![Coverage](https://coveralls.io/repos/github/box/box-python-sdk/badge.svg?branch=sdk-gen)](https://coveralls.io/github/box/box-python-sdk?branch=sdk-gen)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [Supported versions](#supported-versions)
  - [Version v4](#version-v4)
  - [Version v10](#version-v10)
  - [Which Version Should I Use?](#which-version-should-i-use)
- [Installing](#installing)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Documentation](#documentation)
- [Migration guides](#migration-guides)
- [Versioning](#versioning)
  - [Version schedule](#version-schedule)
- [Contributing](#contributing)
- [FIPS 140-2 Compliance](#fips-140-2-compliance)
- [Questions, Bugs, and Feature Requests?](#questions-bugs-and-feature-requests)
- [Copyright and License](#copyright-and-license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Introduction

We are excited to introduce the v10 major release of the Box Python SDK,
designed to elevate the developer experience and streamline your integration with the Box Content Cloud.

With this SDK version, we provide the `box_sdk_gen` package, which gives you access to:

1. Full API Support: The new generation of Box SDKs empowers developers with complete coverage of the Box API ecosystem. You can now access all the latest features and functionalities offered by Box, allowing you to build even more sophisticated and feature-rich applications.
2. Rapid API Updates: Say goodbye to waiting for new Box APIs to be incorporated into the SDK. With our new auto-generation development approach, we can now add new Box APIs to the SDK at a much faster pace (in a matter of days). This means you can leverage the most up-to-date features in your applications without delay.
3. Embedded Documentation: We understand that easy access to information is crucial for developers. With our new approach, we have included comprehensive documentation for all objects and parameters directly in the source code of the SDK. This means you no longer need to look up this information on the developer portal, saving you time and streamlining your development process.
4. Enhanced Convenience Methods: Our commitment to enhancing your development experience continues with the introduction of convenience methods. These methods cover various aspects such as chunk uploads, classification, and much more.
5. Seamless Start: The new SDKs integrate essential functionalities like authentication, automatic retries with exponential backoff, exception handling, request cancellation, and type checking, enabling you to focus solely on your application's business logic.

Embrace the new generation of Box SDKs and unlock the full potential of the Box Content Cloud.

# Supported versions

To enhance developer experience, we have introduced the new generated codebase through the `box_sdk_gen` package.
The `box_sdk_gen` package is available in two major supported versions: v4 and v10.

## Version v4

In v4 of the Box Python SDK, we are introducing a version that consolidates both the manually written package (`boxsdk`)
and the new generated package (`box_sdk_gen`). This allows developers to use both packages simultaneously within a single project.

The codebase for v4 of the Box Python SDK is currently available on the [combined-sdk](https://github.com/box/box-python-sdk/tree/combined-sdk) branch.
Migration guide which would help with migration from `boxsdk` to `box_sdk_gen` can be found [here](./migration-guides/from-boxsdk-to-box_sdk_gen.md).

Version v4 is intended for:

- Existing developers of the Box Python SDK v3 who want to access new API features while keeping their current codebase largely unchanged.
- Existing developers who are in the process of migrating to `box_sdk_gen`, but do not want to move all their code to the new package immediately.

## Version v10

Starting with v10, the SDK is built entirely on the generated `box_sdk_gen` package, which fully and exclusively replaces the old `boxsdk` package.
The codebase for v10 of the Box Python SDK is currently available on the [sdk-gen](https://github.com/box/box-python-sdk/tree/sdk-gen) branch.

Version v10 is intended for:

- New users of the Box Python SDK.
- Developers already working with the generated Box Python SDK previously available under the [Box Python SDK Gen repository](https://github.com/box/box-python-sdk-gen).

## Which Version Should I Use?

| Scenario                                                                                                                     | Recommended Version                                                      | Example `pip install`       |
| ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------- |
| Creating a new application                                                                                                   | Use [v10](https://github.com/box/box-python-sdk/tree/sdk-gen)            | `pip install "boxsdk>=10"`  |
| App using [box-sdk-gen](https://pypi.org/project/box-sdk-gen/) artifact                                                      | Migrate to [v10](https://github.com/box/box-python-sdk/tree/sdk-gen)     | `pip install "boxsdk>=10"`  |
| App using both [box-sdk-gen](https://pypi.org/project/box-sdk-gen/) and [boxsdk](https://pypi.org/project/boxsdk/) artifacts | Upgrade to [v4](https://github.com/box/box-python-sdk/tree/combined-sdk) | `pip install "boxsdk~=4.0"` |
| App using v3 of [boxsdk](https://pypi.org/project/boxsdk/) artifact                                                          | Upgrade to [v4](https://github.com/box/box-python-sdk/tree/combined-sdk) | `pip install "boxsdk~=4.0"` |

For full guidance on SDK versioning, see the [Box SDK Versioning Guide](https://developer.box.com/guides/tooling/sdks/sdk-versioning/).

# Installing

The next generation of the SDK starts with version `10.0.0`.

```console
pip install boxsdk>=10
```

This is autogenerated Box SDK version. Supported Python versions are Python 3.8 and above.

To install also extra dependencies required for JWT authentication, use command:

```console
pip install "boxsdk[jwt]>=10"
```

# Getting Started

To get started with the SDK, get a Developer Token from the Configuration page of your app in the [Box Developer
Console](https://app.box.com/developers/console). You can use this token to make test calls for your own Box account.

The SDK provides an `BoxDeveloperTokenAuth` class, which allows you to authenticate using your Developer Token.
Use instance of `BoxDeveloperTokenAuth` to initialize `BoxClient` object.
Using `BoxClient` object you can access managers, which allow you to perform some operations on your Box account.

The example below demonstrates how to authenticate with Developer Token and print names of all items inside a root folder.

```python
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth

def main(token: str):
    auth: BoxDeveloperTokenAuth = BoxDeveloperTokenAuth(token=token)
    client: BoxClient = BoxClient(auth=auth)
    for item in client.folders.get_folder_items('0').entries:
        print(item.name)

if __name__ == '__main__':
    main('INSERT YOUR DEVELOPER TOKEN HERE')
```

# Authentication

Box Python SDK v10 supports multiple authentication methods including Developer Token, OAuth 2.0,
Client Credentials Grant, and JSON Web Token (JWT).

You can find detailed instructions and example code for each authentication method in
[Authentication](./docs/authentication.md) document.

# Documentation

Browse the [docs](docs/README.md) or see [API Reference](https://developer.box.com/reference/) for more information.

# Migration guides

Migration guides which help you to migrate to supported major SDK versions can be found [here](./migration-guides).

# Versioning

We use a modified version of [Semantic Versioning](https://semver.org/) for all changes. See [version strategy](VERSIONS.md) for details which is effective from 30 July 2022.

A current release is on the leading edge of our SDK development, and is intended for customers who are in active development and want the latest and greatest features.  
Instead of stating a release date for a new feature, we set a fixed minor or patch release cadence of maximum 2-3 months (while we may release more often).
At the same time, there is no schedule for major or breaking release. Instead, we will communicate one quarter in advance the upcoming breaking change to allow customers to plan for the upgrade.

We always recommend that all users run the latest available minor release for whatever major version is in use.
We highly recommend upgrading to the latest SDK major release at the earliest convenient time and before the EOL date.

## Version schedule

| Version | Supported Environments | State     | First Release | EOL/Terminated         |
| ------- | ---------------------- | --------- | ------------- | ---------------------- |
| 10      | Python 3.8+            | Supported | 17 Sep 2025   | TBD                    |
| 4       | Python 3.8+            | Supported | 23 Oct 2025   | 2027 or v5 is released |
| 3       | Python 3.6+            | EOL       | 17 Jan 2022   | 23 Oct 2025            |
| 2       |                        | EOL       | 01 Nov 2018   | 17 Jan 2022            |
| 1       |                        | EOL       | 10 Feb 2015   | 01 Nov 2018            |

# Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

# FIPS 140-2 Compliance

The Python SDK allows the use of FIPS 140-2 validated SSL libraries, such as OpenSSL 3.0.
However, some actions are required to enable this functionality.

Currently, the latest distributions of Python default to OpenSSL v1.1.1, which is not FIPS compliant.
Therefore, if you want to use OpenSSL 3.0 in your network communication,
you need to ensure that Python uses a custom SSL library.
One way to achieve this is by creating a custom Python distribution with the ssl module replaced.

If you are using JWT for authentication, it is also necessary to ensure that the cryptography library,
which is one of the extra dependencies for JWT, uses OpenSSL 3.0.
To enable FIPS mode for the `cryptography` library, you need to install a FIPS-compliant version of OpenSSL
during the installation process of cryptography using the `pip` command.

# Questions, Bugs, and Feature Requests?

Need to contact us directly? [Browse the issues tickets](https://github.com/box/box-python-sdk/issues)! Or, if that
doesn't work, [file a new one](https://github.com/box/box-python-sdk/issues/new) and we will get
back to you. If you have general questions about the Box API, you can post to the [Box Developer Forum](https://community.box.com/box-platform-5).

# Copyright and License

Copyright 2025 Box, Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
