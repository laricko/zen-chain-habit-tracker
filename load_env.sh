#!/usr/bin/env bash

# FOR ZSH USE: export $(grep -v '^#' "$1" | tr '\n' ' ')

export $(grep -v '^#' "$1" | xargs -d '\n')
