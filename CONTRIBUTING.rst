Contributing
============

All contributions are welcome to this project.

Contributor License Agreement
-----------------------------

Before a contribution can be merged into this project, please fill out
the Contributor License Agreement (CLA) located at::

    http://opensource.box.com/cla

To learn more about CLAs and why they are important to open source
projects, please see the `Wikipedia
entry <http://en.wikipedia.org/wiki/Contributor_License_Agreement>`_.

Code of Conduct
------------------

This project adheres to the `Box Open Code of Conduct <http://opensource.box.com/code-of-conduct/>`_. By participating, you are expected to uphold this code.

How to contribute
-----------------

-  **File an issue** - if you found a bug, want to request an
   enhancement, or want to implement something (bug fix or feature).
-  **Send a pull request** - if you want to contribute code. Please be
   sure to file an issue first.

Pull request best practices
---------------------------

We want to accept your pull requests. Please follow these steps:

Step 1: File an issue
~~~~~~~~~~~~~~~~~~~~~

Before writing any code, please file an issue stating the problem you
want to solve or the feature you want to implement. This allows us to
give you feedback before you spend any time writing code. There may be a
known limitation that can't be addressed, or a bug that has already been
fixed in a different way. The issue allows us to communicate and figure
out if it's worth your time to write a bunch of code for the project.

Step 2: Fork this repository in GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will create your own copy of our repository.

Step 3: Add the upstream source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The upstream source is the project under the Box organization on GitHub.
To add an upstream source for this project, type:

.. code-block:: console

    git remote add upstream git@github.com:box/box-python-sdk.git

This will become useful later.

Step 4: Create a feature branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a branch with a descriptive name, such as ``add-search``.

Step 5: Push your feature branch to your fork
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use `semantic-versioning <https://semver.org/>`_ and the `conventional commit message format <https://www.conventionalcommits.org/en/v1.0.0/>`_. 
Keep a separate feature branch for each issue you want to address. As you develop code, continue to push code to your remote feature branch. Example:

.. code-block:: console

    tag: short description
    longer description here if necessary.

The message summary should be a one-sentence description of the change, and it must be 72 characters in length or shorter. For a list of tags, please `click here <https://github.com/commitizen/conventional-commit-types/blob/master/index.json>`_. Note that you must include the `!` for breaking changes (e.g. `feat!: removed old apis`).

Shown below are examples of the release type that will be done based on a commit message.

Commit Types
~~~~~~~~~~~~

"Semantic versioning" means that changes to the version number of the package (e.g. ``3.42.11`` to ``3.43.0``) are done according to rules that indicate how the change will affect consumers. Read more on the `semver page <https://semver.org/>`_.

The version number is broken into 3 positions ``Major.Minor.Patch``. In semantic release terms, changes to the numbers follow ``Breaking.Feature.Fix``. The ``release`` script parses commit messages and decides what type of release to make based on the types of commits detected since the last release.

The rules for commit types are:

- Anything that changes or removes an API, option, or output format is a breaking change denoted by ``!``.
- Anything that adds new functionality in a backwards-compatible way is a feature (``feat``). Consumers have to upgrade to the new version to use the feature, but nothing will break if they do so.
- Bugfixes (``fix``) for existing behavior are a patch. Consumers don't have to do anything but upgrade.
- Other prefixes, such as ``docs`` or ``chore``, don't trigger releases and don't appear in the changelog. These tags signal that there are **no external changes to _any_ APIs** (including non-breaking ones).

In most cases, commits will be a ``feat`` or ``fix``. Make sure to include the ``!`` in the title if there are non-backwards-compatible changes in the commit.

.. list-table::
   :widths: 50 25 25
   :header-rows: 1

   * - Commit message
     - Release type
     - New version
   * - ``feat!: remove old files endpoints``
     - Major ("breaking") 
     - ``X+1.0.0``
   * - ``feat: add new file upload endpoint``
     - Minor ("feature")
     - ``X.Y+1.0``
   * - ``fix: file streaming during download``
     - Patch ("fix")
     - ``X.Y.Z+1``
   * - ``docs: document files api``
     - No release
     - ``X.Y.Z``
   * - ``chore: remove commented code from file upload``
     - No release
     - ``X.Y.Z``
   * - ``refactor: rename a variable (invisible change)``
     - No release
     - ``X.Y.Z``

Step 6: Rebase
~~~~~~~~~~~~~~

Before sending a pull request, rebase against upstream, such as:

.. code-block:: console

    git fetch upstream
    git rebase upstream/main

This will add your changes on top of what's already in upstream,
minimizing merge issues.

Step 7: Run the tests
~~~~~~~~~~~~~~~~~~~~~

Make sure that all tests are passing before submitting a pull request.

Step 8: Send the pull request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Send the pull request from your feature branch to us. Be sure to include
a description that lets us know what work you did.

Keep in mind that we like to see one issue addressed per pull request,
as this helps keep our git history clean and we can more easily track
down issues.

In addition, feel free to add yourself to AUTHORS.rst if you aren't already listed.
