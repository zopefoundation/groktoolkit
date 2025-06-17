===============
Making releases
===============

.. contents::

Making package releases
=======================

The release procedure for the packages that comprise GROK toolkit, like
``grok`` and the ``grokcore.*`` family of libraries, follows ZTK's `official
release guidelines`_.

.. _`official release guidelines`: https://zopetoolkit.readthedocs.io/en/latest/process/releasing-software.html

Updating versions of dependencies
=================================

Manual way
++++++++++

To get new version pins into GROK toolkit run the following steps:

* Check https://zopefoundation.github.io/zopetoolkit/ whether there is a new
  version of ZTK. If this is the case update in ``grok.cfg`` the URL to
  ``ztk-versions.cfg``.
* ``tox -e checkversions | grep "="``

  This command lists the packages where newer versions are available. (The grep
  is needed to omit the other rubbish rendered by the command call.)
* Update ``grok-versions.cfg`` with these new versions and run ``tox`` to run
  their tests.
* Run the ``checkversion`` call from above again to make sure all possible
  versions are updated.
* If the test runs are successful: create a pull request on GitHub.

Automated way
+++++++++++++

* There is a dependabot configuration automatically updating
  ``dependabot/requirements.txt``.

* And there is a GitHub actions job syncing between
  ``dependabot/requirements.txt`` and ``grok-versions.cfg``.

Releasing a new GROK toolkit version
=====================================

* Make sure all tests are running successfully.
* Check wether the supported Python version are correct in ``grok-versions.cfg``,
  see ``.github/workflows/tests.yml`` for the Python versions under test.
* Decide on a version number for the new release, taking https://semver.org/
  into account. (Please note: dropping support for a Python version is
  **no longer** considered a major change, as it is the usual way of life.)
* Update ``docs/changes.rst`` with a new entry describing your release or
  update an existing not yet released one. (also set the release date).
* Update ``version`` and ``copyright`` in ``docs/conf.py`` to the new version
  number.
* Check the documentation builds using ``tox -e docs`` and proof-read your
  changes.
* Commit your changes to ``git``.
* Create a git tag using ``git tag`` and your version number.
* Push your changes, make sure also the tag is pushed.
* Run ``postrelease`` to update the version number to the next development
  version.
* Switch to the branch ``gh-pages``.
* If you increased the major version number, edit ``build_indexes.sh``: In line
  8 add an ``-l`` parameter for your new major version number.
* Run ``build_indexes.sh``, add and commit the changes.
* Push the changes to GitHub, after some minutes the changes should appear at
  https://zopefoundation.github.io/groktoolkit/.
* Create a new release at
  https://github.com/zopefoundation/groktoolkit/releases.


Setup for Dependabot auto-update
================================

* You need a personal access token of one of the zopefoundation admins. (Currently one of ``icemac`` is used.)
* To create the token go to https://github.com/settings/apps -> Fine-grained personal access tokens:

  * Repository access: ``zopefoundation/groktoolkit``
  * Repository permissions: Read and Write access for Contents
  * Save the token in your clipboard.

* Enter the token at:

  * Actions secrets: https://github.com/zopefoundation/groktoolkit/settings/secrets/actions -> Repository secrets -> ``COMMIT_ACTIONS_TOKEN``
  * Dependabot secrets: https://github.com/zopefoundation/groktoolkit/settings/secrets/dependabot -> Repository secrets -> ``COMMIT_ACTIONS_TOKEN``
