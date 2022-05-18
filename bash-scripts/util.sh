#!/usr/bin/bash
# ======================================================================================================================
# ======================================================================================================================
# General Usage:
# return 0 (pass) [if <function_name> "${x}"; then]
# return 1 (fail) [if ! <function_name> "${x}"; then]

# Return types
# 0 - pass
# 1 - fail
# ======================================================================================================================
# ======================================================================================================================
# Print a debug message with the current timestamp to the console
# Globals:
#   None
# Arguments:
#   [*] (string) message(s) to print to the console
# Outputs:
#   None

function err() {
  echo -e "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}
# ----------------------------------------------------------------------------------------------------------------------
# Print a mini-dash line to the console
# Globals:
#   None
# Arguments:
#   None
# Outputs:
#   None

function mini_dash_line_console() {
  echo "--------------------------------------------------------------------------------"
}
# ----------------------------------------------------------------------------------------------------------------------
# Print a mini-dash line to a file
# Globals:
#   None
# Arguments:
#   None
#   [1] (string) File name
# Outputs:
#   None

function mini_dash_line_file() {
  echo "--------------------------------------------------------------------------------" >>"${1}"
}
# ----------------------------------------------------------------------------------------------------------------------
# Print a equal-dash line to the console
# Globals:
#   None
# Arguments:
#   None
# Outputs:
#   None

function equal_dash_line_console() {
  echo "========================================================================================================================"
}
# ----------------------------------------------------------------------------------------------------------------------
# Print a equal-dash line to a file
# Globals:
#   None
# Arguments:
#   [1] (string) File name
# Outputs:
#   None

function equal_dash_line_file() {
  echo "========================================================================================================================" >>"${1}"
}
# ======================================================================================================================
# ======================================================================================================================
# Variable operations
# ----------------------------------------------------------------------------------------------------------------------
# Check if a regular variable is null or not
# Globals:
#   None
# Arguments:
#   None
#   [1] (string) Variable name
# Outputs:
#   0 - regular variable exists
#   1 - regular variable does not exist

function regular_var_exists() {
  [[ -z "${1}" ]] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a variable name defined inside an array is null or not
# Globals:
#   None
# Arguments:
#   [1] (string) Variable name
# Outputs:
#   0 - array variable exists
#   1 - array variable does not exist

function array_var_exists() {
  [[ -z "${!1}" ]] && return 1

  return 0
}
# ======================================================================================================================
# ======================================================================================================================
# Local data operations
# ----------------------------------------------------------------------------------------------------------------------
# Check if a file exists locally or not (relative from where this function is executed)
# Globals:
#   None
# Arguments:
#   [1] (string) File path and name
# Outputs:
#   0 - file does exist locally
#   1 - file does not exist locally

function local_file_exists() {
  [[ ! -f "${1}" ]] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a directory exists locally or not (relative from where this function is executed)
# Globals:
#   None
# Arguments:
#   [1] (string) Directory path and name
# Outputs:
#   0 - directory does exist locally
#   1 - directory does not exist locally


function local_directory_exists() {
  [[ ! -d "${1}" ]] && return 1

  return 0
}
# ======================================================================================================================
# ======================================================================================================================
# Git operations
# ----------------------------------------------------------------------------------------------------------------------
# Check if a branch exists remotely or not
# Note: Assumed to already be inside the repository folder
# Globals:
#   None
# Arguments:
#   [1] (string) remote branch name
# Outputs:
#   0 - remote branch exists
#   1 - remote branch does not exist

function remote_branch_exists_internal() {
  local ALLB
  ALLB=$(git branch -r)

  [ ! "$(echo "${ALLB}" | grep -o -c -w origin/"${1}")" -ge 1 ] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a branch exists remotely or not
# Note: Assumed to be outside the repository folder
# Globals:
#   None
# Arguments:
#   [1] (string) remote branch name
#   [1] (string) repository folder path
# Outputs:
#   0 - remote branch exists
#   1 - remote branch does not exist

function remote_branch_exists_external() {
  cd "${2}" || exit

  local ALLB
  ALLB=$(git branch -r)

  if [[ ! "$(echo "${ALLB}" | grep -o -c -w origin/"${1}")" -ge 1 ]]; then
    cd .. || exit
    return 1
  else
    cd .. || exit
    return 0
  fi
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a branch exists locally or not
# Note: Assumed to already be inside the repository folder
# Globals:
#   None
# Arguments:
#   [1] (string) local branch name
# Outputs:
#   0 - local branch exists
#   1 - local branch does not exist

function local_branch_exists_internal() {
  local ALLB
  ALLB=$(git branch -r)

  [ ! "$(echo "${ALLB}" | grep -o -c -w origin/"${1}")" -ge 1 ] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a branch exists locally or not
# Note: Assumed to be outside the repository folder
# Globals:
#   None
# Arguments:
#   [1] (string) local branch name
#   [1] (string) repository folder path
# Outputs:
#   0 - local branch exists
#   1 - local branch does not exist

function local_branch_exists_external() {
  cd "${2}" || exit

  local ALLB
  ALLB=$(git branch -r)

  if [[ ! "$(echo "${ALLB}" | grep -o -c -w origin/"${1}")" -ge 1 ]]; then
    cd .. || exit
    return 1
  else
    cd .. || exit
    return 0
  fi
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a branch exists locally or not
# Note: If no folder path [2] is passed in, it is assumed you are already in the repository folder
# Globals:
#   None
# Arguments:
#   None
#   [1] (string) local branch name
#   [2] (string) repository folder path referenced from the current location (optional)
# Outputs:
#   0 - local branch exists
#   1 - local branch does not exist

function remote_branch_exists() {
  if [[ ! -n "${1}" ]]; then  # variable does not exist
    export varReg="n"
  else  # variable does exist
    export varReg="y"
  fi

  # Check if the repository folder path was passed as an argument
  if [[ -n "${2}" ]]; then
    cd "${2}" || exit
  fi

  local ALLB
  ALLB=$(git branch -r)

  if [[ ! "$(echo "${ALLB}" | grep -o -c -w origin/"${1}")" -ge 1 ]]; then
    if [[ -n "${2}" ]]; then
      :
    fi
  else
    if [[ -n "${2}" ]]; then
      :
    fi
  fi

  [ ! "$(echo "${ALLB}" | grep -o -c -w origin/"${1}")" -ge 1 ] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a branch exists locally or not
# Note: If no folder path [2] is passed in, it is assumed you are already in the repository folder
# Globals:
#   None
# Arguments:
#   [1] (string) local branch name
#   [2] (string) repository folder path referenced from the current location (optional)
# Outputs:
#   0 - local branch exists
#   1 - local branch does not exist

function local_branch_exists() {
  local ALLB
  ALLB=$(git branch)

  [ ! "$(echo "${ALLB}" | grep -o -c -w "${1}")" -ge 1 ] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a tag exists
# Note: If no folder path [2] is passed in, it is assumed you are already in the repository folder
# Globals:
#   None
# Arguments:
#   [1] (string) tag name
# Outputs:
#   0 - check if tag exists
#   1 - check if the tag does not exist

function check_tag_exists() {
  local ALLT
  ALLT=$(git tag)

  if [ ! "$(echo "${ALLT}" | grep -o -c "${1}")" -ge 1 ]; then
    return 1
  else
    return 0
  fi
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if there are any differences in between the remote
# version in the current repository
# Note: If no folder path [1] is passed in, it is assumed you are already in the repository folder
# Globals:
#   None
# Arguments:
#   None
# Outputs:
#   0 - repository does not have any local changes
#   1 - repository does have local changes

function check_if_repo_difference_exists() {
  local check
  check=$(git status --porcelain | wc -l)

  [[ "${check}" -ne 0 ]] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------

# ======================================================================================================================
# ======================================================================================================================
