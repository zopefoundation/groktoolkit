# Generate package list information for the Grok Toolkit.
# This script has been shamelessly copied from the Zope Toolkit documentation
# and heavily modified.

import os
import os.path
import socket
import xml.etree.ElementTree

import pkg_resources

import ConfigParser
import py.path
import StringIO
import urllib2


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
    print(TABLE_HEADER, file=out)
    for package in sorted(packages):
        version = config.get('versions', package)
        if package == 'IPython':
            # XXX ugly ugly ugly hack.
            package = 'ipython'
        doap_xml = urllib2.urlopen(
            'http://pypi.python.org/pypi?:action=doap&name=%s&version=%s' %
            (package, version)).read()
        doap_xml = StringIO.StringIO(doap_xml.replace('\f', ''))
        doap = xml.etree.ElementTree.ElementTree()
        doap.parse(doap_xml)
        description = ' '.join(
            doap.find('//{%s}shortdesc' % DOAP_NS).text.splitlines())
        homepage = f'http://pypi.python.org/pypi/{package}/{version}'
        print(line % dict(
            name=package, homepage=homepage,
            description=description, version=version), file=out)
    print(file=out)


def packages(config, key):
    if not config.has_option('grok', key):
        print('Key "%s" not found in section [grok]' % key)
        return []
    result = config.get('grok', key).splitlines()
    result = filter(None, map(str.strip, result))
    return result


def write_package_list(path, version, use_trunk=False):
    location = GROKTOOLKIT_ROOT / ('tags/%s' % version)
    if use_trunk:
        location = GROKTOOLKIT_ROOT / 'trunk'

    print('Writing package list for Grok Toolkit "%s"' % version, location)

    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    fp = StringIO.StringIO((location / 'grok.cfg').read())
    config.readfp(fp)
    output = open(path, 'w')

    print(GENERATED_WARNING, file=output)

    heading = 'Grok %s packages' % version
    print('=' * len(heading), file=output)
    print(heading, file=output)
    print('=' * len(heading), file=output)

    print("\n", file=output)

    ztk_version = '1.1.4'
    print('Zope Toolkit %s' % ztk_version, file=output)
    print('------------------------------', file=output)
    print("""
This Grok released is based on Zope Toolkit {}.

`Overview <http://docs.zope.org/zopetoolkit/releases/overview-{}.html>`_ of
the ZTK. List of the ZTK `packages
<http://docs.zope.org/zopetoolkit/releases/packages-{}.html>`_
""".format(ztk_version, ztk_version, ztk_version), file=output)

    print('Packages', file=output)
    print('--------', file=output)
    included = packages(config, 'included')
    package_list(included, config, output)

    deprecating = packages(config, 'deprecating')
    if deprecating:
        print('Deprecating', file=output)
        print('-----------', file=output)
        package_list(deprecating, config.options('versions'), output)

    print('Other dependencies', file=output)
    print('------------------', file=output)
    all = config.options('versions')
    dependencies = (set(all) - set(included))  # - set(deprecating)
    package_list(dependencies, config, output)
    output.close()


if __name__ == '__main__':
    path = os.path.abspath(os.path.join('packages.rst'))
    dist = pkg_resources.get_distribution('groktoolkit')
    use_trunk = False
    if dist.precedence <= pkg_resources.DEVELOP_DIST:
        use_trunk = True
    write_package_list(path, dist.version, use_trunk=use_trunk)
