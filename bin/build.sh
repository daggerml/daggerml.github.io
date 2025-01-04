#!/bin/bash

# make a *temporary* directory
tmpdir=$(mktemp -d)
# trap to remove the directory when the script exits
trap "rm -rf $tmpdir" EXIT

# set daggerml environment variables
export DML_CONFIG_DIR=$tmpdir/daggerml-config
export DML_PROJECT_DIR=$tmpdir/daggerml-projects
export DML_REPO="test"

dml repo create $DML_REPO
dml project init $DML_REPO

sphinx-autobuild source/ build/