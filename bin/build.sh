#!/bin/bash

watch=false
while getopts "w" opt; do
  case $opt in
    w)
      watch=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

tmpdir=$(mktemp -d)
trap "rm -rf $tmpdir" EXIT INT TERM HUP

echo "Temporary directory created at $tmpdir"
export DML_CONFIG_DIR=$tmpdir/config
export DML_PROJECT_DIR=$tmpdir/projects
export DML_CACHE_PATH=$tmpdir/cachedb

export DML_S3_BUCKET=does-not-exist
export DML_S3_PREFIX=does-not-exist

dml config user testi@testico
dml repo create test
dml config repo test
dml config branch main
dml cache create
dml status


# # cat <<EOT | python3 > source/python-lib-readme.md
# # from importlib.metadata import metadata
# # lib_metadata = metadata('daggerml')
# # print(lib_metadata['Description'])
# # EOT

# # cat <<EOT | python3 > source/daggerml-cli-readme.md
# # from importlib.metadata import metadata
# # lib_metadata = metadata('daggerml-cli')
# # print(lib_metadata['Description'])
# # EOT

if [ "$watch" = true ]; then
  # watch for changes and rebuild -- useful for local development
  sphinx-autobuild source/ build/
else
  sphinx-build -b html source build
fi