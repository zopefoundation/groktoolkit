
.. note:: The buildout versions file for all current versions can be found at https://zopefoundation.github.io/groktoolkit/

4.0 (unreleased)
----------------

- Update to ``grok 5.0``. This requires us to drop support for:

  - ``grokcore.xmlrpc``

  - ``grokcore.rest``

  - ``grokcore.json``


3.0 (2023-12-20)
----------------

- Add support for Python 3.12.

- Drop the following packages from GROK toolkit:

  - grokcore.rest (it is still a dependency of some packages)
  - z3c.autoinclude (it is still a dependency of some packages)
