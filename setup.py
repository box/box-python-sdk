# coding: utf-8

from __future__ import unicode_literals

from codecs import open   # pylint:disable=redefined-builtin
from collections import defaultdict
from os.path import dirname, join
import re
import sys

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
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Operating System :: OS Independent',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


class PyTest(TestCommand):
    # pylint:disable=attribute-defined-outside-init

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
    install_requires = ['requests>=2.4.3', 'six>=1.4.0', 'requests-toolbelt>=0.4.0']
    redis_requires = ['redis>=2.10.3']
    jwt_requires = ['pyjwt>=1.3.0', 'cryptography>=0.9.2']
    extra_requires = defaultdict(list)
    extra_requires.update({'jwt': jwt_requires, 'redis': redis_requires, 'all': jwt_requires + redis_requires})
    conditional_dependencies = {
        # Newer versions of pip and wheel, which support PEP 426, allow
        # environment markers for conditional dependencies to use operators
        # such as `<` and `<=` [1]. However, older versions of pip and wheel
        # only support PEP 345, which only allows operators `==` and `in` (and
        # their negations) along with string constants [2]. To get the widest
        # range of support, we'll only use the `==` operator, which means
        # explicitly listing all supported Python versions that need the extra
        # dependencies.
        #
        # [1] <https://www.python.org/dev/peps/pep-0426/#environment-markers>
        # [2] <https://www.python.org/dev/peps/pep-0345/#environment-markers>
        'enum34>=1.0.4': ['2.6', '2.7', '3.3'],   # <'3.4'
        'ordereddict>=1.1': ['2.6'],   # <'2.7'
    }
    for requirement, python_versions in conditional_dependencies.items():
        for python_version in python_versions:
            # <https://wheel.readthedocs.org/en/latest/#defining-conditional-dependencies>
            python_conditional = 'python_version=="{0}"'.format(python_version)
            key = ':{0}'.format(python_conditional)
            extra_requires[key].append(requirement)
    with open('boxsdk/version.py', 'r', encoding='utf-8') as config_py:
        version = re.search(r'^\s+__version__\s*=\s*[\'"]([^\'"]*)[\'"]', config_py.read(), re.MULTILINE).group(1)
    setup(
        name='boxsdk',
        version=version,
        description='Official Box Python SDK',
        long_description=open(join(base_dir, 'README.rst'), encoding='utf-8').read(),
        author='Box',
        author_email='oss@box.com',
        url='http://opensource.box.com',
        packages=find_packages(exclude=['demo', 'docs', 'test', 'test*', '*test', '*test*']),
        install_requires=install_requires,
        extras_require=extra_requires,
        tests_require=['pytest', 'pytest-xdist', 'mock', 'sqlalchemy', 'bottle', 'jsonpatch'],
        cmdclass={'test': PyTest},
        classifiers=CLASSIFIERS,
        keywords='box oauth2 sdk',
        license='Apache Software License, Version 2.0, http://www.apache.org/licenses/LICENSE-2.0',
    )


if __name__ == '__main__':
    main()
