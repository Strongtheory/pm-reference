#!/usr/bin/bash
# ======================================================================================================================
# ======================================================================================================================
# This file contains a set of re-usable utility functions
# ----------------------------------------------------------------------------------------------------------------------
# Contents:
# * Utility functions
# * Standard functions
# * Git functions
# * AWS cli functions [TODO]
# * Azure CLI functions [TODO]
# * GCP CLI functions [TODO]
# ======================================================================================================================
# ======================================================================================================================
# function documentation format

# Note: Generally should be the following format:
# None
# [title] (type) Description

# Per input based format
# [1] (type) Description

# All input based format
# [*] (type) Description

# Description
# Globals:
#   None
#   [title] (type) Description
# Arguments:
#   None
#   [title] (type) Description
#   [1] (type) Description
#   [*] (type) Description
# Outputs:
#   None
#   <>

function tm() {
  :
}
# ======================================================================================================================
# ======================================================================================================================
# Standard Functions (Include Utility functions):

# Utility functions list:
# err
# mini_dash_line_console
# mini_dash_line_file
# equal_dash_line_console
# equal_dash_line_file

# Return types
# 0 - pass
# 1 - fail

# General Usage:
# return 0 (pass) [if <function_name> "${x}"; then]
# return 1 (fail) [if ! <function_name> "${x}"; then]

# Functions List:
# var_regular_exists
# var_array_exists
# local_file_exists
# local_directory_exists
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Implementation
# ----------------------------------------------------------------------------------------------------------------------
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

function var_regular_exists() {
  [[ -z "${1}" ]] && return 1

  return 0
}
# ----------------------------------------------------------------------------------------------------------------------
# Check if a variable name defined inside an array is null or not
# Globals:
#   None
#   [title] (type) Description
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