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
trap "rm -rf $tmpdir" EXIT

export DML_CONFIG_DIR=$tmpdir/daggerml-config
export DML_PROJECT_DIR=$tmpdir/daggerml-projects
export DML_REPO="test"

dml repo create $DML_REPO
dml project init $DML_REPO

if [ "$watch" = true ]; then
  # watch for changes and rebuild -- useful for local development
  sphinx-autobuild source/ build/
else
  sphinx-build -b html source build
fi