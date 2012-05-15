import os
from setuptools import setup, find_packages

version = '1.5.4'

setup(
    name='groktoolkit',
    version=version,
    description='Grok: Now even cavemen can use Zope 3!',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    license='ZPL',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
        'zest.releaser',
        ],
    entry_points = {
        'zest.releaser.releaser.after': [
            'upload_ztk_versions=groktoolkit:upload_entrypoint',
            ],
        }
    )
