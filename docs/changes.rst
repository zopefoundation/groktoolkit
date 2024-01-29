
.. note:: The buildout versions file for all current versions can be found at https://zopefoundation.github.io/groktoolkit/

4.0 (unreleased)
----------------

- Update to ``grok 5.0``. This requires us to drop support for:

  - ``grokcore.xmlrpc``

  - ``grokcore.rest``

  - ``grokcore.json``

- Drop support ``zope.fanstatic``, as this repository has been archived and
  does not support Python 3.12.

- Remove ``fanstatic`` from the list of version pins as it was only needed by
  ``zope.fanstatic``.


3.0 (2023-12-20)
----------------

- Add support for Python 3.12.

- Drop the following packages from GROK toolkit:

  - grokcore.rest (it is still a dependency of some packages)
  - z3c.autoinclude (it is still a dependency of some packages)
