import sys
import re
import os
import commands

HOST = 'grok.zope.org'
RELEASEINFOPATH = '/var/www/html/grok/releaseinfo'

def _upload_gtk_versions(packageroot, version):
    # Create the releaseinfo directory for this version.
    cmd = 'ssh %s "mkdir %s/%s"' % (HOST, RELEASEINFOPATH, version)
    print cmd + '\n'
    print commands.getoutput(cmd)
    # ``scp`` the file to the given destination.
    versions_filename = os.path.join(packageroot, 'grok.cfg')
    cmd = 'scp %s %s:%s/%s/versions.cfg' % (
        versions_filename, HOST, RELEASEINFOPATH, version)
    print cmd + '\n'
    print commands.getoutput(cmd)

def upload_entrypoint(data):
    if data['name'] != 'groktoolkit':
        # We're dealing with another package that somehow depends on
        # groktoolkit. Skip the step in that case.
        return
    packageroot = data['workingdir']
    version = data['version']
    _upload_gtk_versions(packageroot, version)

def upload_gtk_versions():
    packageroot = os.getcwd() # Ugh.
    version = sys.argv[1] # Ugh.
    _upload_gtk_versions(packageroot, version)
