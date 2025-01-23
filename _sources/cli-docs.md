# CLI Documentation

## Global Options
- `--user`: Specify user name/host or email
- `--repo`: Select a specific repository
- `--query`: Apply a JMESPath query to filter response data
- `--project-dir`: Set project directory location (default: `.dml`)
- `--debug`: Enable debug output
- `--config-dir`: Set config directory location
- `--branch`: Select a specific branch
- `-h/--help`: Show help information
- `--version`: Show CLI version

## Commands

### `status`
Shows current repository, branch, and configuration details

### `ref` Subcommands
- `describe <type> <id>`: Get ref properties as JSON
- `dump <ref>`: Dump a ref and its dependencies to JSON
- `load <json>`: Load a previously dumped ref into the repository

### `repo` Subcommands
- `create <name>`: Create a new repository
- `delete <name>`: Delete a repository
- `copy <name>`: Copy current repository to a new name
- `list`: List all repositories
- `gc`: Delete unreachable objects in the repository

### `config` Subcommands
- `repo <repo>`: Select the repository to use
- `branch <name>`: Select the branch to use
- `user <user>`: Set user name/email

### `branch` Subcommands
- `create <name> [commit]`: Create a new branch, optionally from a specific commit
- `delete <name>`: Delete a branch
- `list`: List all branches
- `merge <branch>`: Merge another branch with the current one
- `rebase <branch>`: Rebase the current branch onto another one

### `dag` Subcommands
- `create <name> <message>`: Create a new DAG
 - `--dag-dump`: Optional import from a DAG dump
- `list`: List all DAGs
- `describe <id>`: Get DAG properties as JSON
- `html <id>`: Generate HTML page for a DAG
- `invoke <token> <json>`: Invoke API with token and JSON command body

### `index` Subcommands
- `list`: List all indexes
- `delete <id>`: Delete a specific index

### `commit` Subcommands
- `list`: List all commits
- `log`: Query commit log
 - `--graph`: Print commit graph
- `revert <commit>`: Revert a specific commit