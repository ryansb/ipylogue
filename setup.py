#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Can't import to get the version because we won't have dependencies.
requires = []

with open('requirements.txt', 'r') as reqs:
    requires = reqs.read().splitlines()

setup(name='pitted',
      version=u'0.1.0',
      description='Back up IPython notebooks with git',
      long_description=open('README.md').read(),
      author='Ryan Brown',
      author_email='sb@ryansb.com',
      url='http://github.com/ryansb/pitted',
      packages=['pitted'],
      package_data={'': ['COPYING.txt']},
      include_package_data=False,
      install_requires=requires,
      license=open('COPYING.txt').read(),
      zip_safe=False,
      classifiers=(
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Framework :: IPython',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
      ),
      )
