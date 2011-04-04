===============
Developing Grok
===============

.. contents::

Making releases of packages that make up Grok
=============================================

Making releases
===============

The release procedure for the packages that comprise Grok, like ``grok`` and
the ``grokcore.*`` family of libraries, follows ZTK's `official release
guidelines`_.

.. _`official release guidelines`: http://docs.zope.org/zopetoolkit/process/releasing-software.html

Automating the release
----------------------

Even if it can be useful to follow these release steps by hand, most of it is
automated in the `zest.releaser`_ package that is included in groktoolkit's
``buildout.cfg``. Using this tool will prevent making mistakes caused by the
rather repetitive nature of the release process.

.. _`zest.releaser`: http://pypi.python.org/pypi/zest.releaser

Before commencing the release it is important to to make sure the packages'
changelog is up to date. A useful tool, part of the `zest.releaser`_ tool
chain, is the ``lasttagdiff`` command. This command will output the changes
between the latest release tag and the current trunk:

  $ ./bin/lasttagdiff.

After having reviewed the changes and updating the changelog of a package (and
making sure any changes are commited!) the actual release can be made::

  $ ./bin/fullrelease

Part of the ``fullrelease`` procedure is the registration and upload of the
packge to the Python `Package Index <http://pypi.pytthon.org/>`_. Make sure
you're actually allowed to upload the particular package to the index!

Making the groktoolkit release
==============================

Releases of groktoolkit are similar to that of making releases of the
individual packages. The ``zest.releaser`` tool will help you create the
release tag and update the version information.

The groktoolkit contains a post-release step triggered by ``zest.releaser``
that will upload a ``versions.cfg`` file to::

   grok.zope.org:/var/www/html/grok/releaseinfo/[VERSION]/versions.cfg

Manual groktoolkit post-release steps
-------------------------------------

After having released the groktoolkit, the following steps should be taken:

1. Grokproject generates a ``buildout.cfg`` with an ``extends`` directive
   pointing to the most recent release versions file. It determines the URL
   to this versions file by reading http://grok.zope.org/releaseinfo/current.
   This file needs to be updated to point to the uploaded ``*.cfg`` file for
   the official "final" releases.

2. Add a document with the release announcement in the `releases folder`_
   Name it after the release version number. Summarize what is in
   ``CHANGES.txt``. Make sure you move it to become the first item of the
   releases folder. You can move it up by using the contents view of the
   folder. The last column in that table presents a handle by which you can
   drag up the document in the folder.

   .. _`releases folder`: http://grok.zope.org/project/releases/

3. Official Documentation: Create a build of the docs from the tagged
   release and copy it to the server. The steps are roughly as follows::

   $ svn co svn+ssh://svn.zope.org/repos/main/groktoolkit/tags/[VERSION] gtk
   $ cd gtk
   $ python bootstrap.py
   $ ./bin/buildout -c documentation.cfg
   $ cd doc && make clean && make all
   $ scp -r _build/html grok.zope.org:/var/www/html/grok/doc/[VERSION]
   $ ssh grok.zope.org "rm /var/www/html/grok/doc/current; ln -s /var/www/html/grok/doc/[VERSION] /var/www/html/grok/doc/current"

4. Create a news item in the `blog folder`_ announcing the news. The text
   can be based on the release notes written at point 7.

   .. _`blog folder`: http://grok.zope.org/blog/

5. Make both the new release notes, the new news item, as well as the
   updated upgrade notes public.

6. Update the sidebar in the site. You can edit it here::

     http://grok.zope.org/portal_skins/custom/portlet_download/manage_main

8. Send out an email to at least zope-announce@zope.org as well as grok-
   dev@zope.org announcing the new release. The text can be based on the
   release notes written at step 2.

9. Update the Grok Wikipedia article with the information about the latest
   release: http://en.wikipedia.org/wiki/Grok_(web_framework)

Binary eggs on Windows
----------------------

Grok aims to work on Windows as well. This is not a problem for the most part,
but takes special attention when updating the list of dependencies. The follow
eggs need a compiler on Unixy platforms, and a binary egg on Windows::

  zope.i18nmessageid
  zope.interface
  zope.security
  zope.container
  ZODB3
  zope.hookable
  zope.proxy

Please make sure a Windows version of the egg is available when you update a
dependency!
