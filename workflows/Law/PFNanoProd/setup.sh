#!/usr/bin/env bash

action() {
    local shell_is_zsh="$( [ -z "${ZSH_VERSION}" ] && echo "false" || echo "true" )"
    local this_file="$( ${shell_is_zsh} && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    local this_dir="$( cd "$( dirname "${this_file}" )" && pwd )"


    #
    # global variables
    #

    export DPOA_DIR="${this_dir}"
    export DPOA_DATA_DIR="${DPOA_DIR}/data"
    export DPOA_SOFTWARE_DIR="${DPOA_DATA_DIR}/software"
    export DPOA_VENV_DIR="${DPOA_SOFTWARE_DIR}/venv"
    export DPOA_STORE_DIR="${DPOA_DATA_DIR}/store"

    export DPOA_SCHEDULER_HOST="127.0.0.1"
    export DPOA_SCHEDULER_PORT="8080"

    export VIRTUAL_ENV_DISABLE_PROMPT="1"
    export PYTHONWARNINGS="ignore"


    #
    # software setup
    #

    export DPOA_PYTHON_EXE="${DPOA_PYTHON_EXE:-python3}"
    export PATH="${DPOA_DIR}/bin:${PATH}"
    export PYTHONPATH="${DPOA_DIR}:${PYTHONPATH}"

    local venv_dir="${DPOA_VENV_DIR}/main"

    if [ ! -d "${venv_dir}" ]; then
        echo "installing software at ${venv_dir}"

        # create the venv
        eval "${DPOA_PYTHON_EXE} -m venv \"${venv_dir}\"" || return "$?"
        source "${venv_dir}/bin/activate" "" || return "$?"

        # install software
        pip install -U pip || return "$?"
        LAW_INSTALL_EXECUTABLE=python pip install git+https://github.com/riga/law.git --no-binary law || return "$?"
        pip install 'scinum~=1.4' || return "$?"
        pip install 'tabulate~=0.8' || return "$?"
        pip install 'PyYAML~=6.0' || return "$?"
    else
        # just activate it
        source "${venv_dir}/bin/activate" "" || return "$?"
    fi


    #
    # law setup
    #

    export LAW_HOME="${DPOA_DIR}/.law"
    export LAW_CONFIG_FILE="${DPOA_DIR}/law.cfg"

    # source law's bash completion scipt
    source "$( law completion )" ""

    # build the software cache
    law software

    # silently index
    law index -q
}
action "$@"
