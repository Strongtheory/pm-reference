#!/usr/bin/bash
# ======================================================================================================================
# ======================================================================================================================
# Functions List:
# err
# mini_dash_line_console
# mini_dash_line_file
# equal_dash_line_console
# equal_dash_line_file

# var_regular_exists
# var_array_exists
# local_file_exists
# local_directory_exists

# branch_remote_exists
# branch_local_exists
# check_tag_exists
# check_if_repository_difference_exists
# check_if_specific_file_difference_exists
# check_if_it_is_a_repository

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
# Check if a regular variable is null or not
# Globals:
#   None
# Arguments:
#   None
#   [1] (string) Variable name
# Outputs:
#   0 - regular variable exists
#   1 - regular variable does not exist

function var_regular_exists() {
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

function var_array_exists() {
  [[ -z "${!1}" ]] && return 1

  return 0
}
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
# Check if a branch exists locally or not
# Globals:
#   None
# Arguments:
#   None
#   [1] (string) local branch name
# Outputs:
#   0 - local branch exists
#   1 - local branch does not exist

function branch_remote_exists() {
  local ALLB
  ALLB=$(git branch -r)

  [ ! "$(echo "${ALLB}" | grep -o -c -w origin/"${1}")" -ge 1 ] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a branch exists remotely or not
# Globals:
#   None
# Arguments:
#   [1] (string) remote branch name
# Outputs:
#   0 - remote branch exists
#   1 - remote branch does not exist

function branch_local_exists() {
  local ALLB
  ALLB=$(git branch)

  [ ! "$(echo "${ALLB}" | grep -o -c -w "${1}")" -ge 1 ] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a tag exists
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
# (Must already be in the repository folder for this to work)
# Globals:
#   None
# Arguments:
#   None
# Outputs:
#   0 - repository does not have any local changes
#   1 - repository does have local changes

function check_if_repository_difference_exists() {
  local check
  check=$(git status --porcelain | wc -l)

  [[ "${check}" -ne 0 ]] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if there are any differences in between the remote
# version in the current repository for a specific file
# (Must already be in the repository folder for this to work)
# Globals:
#   None
# Arguments:
#   [1] (string) file name
# Outputs:
#   0 - specific file does not have any local changes
#   1 - specific file does have local changes

function check_if_specific_file_difference_exists() {
  if ! local_file_exists "${1}"; then
    return 1
  fi

  local check
  check=$(git diff --exit-code "${1}" | wc -l)

  [[ "${check}" -ne 0 ]] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if the current directory is a valid git repository
# (If not target directory is provided, it check the current directory by default)
# Globals:
#   None
# Arguments:
#   [1] (string, optional) target directory
# Outputs:
#   0 - current or target directory is a valid repository
#   1 - current or target directory is not valid repository

function check_if_it_is_a_repository() {
  local check

  if var_regular_exists "${1}"; then
    cd "${1}" || exit
    check=$(git rev-parse --git-dir > /dev/null 2>&1)

    if [[ "${check}" -ne 0 ]]; then
      cd .. || exit
      return 1
    else
      cd .. || exit
      return 0
    fi
  fi

  check=$(git rev-parse --git-dir > /dev/null 2>&1)

  [[ "${check}" -ne 0 ]] && return 1

  return 0
}
# ======================================================================================================================
# ======================================================================================================================
