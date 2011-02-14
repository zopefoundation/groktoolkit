# Generate package list information for the Grok Toolkit.
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
import pkg_resources

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
    result = config.get('grok', key).splitlines()
    result = filter(None, map(str.strip, result))
    return result

def write_package_list(path, version, use_trunk=False):
    location = GROKTOOLKIT_ROOT / ('tags/%s' % version)
    if use_trunk:
        location = GROKTOOLKIT_ROOT / 'trunk'

    print 'Writing package list for Grok Toolkit "%s"' % version, location

    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    fp = StringIO.StringIO((location/'grok.cfg').read())
    config.readfp(fp)
    output = open(path, 'w')

    print >>output, GENERATED_WARNING

    heading = 'Grok %s packages' % version
    print >>output, '=' * len(heading)
    print >>output, heading
    print >>output, '=' * len(heading)

    print >>output, """
Release yadda yadda.
"""

    #ztk_version = None
    #extends = config.get('buildout', 'extends').splitlines()
    #for extend in extends:
    #    if 'ztk-versions.cfg' not in extend:
    #        continue

    ztk_version = '1.1'
    print >>output, 'Zope Toolkit %s' % ztk_version
    print >>output, '------------------------------'
    print >>output, """
This Grok released is based on Zope Toolkit %s.

`Overview <http://docs.zope.org/zopetoolkit/releases/overview-%s.html>`_ of the
ZTK. List of the ZTK `packages <http://docs.zope.org/zopetoolkit/releases/packages-%s.html>`_
""" % (ztk_version, ztk_version, ztk_version)

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

if __name__ == '__main__':
    path = os.path.abspath(os.path.join('packages.rst'))
    dist = pkg_resources.get_distribution('groktoolkit')
    use_trunk = False
    if dist.precedence <= pkg_resources.DEVELOP_DIST:
        use_trunk = True
    write_package_list(path, dist.version, use_trunk=use_trunk)
