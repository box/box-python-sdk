from setuptools import setup, find_packages

from os.path import dirname, join

import re


def main():
    install_requires = ['requests', 'requests-toolbelt']
    tests_require = ['pytest', 'pytest-timeout', 'pytest-cov', 'pytest-rerunfailures']
    dev_requires = ['tox']
    jwt_requires = ['pyjwt>=1.7.0', 'cryptography>=3']
    version_file = open(join(dirname(__file__), 'box_sdk_gen/networking/version.py'))
    version_regex = re.compile('.*__version__ = \'(.*?)\'', re.S)
    version_string_grouped = version_regex.match(version_file.read())
    __version__ = version_string_grouped.group(1)
    extras_require = {
        'test': tests_require + jwt_requires,
        'dev': dev_requires,
        'jwt': jwt_requires,
    }
    setup(
        name='box-sdk-gen',
        version=__version__,
        description='Official Box Python Generated SDK',
        url='https://github.com/box/box-python-sdk-gen.git',
        licence='Apache-2.0, http://www.apache.org/licenses/LICENSE-2.0',
        author='Box',
        long_description_content_type='text/markdown',
        long_description=open(
            join(dirname(__file__), 'README.md'), encoding='utf-8'
        ).read(),
        author_email='oss@box.com',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Operating System :: OS Independent',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: MacOS :: MacOS X',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        keywords='box, sdk, api, rest, boxsdk, box-sdk-gen',
        install_requires=install_requires,
        tests_require=tests_require,
        extras_require=extras_require,
        packages=find_packages(exclude=['docs', '*test*']),
    )


if __name__ == '__main__':
    main()
