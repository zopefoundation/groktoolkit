# Generate package list information for trunk and tags of the Grok Toolkit.
# This script has been shamelessly copied from the Zope Toolkit documentation
# and heavily modified.

import ConfigParser
import StringIO
import os
import os.path
import socket
import urllib2
import xml.etree.ElementTree
import py.path

socket.setdefaulttimeout(10)

TABLE_HEADER = """\
.. list-table::
    :class: packagelist
    :widths: 25 10 40 25
    :header-rows: 1

    * - Name
      - Version
      - Description
      - Links\
"""

PACKAGE_LINE_BASE = """
    * - `%(name)s <%(homepage)s>`_
      - %(version)s
      - %(description)s\
"""

DEPENDENCY_PACKAGE_LINE = PACKAGE_LINE_BASE + """
      - \
"""

PACKAGE_LINE = PACKAGE_LINE_BASE + """
      - `Bugs <http://bugs.launchpad.net/%(name)s>`_ |
        `Subversion <http://svn.zope.org/%(name)s>`_ \
"""

GENERATED_WARNING = """\
.. This file is generated. Please do not edit manually or check in.
"""

DOAP_NS = 'http://usefulinc.com/ns/doap#'
GROKTOOLKIT_ROOT = py.path.svnurl('http://svn.zope.org/repos/main/groktoolkit')

def package_list(
        packages, config, out, line=PACKAGE_LINE):
    print >>out, TABLE_HEADER
    for package in sorted(packages):
        version = config.get('versions', package)
        doap_xml = urllib2.urlopen(
            'http://pypi.python.org/pypi?:action=doap&name=%s&version=%s' %
            (package, version)).read()
        doap_xml = StringIO.StringIO(doap_xml.replace('\f', ''))
        doap = xml.etree.ElementTree.ElementTree()
        doap.parse(doap_xml)
        description = doap.find('//{%s}shortdesc' % DOAP_NS).text
        homepage = 'http://pypi.python.org/pypi/%s/%s' % (package, version)
        print >>output, line % dict(
            name=package, homepage=homepage,
            description=description, version=version)
    print >>out

def packages(config, key):
    if not config.has_option('grok', key):
        print 'Key "%s" not found in section [grok]' % key
        return []
    result = config.get('grok', key).split('\n')
    result = filter(None, map(str.strip, result))
    return result

releases = []
tags_url = GROKTOOLKIT_ROOT/'tags'

for tag_url in tags_url.listdir().reverse():
    releases.append((tag_url.basename, tag_url))

for release, location in releases:
    print 'Writing package list for "%s"' % release

    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    fp = StringIO.StringIO((location/'grok.cfg').read())
    config.readfp(fp)

    output = open(
        os.path.join('doc', 'releases', 'packages-%s.rst' % release), 'w')

    print >>output, GENERATED_WARNING

    heading = 'Grok %s packages' % release
    print >>output, heading
    print >>output, '=' * len(heading)

    included = packages(config, 'included')
    package_list(included, config, output)

    deprecating = packages(config, 'deprecating')
    if deprecating:
        print >>output, 'Deprecating'
        print >>output, '-----------'
        package_list(deprecating, versions, output)

    print >>output, 'Dependencies'
    print >>output, '------------'
    all = config.options('versions')
    dependencies = set(all) - (set(included) | set(deprecating))
    package_list(dependencies, config, output, DEPENDENCY_PACKAGE_LINE)
    output.close()

print "Writing overview"

output = open(os.path.join('doc', 'releases', 'index.rst'), 'w')
print >>output, GENERATED_WARNING
print >>output, """
Releases
========

This area collects release-specific information about the toolkit including a
list of backward-incompatible changes, new techniques developed, and libraries
included.

.. toctree::
    :maxdepth: 1

"""

for release, location in releases:
    print >>output, """
    overview-%s\
""" % release


for release, location in releases:
    overview = open(
        os.path.join('doc', 'releases', 'overview-%s.rst' % release), 'w')
    print >>overview, GENERATED_WARNING
    title = "Grok %s" % release
    print >>overview, title
    print >>overview, "=" * len(title)
    print >>overview, """
This document covers major changes in this release that can lead to
backward-incompatibilities and explains what to look out for when updating.

.. contents::
    :local:

List of packages
----------------

See the separate `package list <packages-%s.html>`_ document.

""" % release

    #overview.write((location/'README.txt').read())
    overview.close()
