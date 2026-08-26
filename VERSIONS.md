# Version Lifecycle

We use a modified version of [Semantic Versioning](https://semver.org/) for all changes. It is strongly encouraged that you pin at least the major version and potentially the minor version to avoid pulling in breaking changes. Increasing the major version of an SDK indicates that this SDK underwent significant and substantial changes to support new idioms and patterns in the language. Major versions are introduced when public interfaces (e.g. classes, methods, types, etc.), behaviours, or semantics have changed.

Semantic Versions take the form of `MAJOR.MINOR.PATCH`.

When bugs are fixed in the library in a backwards-compatible way, the PATCH level will be incremented by one. PATCH changes should not break your code and are generally safe for upgrade.

When a new feature set comes online or a small breaking change is introduced, the MINOR version will be incremented by one and the PATCH version resets to zero. MINOR changes may require some amount of manual code change for upgrade. These backwards-incompatible changes will mostly be limited to a small number of function signature changes.

The MAJOR version is used to indicate the family of technology represented by the library. Breaking changes that require extensive reworking of code will cause the MAJOR version to be incremented by one, and the MINOR and PATCH versions will be reset to zero. Since frequent major updates can be very disruptive, we will only introduce this type of breaking change when absolutely necessary.

## Support lifecycle

Each Box SDK README publishes a **[Version schedule](README.md#version-schedule)** table. That table is the source of truth for which **major versions** are **Supported**, when each was first released, and when each reaches **end of life (EOL)**.

After a major version reaches EOL it no longer receives new features, bug fixes, or security patches. Existing applications that pin that version continue to run, but you should plan to upgrade. The version is then marked `EOL` in the README schedule.

Major version releases, breaking changes, and EOL dates are announced through public channels via:

- Box developer documentation, such as the API reference, user guides, and GitHub READMEs.
- Deprecation warnings are added to the SDKs, outlining the path to end-of-support and linking to the SDK documentation.

Deprecations are introduced in minor releases. We will not introduce new deprecations in patch releases. These deprecations will preserve the existing behaviour while emitting a warning that provide guidance on:

- How to achieve similar behaviour if an alternative is available
- The version in which the deprecation will be enforced.

Deprecations will only be enforced in major releases. For example, if a behaviour is deprecated in version 1.2.0, it will continue to work, with a warning, for all releases in the 1.x series. The behaviour will change and the deprecation will be removed in the next major release (2.x.x).
