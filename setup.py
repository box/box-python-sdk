# coding: utf-8

from codecs import open   # pylint:disable=redefined-builtin
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
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
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
        # pylint:disable=import-outside-toplevel
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def main():
    base_dir = dirname(__file__)
    install_requires = [
        'attrs>=17.3.0',
        'requests>=2.4.3',
        'requests-toolbelt>=0.4.0, <1.0.0',
        'wrapt>=1.10.1'
    ]
    redis_requires = ['redis>=2.10.3']
    jwt_requires = ['pyjwt>=1.3.0', 'cryptography>=3, <3.5.0']
    extra_requires = {'jwt': jwt_requires, 'redis': redis_requires, 'all': jwt_requires + redis_requires}
    test_requires = [
        'bottle',
        'jsonpatch>1.14',
        'mock>=2.0.0, <4.0.0',
        'pycodestyle',
        'pylint',
        'sphinx',
        'sqlalchemy<1.4.0',
        'tox',
        'pytest>=2.8.3, <4.0.0',
        'pytest-cov',
        'pytest-xdist<1.28.0',
        'coveralls',
        'coverage',
        'tox-gh-actions',
        'pytz',
    ]
    extra_requires['test'] = test_requires
    with open('boxsdk/version.py', 'r', encoding='utf-8') as config_py:
        version = re.search(r'^\s+__version__\s*=\s*[\'"]([^\'"]*)[\'"]', config_py.read(), re.MULTILINE).group(1)
    setup(
        name='boxsdk',
        version=version,
        description='Official Box Python SDK',
        long_description=open(join(base_dir, 'README.rst'), encoding='utf-8').read(),  # pylint:disable=consider-using-with
        author='Box',
        author_email='oss@box.com',
        url='http://opensource.box.com',
        packages=find_packages(exclude=['demo', 'docs', 'test', 'test*', '*test', '*test*']),
        install_requires=install_requires,
        extras_require=extra_requires,
        tests_require=test_requires,
        cmdclass={'test': PyTest},
        classifiers=CLASSIFIERS,
        keywords='box oauth2 sdk',
        license='Apache Software License, Version 2.0, http://www.apache.org/licenses/LICENSE-2.0',
        package_data={'boxsdk': ['py.typed']},
    )


if __name__ == '__main__':
    main()
