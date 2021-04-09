#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"


# shellcheck disable=SC2086
exec $cmd
