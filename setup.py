# coding: utf-8

from __future__ import unicode_literals

from os.path import dirname, join
import sys
from sys import version_info

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Operating System :: OS Independent',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


class PyTest(TestCommand):
    user_options = [(b'pytest-args=', b'a', b"Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Do the import here, once the eggs are loaded.
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def main():
    base_dir = dirname(__file__)
    install_requires = ['requests>=2.4.3', 'six>=1.4.0']
    if version_info < (3, 4):
        install_requires.append('enum34>=1.0.4')
    elif version_info < (2, 7):
        install_requires.append('ordereddict>=1.1')
    setup(
        name='boxsdk',
        version='1.0.2',
        description='Official Box Python SDK',
        long_description=open(join(base_dir, 'README.rst')).read(),
        author='Box',
        author_email='oss@box.com',
        url='http://opensource.box.com',
        packages=find_packages(exclude=['demo', 'docs', 'test']),
        install_requires=install_requires,
        tests_require=['pytest', 'pytest-xdist', 'mock', 'sqlalchemy', 'bottle', 'jsonpatch'],
        cmdclass={'test': PyTest},
        classifiers=CLASSIFIERS,
        keywords='box oauth2 sdk',
        license=open(join(base_dir, 'LICENSE')).read(),
    )


if __name__ == '__main__':
    main()
