# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [9.0.0](https://github.com/box/box-python-sdk/compare/v3.14.0...v9.0.0) (2025-08-20)


### ⚠ BREAKING CHANGES

* Change names of unions (box/box-codegen#789) (#939)
* remove unused models from schemas (box/box-openapi#547) (#932)

### Bug Fixes

* Rename external user deletion method (box/box-codegen[#796](https://github.com/box/box-python-sdk/issues/796)) ([#953](https://github.com/box/box-python-sdk/issues/953)) ([381aec2](https://github.com/box/box-python-sdk/commit/381aec2aa835f043bc083d11a8b00a8f8dd75bf9))


### New Features and Enhancements

* Add External User Deletion API (box/box-openapi[#550](https://github.com/box/box-python-sdk/issues/550)) ([#941](https://github.com/box/box-python-sdk/issues/941)) ([a80ad85](https://github.com/box/box-python-sdk/commit/a80ad856b3193e54272e04f01ddb025b2d9f781f))
* Change names of unions (box/box-codegen[#789](https://github.com/box/box-python-sdk/issues/789)) ([#939](https://github.com/box/box-python-sdk/issues/939)) ([cf2b1d5](https://github.com/box/box-python-sdk/commit/cf2b1d5b12be0ff2453867b7d3502437283bf695))
* remove unused models from schemas (box/box-openapi[#547](https://github.com/box/box-python-sdk/issues/547)) ([#932](https://github.com/box/box-python-sdk/issues/932)) ([6ef6d63](https://github.com/box/box-python-sdk/commit/6ef6d63c37e6eccc3489a9076e0a0b0940a6e0d6)), closes [box/box-openapi#542](https://github.com/box/box-openapi/issues/542) [box/box-openapi#544](https://github.com/box/box-openapi/issues/544) [box/box-codegen#781](https://github.com/box/box-codegen/issues/781) [box/box-openapi#545](https://github.com/box/box-openapi/issues/545)
* Support event with long polling (box/box-codegen[#757](https://github.com/box/box-python-sdk/issues/757)) ([#936](https://github.com/box/box-python-sdk/issues/936)) ([4442a84](https://github.com/box/box-python-sdk/commit/4442a848576c9499bced5294cd8b7b6da7d9bf12))
* Support Python 3.12 and Python 3.13 ([#898](https://github.com/box/box-python-sdk/issues/898)) ([d604ea9](https://github.com/box/box-python-sdk/commit/d604ea98012aed3c2d0212d1b40b71a52efb55ec))

## [3.14.0](https://github.com/box/box-python-sdk/compare/v3.13.0...v3.14.0) (2025-04-09)


### New Features and Enhancements:

* Add `stream_file_content` parameter to upload methods ([#890](https://github.com/box/box-python-sdk/issues/890)) ([0e63c00](https://github.com/box/box-python-sdk/commit/0e63c002ee17618c08200c12caae4bb3890b1e90))

## [3.13.0](https://github.com/box/box-python-sdk/compare/v3.12.0...v3.13.0) (2024-08-22)


### New Features and Enhancements:

* Add support for get AI agent default ([#883](https://github.com/box/box-python-sdk/issues/883)) ([c1010e0](https://github.com/box/box-python-sdk/commit/c1010e0349847586a9f00046570e975ec48eb0c5))

## [3.12.0](https://github.com/box/box-python-sdk/compare/v3.11.0...v3.12.0) (2024-08-06)


### New Features and Enhancements:

* add create sign request function with different required parameters ([#878](https://github.com/box/box-python-sdk/issues/878)) ([d972f54](https://github.com/box/box-python-sdk/commit/d972f54dcf9962c6b911422793a682d8f6289f9e))
* Support Box AI features ([#877](https://github.com/box/box-python-sdk/issues/877)) ([3026d2a](https://github.com/box/box-python-sdk/commit/3026d2ab9932cd07aa9ff15a3ac3c3c14d3089b0))

## [3.11.0](https://github.com/box/box-python-sdk/compare/v3.10.0...v3.11.0) (2024-06-07)


### New Features and Enhancements:

* Use upload session `urls` for chunk upload ([#875](https://github.com/box/box-python-sdk/issues/875)) ([c67b03c](https://github.com/box/box-python-sdk/commit/c67b03c7d88533773d62d72f0b626031805d61eb))

## [3.10.0](https://github.com/box/box-python-sdk/compare/v3.9.2...v3.10.0) (2024-05-22)


### New Features and Enhancements:

* Transition to stable status ([#872](https://github.com/box/box-python-sdk/issues/872)) ([6203606](https://github.com/box/box-python-sdk/commit/620360607a51ee302cde61401db1424c9bf48d81))

### Bug Fixes:

* Change exception type for missing location header ([#871](https://github.com/box/box-python-sdk/issues/871)) ([8c5e0ec](https://github.com/box/box-python-sdk/commit/8c5e0eca7e494baa8138dceededa2009abc1717b))
* fix annnotation of oauths access_token ([#855](https://github.com/box/box-python-sdk/issues/855)) ([804780e](https://github.com/box/box-python-sdk/commit/804780e4c8d410590fa20cdb6dd35224d59d2ec0))
* Fix retention policy integration test ([#867](https://github.com/box/box-python-sdk/issues/867)) ([8e0d640](https://github.com/box/box-python-sdk/commit/8e0d6406f26be87799838b0aa57acd62c79d59a2))
* Remove delete classification ([#861](https://github.com/box/box-python-sdk/issues/861)) ([393cfef](https://github.com/box/box-python-sdk/commit/393cfefa57e729f34221a4e5923a4a50532f4013))
* Update exception file get download URL ([#866](https://github.com/box/box-python-sdk/issues/866)) ([94dcbcd](https://github.com/box/box-python-sdk/commit/94dcbcd490d98ff19afd38c9880de8022ad2ec89))

### [3.9.2](https://github.com/box/box-python-sdk/compare/v3.9.1...v3.9.2) (2023-10-18)


### Bug Fixes:

* Remove restriction to version <2 of `urllib3` library ([#851](https://github.com/box/box-python-sdk/issues/851)) ([1dcd82e](https://github.com/box/box-python-sdk/commit/1dcd82e93267bfc68e3a7f8068b3c45ab7e86daf))

### [3.9.1](https://github.com/box/box-python-sdk/compare/v3.9.0...v3.9.1) (2023-09-14)


### Bug Fixes:

* do not retry creating a ZIP when response code is 202 ([#845](https://github.com/box/box-python-sdk/issues/845)) ([3f6ed4e](https://github.com/box/box-python-sdk/commit/3f6ed4e1053a494ed9f2b79828850e059d0a1617)), closes [#844](https://github.com/box/box-python-sdk/issues/844)

## [3.9.0](https://github.com/box/box-python-sdk/compare/v3.8.1...v3.9.0) (2023-09-06)


### New Features and Enhancements:

* adds get sign template and get sign templates methods on Client ([#835](https://github.com/box/box-python-sdk/issues/835)) ([fbc783d](https://github.com/box/box-python-sdk/commit/fbc783d5af2e75f883f1a0051613c513139f68fb))
* Support create sign request with template ID ([#834](https://github.com/box/box-python-sdk/issues/834)) ([4f11d75](https://github.com/box/box-python-sdk/commit/4f11d7596488194fc740936fe987f42864003d41))

### Bug Fixes:

* ChunkedUploader Resume Not Closing ThreadPoolExecutor Instances ([#840](https://github.com/box/box-python-sdk/issues/840)) ([f210f00](https://github.com/box/box-python-sdk/commit/f210f00ad823d7755309f2e8804641e0debf8197))

### [3.8.1](https://github.com/box/box-python-sdk/compare/v3.8.0...v3.8.1) (2023-08-01)


### Bug Fixes:

* Fix JSON response validation retry strategy ([#831](https://github.com/box/box-python-sdk/issues/831)) ([69834eb](https://github.com/box/box-python-sdk/commit/69834eb4c91a5aa4bc294a9fa49ecf753979d029))

## [3.8.0](https://github.com/box/box-python-sdk/compare/v3.7.3...v3.8.0) (2023-07-25)


### New Features and Enhancements:

* Support updating all fields of `collaboration` ([#829](https://github.com/box/box-python-sdk/issues/829)) ([6dc7ecc](https://github.com/box/box-python-sdk/commit/6dc7ecc6f9c94e7531c4147a3645927b85928b2c))

### [3.7.3](https://github.com/box/box-python-sdk/compare/v3.7.2...v3.7.3) (2023-07-07)


### Bug Fixes:

* Stop processing data for logging when logging is disabled and cache response `json` ([#824](https://github.com/box/box-python-sdk/issues/824)) ([3079171](https://github.com/box/box-python-sdk/commit/3079171f8dfc1a4c85f8587e8ce90e8fbd826ee4))

### [3.7.2](https://github.com/box/box-python-sdk/compare/v3.7.1...v3.7.2) (2023-05-26)


### Bug Fixes:

* Use the older version of `urllib3` ([#815](https://github.com/box/box-python-sdk/issues/815)) ([ee29aa3](https://github.com/box/box-python-sdk/commit/ee29aa3fcf9ac71e9866913a87414cf625c0b805))

### [3.7.1](https://github.com/box/box-python-sdk/compare/v3.7.0...v3.7.1) (2023-04-18)


### Bug Fixes:

* Rename filter date parameters in legal hold creation according to the documentation ([#810](https://github.com/box/box-python-sdk/issues/810)) ([f52c66a](https://github.com/box/box-python-sdk/commit/f52c66a8a8399a776493537f692460ace2995e40))

## [3.7.0](https://github.com/box/box-python-sdk/compare/v3.6.2...v3.7.0) (2023-03-08)


### New Features and Enhancements:

* Update `retention_policies` and `retention_policy_assignments` ([#803](https://github.com/box/box-python-sdk/issues/803)) ([8b72f7e](https://github.com/box/box-python-sdk/commit/8b72f7e992bce676723a40ac12bde06c8cca3bfb))
* Use multiple threading for chunked upload ([#800](https://github.com/box/box-python-sdk/issues/800)) ([506ce0d](https://github.com/box/box-python-sdk/commit/506ce0d1e72ab4eeb6c5933a32c753e232a2f624))

### [3.6.2](https://github.com/box/box-python-sdk/compare/v3.6.1...v3.6.2) (2023-02-07)


### Bug Fixes:

* Retry `Connection broken` and `Connection reset` requests errors ([#794](https://github.com/box/box-python-sdk/issues/794)) ([f1a0aa4](https://github.com/box/box-python-sdk/commit/f1a0aa434369f06e80654a9f5c4b796100881aa6))

### [3.6.1](https://github.com/box/box-python-sdk/compare/v3.6.0...v3.6.1) (2023-01-09)


### Bug Fixes:

* Retry CCG and JWT auth requests on connection reset error ([#790](https://github.com/box/box-python-sdk/issues/790)) ([205997d](https://github.com/box/box-python-sdk/commit/205997db9870395b9dd042854c4201338dcf925f)), closes [#789](https://github.com/box/box-python-sdk/issues/789)

## [3.6.0](https://github.com/box/box-python-sdk/compare/v3.5.1...v3.6.0) (2023-01-03)


### New Features and Enhancements:

* Add support marker in trash get items ([#781](https://github.com/box/box-python-sdk/issues/781)) ([e2d1846](https://github.com/box/box-python-sdk/commit/e2d1846818aeccfcba2a2f09a5cd924c9f6cd534))
* Sanitize proxy credentials ([#782](https://github.com/box/box-python-sdk/issues/782)) ([97fb5aa](https://github.com/box/box-python-sdk/commit/97fb5aa2ed72008570abb327269ecec150632af9))

### Bug Fixes:

* Fix index error when getting an empty list of user term of service statuses ([#780](https://github.com/box/box-python-sdk/issues/780)) ([23d763a](https://github.com/box/box-python-sdk/commit/23d763ac4ba592131c43eb0319929db25d041c30))
* Specify which exceptions should be retried ([#784](https://github.com/box/box-python-sdk/issues/784)) ([833cd46](https://github.com/box/box-python-sdk/commit/833cd46bafe774f19925f78600df90477bf07055))

### [3.5.1](https://github.com/box/box-python-sdk/compare/v3.5.0...v3.5.1) (2022-11-30)


### Bug Fixes:

* Renew connection when Connection reset error occurs ([#771](https://github.com/box/box-python-sdk/issues/771)) ([bcaab27](https://github.com/box/box-python-sdk/commit/bcaab277c3cabba498076d066366abbaa5507904)), closes [#756](https://github.com/box/box-python-sdk/issues/756) [#757](https://github.com/box/box-python-sdk/issues/757) [#763](https://github.com/box/box-python-sdk/issues/763) [#765](https://github.com/box/box-python-sdk/issues/765) [#766](https://github.com/box/box-python-sdk/issues/766) [#770](https://github.com/box/box-python-sdk/issues/770)
* Retry JWT auth when got error: required unique `jti` claim. ([#768](https://github.com/box/box-python-sdk/issues/768)) ([878e958](https://github.com/box/box-python-sdk/commit/878e958abfb01740656aaff42492777753e4c8ea))
* Update `pyjtw` dependency to work with Python 3.10 ([#772](https://github.com/box/box-python-sdk/issues/772)) ([b13c5cd](https://github.com/box/box-python-sdk/commit/b13c5cd34105d3f774d3f6d35db7aaf51dd3e247))

## [3.5.0](https://github.com/box/box-python-sdk/compare/v3.4.0...v3.5.0) (2022-09-23)


### New Features and Enhancements:

* Add `redirect_url` and `declined_redirect_url` fields to Sign Request ([#752](https://github.com/box/box-python-sdk/issues/752)) ([5d1f609](https://github.com/box/box-python-sdk/commit/5d1f609ed4c2ddb24bd88ffac256a2809a012698))
* Add support for modifiable retention policies & enable deleting retention policy assignment ([#759](https://github.com/box/box-python-sdk/issues/759)) ([847301b](https://github.com/box/box-python-sdk/commit/847301b43be335365858a80420459dffaada4302))
* Support file request APIs ([#747](https://github.com/box/box-python-sdk/issues/747)) ([71895e3](https://github.com/box/box-python-sdk/commit/71895e33ff7cf339fd8e095a5393f04b86791d5a))

### Bug Fixes:

* Do not log the content of downloaded file ([#760](https://github.com/box/box-python-sdk/issues/760)) ([5d26431](https://github.com/box/box-python-sdk/commit/5d264314f949c1f4d9136efd5cf8f13dd5897c05))
* Fix closing file after chunked upload ([#761](https://github.com/box/box-python-sdk/issues/761)) ([b433692](https://github.com/box/box-python-sdk/commit/b433692ecc07d62d011785a557128c1780ea1647))

## [3.4.0](https://github.com/box/box-python-sdk/compare/v3.3.0...v3.4.0) (2022-07-06)


### New Features and Enhancements:

* Add support for editable shared links for files ([#737](https://github.com/box/box-python-sdk/issues/737)) ([1396200](https://github.com/box/box-python-sdk/commit/1396200c24bf62de63f9cb7949af5997593b9fac))
* Support uploading and deleting user avatar ([#743](https://github.com/box/box-python-sdk/issues/743)) ([fe00a9e](https://github.com/box/box-python-sdk/commit/fe00a9eb3434ee14bc4f01332d54c0272ed5f2d3))

## [3.3.0](https://github.com/box/box-python-sdk/compare/v3.2.0...v3.3.0) (2022-04-28)


### New Features and Enhancements:

* Add support for multiple date time formats ([#722](https://github.com/box/box-python-sdk/issues/722)) ([92364de](https://github.com/box/box-python-sdk/commit/92364de1e7c1eee1e85857546af65c307ca863a0))

### Bug Fixes:

* Add missing fields to metadata template field ([#719](https://github.com/box/box-python-sdk/issues/719)) ([9e574a3](https://github.com/box/box-python-sdk/commit/9e574a3e56f72c0e78a31ddda78bc11d36ff3516)), closes [#717](https://github.com/box/box-python-sdk/issues/717)
* Upload session commit return None on 202 ([#718](https://github.com/box/box-python-sdk/issues/718)) ([86a1856](https://github.com/box/box-python-sdk/commit/86a185630e6cce8f742123c7340da08267621313)), closes [#715](https://github.com/box/box-python-sdk/issues/715)

## [3.2.0](https://github.com/box/box-python-sdk/compare/v3.1.0...v3.2.0) (2022-03-11)


### New Features and Enhancements:

* Add setting `disposition_at` field for files under retention ([#710](https://github.com/box/box-python-sdk/issues/710)) ([91b1373](https://github.com/box/box-python-sdk/commit/91b13730a0beef2cf2a8a8c71087b11557fa5982))
* Add support for Client Credentials Grant authentication method ([#705](https://github.com/box/box-python-sdk/issues/705)) ([d33d16d](https://github.com/box/box-python-sdk/commit/d33d16db656cb5578f057a7e24f5396d635b5361))

### Bug Fixes:

* Add missing `box_sign` object to `__all__` list ([#708](https://github.com/box/box-python-sdk/issues/708)) ([5d80481](https://github.com/box/box-python-sdk/commit/5d8048116640fa672d6a1d700a6c1111faf87bb9))
* Fix `jwt` import errors ([#711](https://github.com/box/box-python-sdk/issues/711)) ([ee7bb6f](https://github.com/box/box-python-sdk/commit/ee7bb6f1dc5aa65dbf6ffeb18ee130f765f7b49b))

## [3.1.0](https://github.com/box/box-python-sdk/compare/v3.0.1...v3.1.0) (2022-02-16)


### New Features and Enhancements:

* Add support for Python 3.10 ([#692](https://github.com/box/box-python-sdk/issues/692)) ([d4aed82](https://github.com/box/box-python-sdk/commit/d4aed82831af97305bace9a4588d27b23856c306))
* Add support for Python 3.8, Python 3.9, `pypy-3.7` and `pypy-3.8`. ([#689](https://github.com/box/box-python-sdk/issues/689)) ([0aa94cc](https://github.com/box/box-python-sdk/commit/0aa94cc8a5c4db0fc204b27a60690b73c98a89cb))
* Deprecate `use_index` parameter from `MDQ` of files/folders ([#666](https://github.com/box/box-python-sdk/issues/666)) ([2595720](https://github.com/box/box-python-sdk/commit/25957204b82c878e15dc3d118505a741171e9772))
* Replace external package `mock` with Python standard library `unittest.mock` ([#697](https://github.com/box/box-python-sdk/issues/697)) ([6fd6366](https://github.com/box/box-python-sdk/commit/6fd63667aa7da4c794b4fb880d5c2949efe0073f))
* Upgrade cryptography library to the most recent version. ([#668](https://github.com/box/box-python-sdk/issues/668)) ([9c94d08](https://github.com/box/box-python-sdk/commit/9c94d0878515dc75c1f267e2fb1f189a852772b6)), closes [#667](https://github.com/box/box-python-sdk/issues/667)

### Bug Fixes:

* `UploadSession.commit` returns `None` when retry limit was reached ([#696](https://github.com/box/box-python-sdk/issues/696)) ([9456fe0](https://github.com/box/box-python-sdk/commit/9456fe0124f4ac4e9c8a7bcc49039f07f310c477))
* Add missing `api_call` decorator for `create_upload_session` ([#686](https://github.com/box/box-python-sdk/issues/686)) ([3510d3a](https://github.com/box/box-python-sdk/commit/3510d3ac085767205854014ecef80fd078d71773))
* Fix chunked upload ([#673](https://github.com/box/box-python-sdk/issues/673)) ([2605fd7](https://github.com/box/box-python-sdk/commit/2605fd782396ad6e42bd11c10f846e771634b7a0)), closes [#671](https://github.com/box/box-python-sdk/issues/671)

## [3.0.1] (2022-01-26)

### Bug Fixes:

-   Move sphinx to test requirements
    ([#662](https://github.com/box/box-python-sdk/pull/662))

## [3.0.0] (2022-01-17)

### ⚠ Breaking Changes:

-   Drop support for python 2.7
    ([#645](https://github.com/box/box-python-sdk/pull/645))
-   Add missing parameter `stream_position` to `get_admin_events` method
    ([#648](https://github.com/box/box-python-sdk/pull/648))
-   Drop support for python 3.5
    ([#654](https://github.com/box/box-python-sdk/pull/654))
-   Remove deprecated code using insensitive language
    ([#651](https://github.com/box/box-python-sdk/pull/651))
-   Enforcing usage of keyword-only arguments in some functions
    ([#656](https://github.com/box/box-python-sdk/pull/656))

### New Features and Enhancements:

-   Remove `six` library and `__future__` imports
    ([#646](https://github.com/box/box-python-sdk/pull/646))
-   Add type hints to method parameters
    ([#650](https://github.com/box/box-python-sdk/pull/650))

### Bug Fixes:

-   Add missing `api_call` decorators on `multiput` calls
    ([#653](https://github.com/box/box-python-sdk/pull/653))
-   Added `py.typed` file for `mypy` to recognise type hints
    ([#657](https://github.com/box/box-python-sdk/pull/657))

## [2.14.0] (2021-12-08)

### New Features and Enhancements:

-   Add `admin_logs_streaming` support for events stream
    ([#623](https://github.com/box/box-python-sdk/pull/623))
-   Add `vanity_name` parameter for creating shared link to
    a file or folder
    ([#637](https://github.com/box/box-python-sdk/pull/637))
-   Add getting files and file versions under retention for a retention
    policy assignment
    ([#633](https://github.com/box/box-python-sdk/pull/633))
-   Support base item operations for WebLink class
    ([#639](https://github.com/box/box-python-sdk/pull/639))

### Bug Fixes:

-   Limit cryptography to version \<3.5.0
    ([#636](https://github.com/box/box-python-sdk/pull/636))
-   Avoid raising 404 when a thumbnail cannot be generated for a file
    ([#642](https://github.com/box/box-python-sdk/pull/642))

## [2.13.0] (2021-09-30)

### New Features and Enhancements:

-   Sensitive language replacement
    ([#609](https://github.com/box/box-python-sdk/pull/609))
-   Add BoxSign support
    ([#617](https://github.com/box/box-python-sdk/pull/617))

### Bug Fixes:

-   Upgrade cryptography to version 3
    ([#620](https://github.com/box/box-python-sdk/pull/620))

## [2.12.1] (2021-06-16)

### Bug Fixes:

-   Fix bug when thumbnail representations are not found
    ([#597](https://github.com/box/box-python-sdk/pull/597))

## [2.12.0] (2021-04-16)

### New Features and Enhancements:

-   Add metadata query functionality
    ([#574](https://github.com/box/box-python-sdk/pull/574))
-   Add folder lock functionality
    ([#581](https://github.com/box/box-python-sdk/pull/581))
-   Add search query support for the
    `include_recent_shared_links` field
    ([#582](https://github.com/box/box-python-sdk/pull/582))
-   Update `get_groups()` to use documented parameter to
    filter by name
    ([#586](https://github.com/box/box-python-sdk/pull/586))

## [2.11.0] (2021-01-11)

### New Features and Enhancements:

-   Deprecate and add method for getting a thumbnail
    ([#572](https://github.com/box/box-python-sdk/pull/572))

## [2.10.0] (2020-10-02)

### New Features and Enhancements:

-   Add support for `copyInstanceOnItemCopy` field for
    metadata templates
    ([#546](https://github.com/box/box-python-sdk/pull/546))
-   Allow creating tasks with the `action` and
    `completion_rule` parameters
    ([#544](https://github.com/box/box-python-sdk/pull/544))
-   Add zip functionality
    ([#539](https://github.com/box/box-python-sdk/pull/539))

### Bug Fixes:

-   Fix bug with updating a collaboration role to owner
    ([#536](https://github.com/box/box-python-sdk/pull/536))
-   Allow ints to be passed in as item IDs
    ([#530](https://github.com/box/box-python-sdk/pull/530))

## [2.9.0] (2020-06-23)

-   Fix exception handling for OAuth
-   Fix path parameter sanitization

## [2.8.0] (2020-04-24)

-   Added support for token exchange using shared links
-   Added the ability to pass in a SHA1 value for file uploads

## [2.7.1] (2020-01-21)

-   Fixed bug in `_get_retry_request_callable` introduced
    in release 2.7.0 which caused chunked uploads to fail

## [2.7.0] (2020-01-16)

-   Fixed bug in `get_admin_events` function which caused
    errors when the optional `event_types` parameter was
    omitted.
-   Add marker based pagination for listing users.
-   Added support for more attribute parameters when uploading new files
    and new versions of existing files.
-   Combined preflight check and lookup of accelerator URL into a single
    request for uploads.
-   Fixed JWT retry logic so a new JTI claim is generated on each retry.
-   Fixed bug where JWT authentication requests returned incorrect error
    codes.
-   Fixed retry logic so when a `Retry-After` header is
    passed back from the API, the SDK waits for the amount of time
    specified in the header before retrying.

## [2.6.1] (2019-10-24)

-   Added `api_call` decorator for copy method.

## [2.6.0] (2019-08-29)

-   Added a new get events function with created_before, created_after,
    and event_type parameters

## [2.5.0] (2019-06-20)

-   Allowed passing `None` to clear configurable_permission
    field in the add_member() method.

## [2.4.1] (2019-05-16)

-   Patch release for issues with v2.4.0.

## [2.4.0] (2019-05-16)

-   Added ability to set metadata on a
    [file](https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md#set-metadata)
    or a
    [folder](https://github.com/box/box-python-sdk/blob/main/docs/usage/folders.md#set-metadata)

## [2.3.2] (2019-03-29)

-   Fixing an issue in v2.3.1 where package could not be installed.

## [2.3.1] (2019-03-29)

-   Fixing an issue in v2.3.0 where package could not be installed.

## [2.3.0] (2019-03-28)

-   Added the ability to set [file description upon
    upload](https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md#upload-a-file)
-   Added support for [basic authenticated proxy and unauthenticated
    proxy](https://github.com/box/box-python-sdk/blob/main/docs/usage/configuration.md#proxy)

## [2.2.2] (2019-03-14)

-   Updated requests-toolbelt dependency restriction.

## [2.2.1] (2019-02-15)

-   Fixing an issue in v2.2.0 where package could not be installed.

## [2.2.0] (2019-02-14)

-   Added abilty for user to [retrieve an
    avatar](https://github.com/box/box-python-sdk/blob/main/docs/usage/user.md#get-the-avatar-for-a-user)
    for a user.
-   Changed retry strategy to use exponential backoff with randomized
    jitter.

## [2.1.0] (2019-02-07)

-   Added ability for user to [chunk upload
    files](https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md#chunked-upload)
    and resume uploads for interrupted uploads.
-   Added ability to [verify webhook
    message](https://github.com/box/box-python-sdk/blob/main/docs/usage/webhook.md#validate-webhook-message).
-   Added ability for user to add metadata classification to
    [files](https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md#set-a-classification)
    and
    [folders](https://github.com/box/box-python-sdk/blob/main/docs/usage/folders.md#set-a-classification).
-   Bugfix where calling `.response_object()` method on an API object
    could throw.

## [2.0.0]

### ⚠ Breaking Changes

-   Python 2.6 is no longer supported.

-   Python 3.3 is no longer supported.

-   `client.search()` now returns a `Search` object that exposes a
    `query()` method to call the Search API. Use
    `client.search().query(**search_params)` instead of
    `client.search(**search_params)`.

-   `client.get_memberships(...)` has a change in signature. The limit
    and offset parameters have swapped positions to keep consistency
    with the rest of the SDK.

-   `client.groups(...)` has been changed to `client.get_groups`. The
    limit and offset parameters have swapped positions.

-   The `unshared_at` parameter for `item.create_shared_link(...)` and
    `file.get_shared_link_download_url(...)` now takes an
    https://tools.ietf.org/html/rfc3339#section-5.8
    `unicode` string instead of a `datetime.date`. Users migrating from
    v1.x can pass the value of `date.isoformat()` instead of the `date`
    object itself.

-   `Events.get_events(...)` now returns a list of `Event` instances
    rather than a list of `dict` representing events. `Event` inherits
    from `Mapping` but will not have all the same capabilities as
    `dict`.

    -   Your code is affected if you use `Events.get_events(...)` and
        expect a list of `dict` rather than a list of `Mapping`. For
        example, if you use `__setitem__` (`event['key'] = value`),
        `update()`, `copy()`, or if your code depends on the `str` or
        `repr` of the `Event`. Use of `__getitem__` (`event['key']`),
        `get()`, and other `Mapping` methods is unaffected. See
        <https://docs.python.org/2.7/library/collections.html#collections-abstract-base-classes>
        for methods supported on `Mapping` instances.
    -   Migration: If you still need to treat an `Event` as a `dict`,
        you can get a deepcopy of the original `dict` using the new
        property on `BaseAPIJSONObject`, `response_object`.

-   `LoggingNetwork` has been removed. Logging calls are now made from
    the `DefaultNetwork` class. In addition, the logging format strings
    in this class have changed in a way that will break logging for any
    applications that have overridden any of these strings. They now use
    keyword format placeholders instead of positional placeholders. All
    custom format strings will now have to use the same keyword format
    placeholders. Though this is a breaking change, the good news is
    that using keyword format placeholders means that any future changes
    will be automatically backwards-compatibile (as long as there
    aren\'t any changes to change/remove any of the keywords).

-   `File.update_contents()` and `File.update_contents_with_stream()`
    now correctly return a `File` object with the correct internal JSON
    structure. Previously it would return a `File` object where the file
    JSON is hidden inside `file['entries'][0]`. This is a bugfix, but
    will be a breaking change for any clients that have already written
    code to handle the bug.

-   Comparing two objects (e.g. a `File` and a `Folder`) that have the
    same Box ID but different types with `==` will now correctly return
    `False`.

-   The following methods now return iterators over the entire
    collection of returned objects, rather than a single page:

    -   `client.users()`
    -   `client.groups()`
    -   `client.search().query()`
    -   `folder.get_items()`

    Since `folder.get_items()` now returns an iterator,
    `folder.get_items_limit_offset()` and `folder.get_items_marker()`
    have been removed. To use marker based paging with
    `folder.get_items()`, pass the `use_marker=True` parameter and
    optionally specify a `marker` parameter to begin paging from that
    point in the collection.

    Additionally, `group.membership()` has been renamed to
    `group.get_memberships()`, and returns an iterator of membership
    objects. This method no longer provides the option to return tuples
    with paging information.

-   The `Translator` class has been reworked; `translator.get(...)`
    still returns the constructor for the object class corresponding to
    the passed in type, but `translator.translate(...)` now takes a
    `Session` and response object directly and produces the translated
    object. This method will also translate any nested objects found.

    -   This change obviates the need for `GroupMembership` to have a
        custom constructor; it now uses the default `BaseObject`
        constructor.

### Features

-   All publicly documented API endpoints and parameters should now be
    supported by the SDK
-   Added more flexibility to the object translation system:
    -   Can create non-global `Translator` instances, which can extend
        or not-extend the global default `Translator`.
    -   Can initialize `BoxSession` with a custom `Translator`.
    -   Can register custom subclasses on the `Translator` which is
        associated with a `BoxSession` or a `Client`.
    -   All translation of API responses now use the `Translator` that
        is referenced by the `BoxSession`, instead of directly using the
        global default `Translator`.
    -   Nested objects are now translated by `translator.translate()`
-   When the `auto_session_renewal` is `True` when calling any of the
    request methods on `BoxSession`, if there is no access token,
    `BoxSession` will renew the token before making the request.
    This saves an API call.
-   Auth objects can now be closed, which prevents them from being used
    to request new tokens. This will also revoke any existing tokens
    (though that feature can be disabled by passing `revoke=False`).
    Also introduces a `closing()` context manager method, which will
    auto-close the auth object on exit.
-   Various enhancements to the `JWTAuth` baseclass:
    -   The `authenticate_app_user()` method is renamed to
        `authenticate_user()`, to reflect that it may now be used to
        authenticate managed users as well. See the method docstring for
        details. `authenticate_app_user()` is now an alias of
        `authenticate_user()`, in order to not introduce an unnecessary
        backwards-incompatibility.
    -   The `user` argument to `authenticate_user()` may now be either a
        user ID string or a `User` instance. Before it had to be a
        `User` instance.
    -   The constructor now accepts an optional `user` keyword argument,
        which may be a user ID string or a `User` instance. When this is
        passed, `authenticate_user()` and can be called without passing
        a value for the `user` argument. More importantly, this means
        that `refresh()` can be called immediately after construction,
        with no need for a manual call to `authenticate_user()`.
        Combined with the aforementioned improvement to the
        `auto_session_renewal` functionality of `BoxSession`, this means
        that authentication for `JWTAuth` objects can be done completely
        automatically, at the time of first API call.
    -   The constructor now supports passing the RSA private key in two
        different ways: by file system path (existing functionality), or
        by passing the key data directly (new functionality). The
        `rsa_private_key_file_sys_path` parameter is now optional, but
        it is required to pass exactly one of
        `rsa_private_key_file_sys_path` or `rsa_private_key_data`.
    -   Document that the `enterprise_id` argument to `JWTAuth` is
        allowed to be `None`.
    -   `authenticate_instance()` now accepts an `enterprise` argument,
        which can be used to set and authenticate as the enterprise
        service account user, if `None` was passed for `enterprise_id`
        at construction time.
    -   Authentications that fail due to the expiration time not falling
        within the correct window of time are now automatically retried
        using the time given in the Date header of the Box API response.
        This can happen naturally when the system time of the machine
        running the Box SDK doesn\'t agree with the system time of the
        Box API servers.
-   Added an `Event` class.
-   Moved `metadata()` method to `Item` so it\'s now available for
    `Folder` as well as `File`.
-   The `BaseAPIJSONObject` baseclass (which is a superclass of all API
    response objects) now supports `__contains__` and `__iter__`. They
    behave the same as for `Mapping`. That is, `__contains__` checks for
    JSON keys in the object, and `__iter__` yields all of the object\'s
    keys.
-   Added a `RecentItem` class.
-   Added `client.get_recent_items()` to retrieve a user\'s recently
    accessed items on Box.
-   Added support for the `can_view_path` parameter when creating new
    collaborations.
-   Added `BoxObjectCollection` and subclasses
    `LimitOffsetBasedObjectCollection` and `MarkerBasedObjectCollection`
    to more easily manage paging of objects from an endpoint. These
    classes manage the logic of constructing requests to an endpoint and
    storing the results, then provide `__next__` to easily iterate over
    the results. The option to return results one by one or as a `Page`
    of results is also provided.
-   Added a `downscope_token()` method to the `Client` class. This
    generates a token that has its permissions reduced to the provided
    scopes and for the optionally provided `File` or `Folder`.
-   Added methods for configuring `JWTAuth` from config file:
    `JWTAuth.from_settings_file` and `JWTAuth.from_settings_dictionary`.
-   Added `network_response` property to `BoxOAuthException`.
-   API Configuration can now be done per `BoxSession` instance.

### Other

-   Added extra information to `BoxAPIException`.
-   Added `collaboration()` method to `Client`.
-   Reworked the class hierarchy. Previously, `BaseEndpoint` was the
    parent of `BaseObject` which was the parent of all smart objects.
    Now `BaseObject` is a child of both `BaseEndpoint` and
    `BaseAPIJSONObject`. `BaseObject` is the parent of all objects that
    are a part of the REST API. Another subclass of `BaseAPIJSONObject`,
    `APIJSONObject`, was created to represent pseudo-smart objects such
    as `Event` that are not directly accessible through an API endpoint.
-   Added `network_response_constructor` as an optional property on the
    `Network` interface. Implementations are encouraged to override this
    property, and use it to construct `NetworkResponse` instances. That
    way, subclass implementations can easily extend the functionality of
    the `NetworkResponse`, by re-overriding this property. This property
    is defined and used in the `DefaultNetwork` implementation.
-   Move response logging to a new `LoggingNetworkResponse` class (which
    is made possible by the aforementioned
    `network_response_constructor` property). Now the SDK decides
    whether to log the response body, based on whether the caller reads
    or streams the content.
-   Add more information to the request/response logs from
    `LoggingNetwork`.
-   Add logging for request exceptions in `LoggingNetwork`.
-   Bugfix so that the return value of `JWTAuth.refresh()` correctly
    matches that of the auth interface (by returning a tuple of ((access
    token), (refresh token or None)), instead of just the access token).
    In particular, this fixes an exception in `BoxSession` that always
    occurred when it tried to refresh any `JWTAuth` object.
-   Fixed an exception that was being raised from
    `ExtendableEnumMeta.__dir__()`.
-   CPython 3.6 support.
-   Increased required minimum version of six to 1.9.0.

## [1.5.3] (2016-05-26)

-   Bugfix so that `JWTAuth` opens the PEM private key file in `'rb'`
    mode.

## [1.5.2] (2016-05-19)

-   Bugfix so that `OAuth2` always has the correct tokens after a call
    to `refresh()`.

## [1.5.1] (2016-03-23)

-   Added a `revoke()` method to the `OAuth2` class. Calling it will
    revoke the current access/refresh token pair.

## [1.5.0] (2016-03-17)

-   Added a new class, `LoggingClient`. It\'s a `Client` that uses the
    `LoggingNetwork` class so that requests to the Box API and its
    responses are logged.
-   Added a new class, `DevelopmentClient` that combines `LoggingClient`
    with the existing `DeveloperTokenClient`. This client is ideal for
    exploring the Box API or for use when developing your application.
-   Made the `oauth` parameter to `Client` optional. The constructor now
    accepts new parameters that it will use to construct the `OAuth2`
    instance it needs to auth with the Box API.
-   Changed the default User Agent string sent with requests to the Box
    API. It is now \'box-python-sdk-\<version\>\'.
-   Box objects have an improved `__repr__`, making them easier to
    identify during debugging sessions.
-   Box objects now implement `__dir__`, making them easier to explore.
    When created with a Box API response, these objects will now include
    the API response fields as attributes.

## [1.4.2] (2016-02-23)

-   Make sure that `__all__` is only defined once, as a list of `str`.
    Some programs (e.g. PyInstaller) naively parse \_\_init\_\_.py
    files, and if `__all__` is defined twice, the second one will be
    ignored. This can cause `__all__` to appear as a list of `unicode`
    on Python 2.

-   Create wheel with correct conditional dependencies and license file.

-   Change the `license` meta-data from the full license text, to just a
    short string, as specified in \[1\]\[2\].

    \[1\]
    \<<https://docs.python.org/3.5/distutils/setupscript.html#additional-meta-data>\>

    \[2\] \<<https://www.python.org/dev/peps/pep-0459/#license>\>

-   Include entire test/ directory in source distribution.
    test/\_\_init\_\_.py was previously missing.

-   Update documentation.

## [1.4.1] (2016-02-11)

-   Files now support getting a direct download url.

## [1.4.0] (2016-01-05)

-   Added key id parameter to JWT Auth.

## [1.3.3] (2016-01-04)

### Bugfixes

-   Fixed import error for installations that don\'t have redis
    installed.
-   Fixed use of `raw_input` in the developer token auth for py3
    compatibility.

## [1.3.3] (2015-12-22)

-   Added a new class, `DeveloperTokenClient` that makes it easy to get
    started using the SDK with a Box developer token. It uses another
    new class, `DeveloperTokenAuth` for auth.

### Bugfixes

-   Added limit, offset, and filter_term parameters to `client.users()`
    to match up with the Box API.

## [1.3.2] (2015-11-16)

-   Fix `boxsdk.util.log.setup_logging()` on Python 3.

## [1.3.1] (2015-11-06)

-   Add requests-toolbelt to setup.py (it was accidentally missing from
    1.3.0).

## [1.3.0] (2015-11-05)

-   CPython 3.5 support.
-   Support for cryptography\>=1.0 on PyPy 2.6.
-   Travis CI testing for CPython 3.5 and PyPy 2.6.0.
-   Added a logging network class that logs requests and responses.
-   Added new options for auth classes, including storing tokens in
    Redis and storing them on a remote server.
-   Stream uploads of files from disk.

## [1.2.2] (2015-07-22)

-   The SDK now supports setting a password when creating a shared link.

## [1.2.1] (2015-07-22)

### Bugfixes

-   Fixed an ImportError for installs that didn\'t install the \[jwt\]
    extras.

## [1.2.0] (2015-07-13)

-   Added support for Box Developer Edition. This includes JWT auth
    (auth as enterprise or as app user), and `create_user`
    functionality.
-   Added support for setting shared link expiration dates.
-   Added support for setting shared link permissions.
-   Added support for \'As-User\' requests. See
    <https://developer.box.com/en/guides/authentication/oauth2/as-user/>
-   Improved support for accessing shared items. Items returned from the
    `client.get_shared_item` method will remember the shared link (and
    the optionally provided shared link password) so methods called on
    the returned items will be properly authorized.

## [1.1.7] (2015-05-28)

-   Add context_info from failed requests to BoxAPIException instances.

### Bugfixes

-   `Item.remove_shared_link()` was trying to return an incorrect
    (according to its own documentation) value, and was also attempting
    to calculate that value in a way that made an incorrect assumption
    about the API response. The latter problem caused invocations of the
    method to raise TypeError. The method now handles the response
    correctly, and correctly returns type `bool`.

## [1.1.6] (2015-04-17)

-   Added support for the Box accelerator API for premium accounts.

## [1.1.5] (2015-04-03)

-   Added support for preflight check during file uploads and updates.

## [1.1.4] (2015-04-01)

-   Added support to the search endpoint for metadata filters.
-   Added support to the search endpoint for filtering based on result
    type and content types.

## [1.1.3] (2015-03-26)

-   Added support for the /shared_items endpoint.
    `client.get_shared_item` can be used to get information about a
    shared link. See <https://developers.box.com/docs/#shared-items>

## [1.1.2] (2015-03-20)

### Bugfixes

-   Certain endpoints (e.g. search, get folder items) no longer raise an
    exception when the response contains items that are neither files
    nor folders.

## [1.1.1] (2015-03-11)

-   A minor change to namespacing. The `OAuth2` class can now be
    imported directly from `boxsdk`. Demo code has been updated to
    reflect the change.

## [1.1.0] (2015-03-02)

### Features

-   The SDK now supports Box metadata. See the [metadata
    docs](https://developers.box.com/metadata-api/) for more
    information.
-   The object paging API has been improved. SDK extensions that need
    fine-grained control over when the next "page" of API results will
    be fetched can now do that.

### Example Code

-   The example code has been improved to be more robust and to work
    with all Python versions supported by the SDK (CPython 2.6-2.7,
    CPython 3.3-3.4, and PyPy).
-   The example code has an example on how to use the new metadata
    feature.
-   The README has improved code examples.

### Bugfixes

-   Oauth2 redirect URIs containing non-ASCII characters are now
    supported.
