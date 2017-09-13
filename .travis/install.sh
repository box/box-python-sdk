#!/bin/bash

# Originally from
# <https://github.com/pyca/cryptography/blob/d93aa99636b06d5d403130425098b2f0cc1b516e/.travis/install.sh>.

set -e
set -x
set -o pipefail

git clean -f -d -X
rm -r -f $PWD/.pyenv  # Apparently `git-clean` won't remove other repositories.

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew install pyenv
    brew outdated pyenv || brew upgrade pyenv

    if which -s pyenv; then
        rm -r -f $HOME/.pyenv
        eval "$(pyenv init -)"
    fi

    case "${TOX_ENV}" in
        py26)
            curl -O https://bootstrap.pypa.io/get-pip.py
            python get-pip.py --user
            ;;
        py27)
            curl -O https://bootstrap.pypa.io/get-pip.py
            python get-pip.py --user
            ;;
        py33)
            pyenv install 3.3.6
            pyenv global 3.3.6
            ;;
        py34)
            pyenv install 3.4.2
            pyenv global 3.4.2
            ;;
        py35)
            pyenv install 3.5.0
            pyenv global 3.5.0
            ;;
        py36)
            pyenv install 3.6.0
            pyenv global 3.6.0
            ;;
        pypy)
            pyenv install "pypy${PYPY_VERSION}"
            pyenv global "pypy${PYPY_VERSION}"
            ;;
    esac
    pyenv rehash
    python -m pip install -U --user virtualenv
else
    # pyenv installation to get specified pypy version (Travis may only have older version(s))
    if [[ "${TOX_ENV}" == "pypy" ]]; then
        git clone https://github.com/yyuu/pyenv.git $PWD/.pyenv
        export PYENV_ROOT="$PWD/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init -)"
        pyenv install "pypy${PYPY_VERSION}"
        pyenv global "pypy${PYPY_VERSION}"
    fi
    pip install -U virtualenv
fi

python -m virtualenv $PWD/.venv
source $PWD/.venv/bin/activate
pip install -U tox
