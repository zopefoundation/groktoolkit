
.. note:: The buildout versions file for all current versions can be found at https://zopefoundation.github.io/groktoolkit/

5.5 (unreleased)
----------------

- Include Zope toolkit (ZTK) versions directly into GROK toolkit and run their
  tests here so we no longer depend on ZTK releases to see updates of these
  versions.

5.4 (2025-06-10)
----------------

- Completely drop ``z3c.autoinclude`` as all packages in groktoolkit no longer
  use it (it got deprecated in version 3.0).

- Update to zopetoolkit version 3.3.


5.3 (unreleased)
----------------

- Drop support for Python 3.8.

- Update to zopetoolkit version 3.2.

- Update dependencies to their newest versions.

5.2 (2024-11-08)
----------------

- Add support for Python 3.13.

- Drop version pins for ``twine`` and ``pkginfo`` as they are not used and we
  pinned incompatible versions resulting in an error downstream.

- Update zopetoolkit to version 3.1.

- Add ``zope.testbrowser`` to the list of tested packages.

5.1 (2024-08-22)
----------------

- Drop support for Python 3.7.

- Update to ZTK 3.0.

- Update dependencies to their newest versions.

5.0 (2024-04-23)
----------------

- Drop ``grokui.admin`` from list of version pins and from all tutorial apps as
  its repository has been archived.

- Update dependencies to their newest versions.

- Update to ZTK 2.2.


4.0 (2024-01-29)
----------------

- Update to ``grok 5.0``. This requires us to drop support for:

  - ``grokcore.xmlrpc``

  - ``grokcore.rest``

  - ``grokcore.json``

- Drop support for ``zope.fanstatic``, as this repository has been archived and
  it does not support Python 3.12.

- Remove ``fanstatic`` from the list of version pins as it was only needed by
  ``zope.fanstatic``.


3.0 (2023-12-20)
----------------

- Add support for Python 3.12.

- Drop the following packages from GROK toolkit:

  - grokcore.rest (it is still a dependency of some packages)
  - z3c.autoinclude (it is still a dependency of some packages)
