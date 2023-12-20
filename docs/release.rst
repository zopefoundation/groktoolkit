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

Releasing a new GROK toolkit version
=====================================

Updating versions of dependencies
---------------------------------

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

Creating a release
------------------

* Make sure all tests are running successfully.
* Decide on a version number for the new release, taking https://semver.org/
  into account. (Please note: dropping support for a Python version is
  considered a major change as it enforces changes for users of GROK toolkit
  who are using the no longer supported Python version.)
* Update ``docs/changes.rst`` with a new entry describing your release or
  update an existing not yet released one. (also set the release date).
* Check the documentation builds using ``tox -e docs`` and proof-read your
  changes.
* Commit your changes to ``git``.
* Create a git tag using ``git tag`` and your version number.
* Push your changes, make sure also the tag is pushed.
* Switch to the branch ``gh-pages``.
* Run ``build_indexes.sh``, add and commit the changes.
* Push the changes to GitHub, after some seconds the changes should appear at
  https://zopefoundation.github.io/zopetoolkit/.
