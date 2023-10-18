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
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
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
        'urllib3',
        'requests>=2.4.3,<3',
        'requests-toolbelt>=0.4.0',
        'python-dateutil',  # To be removed after dropping Python 3.6
    ]
    redis_requires = ['redis>=2.10.3']
    jwt_requires = ['pyjwt>=1.7.0', 'cryptography>=3']
    coveralls_requires = ['coveralls']
    dev_requires = ['tox<=3.28.0']
    gh_requires = ['tox-gh-actions']
    test_requires = [
        'bottle',
        'jsonpatch>1.14',
        'sqlalchemy<1.4.0',
        'pytest',
        'pytest-timeout',
        'pytest-cov',
        'pytest-lazy-fixture',
        'pytz',
        'urllib3<2'
    ]
    extra_requires = {
        'jwt': jwt_requires,
        'redis': redis_requires,
        'coveralls': coveralls_requires + dev_requires,
        'dev': dev_requires,
        'gh': gh_requires + dev_requires,
        'test': test_requires,
    }
    with open('boxsdk/version.py', encoding='utf-8') as config_py:
        version = re.search(r'^\s*__version__\s*=\s*[\'"]([^\'"]*)[\'"]', config_py.read(), re.MULTILINE).group(1)
    setup(
        name='boxsdk',
        version=version,
        description='Official Box Python SDK',
        long_description_content_type="text/markdown",
        long_description=open(join(base_dir, 'README.md'), encoding='utf-8').read(),  # pylint:disable=consider-using-with
        author='Box',
        author_email='oss@box.com',
        url='https://github.com/box/box-python-sdk',
        project_urls={
            'Changelog': 'https://github.com/box/box-python-sdk/blob/main/CHANGELOG.md',
        },
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
