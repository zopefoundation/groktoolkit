# Generate package list information for trunk and tags of the Grok Toolkit.
# This script has been shamelessly copied from the Zope Toolkit documentation
# and heavily modified.

import ConfigParser
import os
import os.path
import py.path
import socket
import StringIO
import sys
import urllib2
import xml.etree.ElementTree

socket.setdefaulttimeout(10)

TABLE_HEADER = """\
.. list-table::
    :class: packagelist
    :widths: 25 10 65
    :header-rows: 1

    * - Name
      - Version
      - Description\
"""

PACKAGE_LINE_BASE = """
    * - `%(name)s <%(homepage)s>`_
      - %(version)s
      - %(description)s\
"""

PACKAGE_LINE = PACKAGE_LINE_BASE

GENERATED_WARNING = """\
.. This file is generated. Please do not edit manually or check in.
"""

DOAP_NS = 'http://usefulinc.com/ns/doap#'
GROKTOOLKIT_ROOT = py.path.svnurl('http://svn.zope.org/repos/main/groktoolkit')
TAGS_URL = GROKTOOLKIT_ROOT/'tags'

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
        description = ' '.join(
            doap.find('//{%s}shortdesc' % DOAP_NS).text.splitlines())
        homepage = 'http://pypi.python.org/pypi/%s/%s' % (package, version)
        print >>out, line % dict(
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

def get_releases():
    tags = TAGS_URL.listdir()
    tags.reverse()
    releases = []
    for tag in tags:
        releases.append((tag.basename, tag))
        break
    return releases

def write_package_lists(releases, path):
    for release, location in releases:
        print 'Writing package list for "%s"' % release

        config = ConfigParser.RawConfigParser()
        config.optionxform = str
        fp = StringIO.StringIO((location/'grok.cfg').read())
        config.readfp(fp)

        output = open(os.path.join(path, 'packages-%s.rst' % release), 'w')

        print >>output, GENERATED_WARNING

        heading = 'Grok %s packages' % release
        print >>output, '=' * len(heading)
        print >>output, heading
        print >>output, '=' * len(heading)

        ztk_version = '1.1'
        print >>output, 'Zope Toolkit %s' % ztk_version
        print >>output, '------------------------------'
        print >>output, '`Overview of ZTK-%s <http://docs.zope.org/zopetoolkit/releases/overview-%s.html>`' % (ztk_version, ztk_version)

        print >>output, 'Packages'
        print >>output, '--------'
        included = packages(config, 'included')
        package_list(included, config, output)

        deprecating = packages(config, 'deprecating')
        if deprecating:
            print >>output, 'Deprecating'
            print >>output, '-----------'
            package_list(deprecating, versions, output)

        print >>output, 'Other dependencies'
        print >>output, '------------------'
        all = config.options('versions')
        dependencies = (set(all) - set(included)) - set(deprecating)
        package_list(dependencies, config, output)
        output.close()

def write_overview(releases, path):
    print "Writing overview"

    output = open(os.path.join(path, 'index.rst'), 'w')
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
    overview-%s""" % release

    for release, location in releases:
        overview = open(os.path.join(path, 'overview-%s.rst' % release), 'w')
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

if __name__ == '__main__':
    releases = get_releases()
    path = os.path.abspath(os.path.join('releases'))
    write_package_lists(releases, path)
    write_overview(releases, path)
