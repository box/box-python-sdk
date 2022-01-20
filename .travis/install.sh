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
        eval "$(pyenv init --path)"
    fi

    case "${TOX_ENV}" in
        py36)
            pyenv install 3.6.0
            pyenv global 3.6.0
            ;;
        py37)
            pyenv install 3.7.0
            pyenv global 3.7.0
            ;;
        pypy)
            pyenv install "pypy${PYPY_VERSION}"
            pyenv global "pypy${PYPY_VERSION}"
            ;;

    esac
    pyenv rehash
    python -m pip install -U --user virtualenv
    python -m virtualenv $PWD/.venv
else
    # pyenv installation to get specified pypy version (Travis may only have older version(s))
    if [[ "${TOX_ENV}" == "pypy" ]]; then
        git clone https://github.com/yyuu/pyenv.git $PWD/.pyenv
        export PYENV_ROOT="$PWD/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init --path)"
        pyenv install "pypy${PYPY_VERSION}"
        pyenv global "pypy${PYPY_VERSION}"
        pip install -U virtualenv
        pip install --upgrade pip
        python -m venv $PWD/.venv
    else
        python -m virtualenv $PWD/.venv
    fi
fi

source $PWD/.venv/bin/activate
pip install -U tox
