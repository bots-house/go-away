#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

for script in ./sql/up_*.sql; do
  echo "applying ${script}"
  # {executable} {db_dsn} {sql_script} {retry_times} {timeout}
  ./sql/up-db.py "${DB_DSN}" "${script}" 5 3
done


# shellcheck disable=SC2086
exec $cmd
