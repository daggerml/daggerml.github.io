---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  execution_mode: auto
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# How-To Guide

This guide will walk you through the most useful aspects of DaggerML,
including creating and managing DAGs, using the API, and running tests.

## Install

In a virtual environment, install `daggerml-cli`.

```sh
pip install daggerml-cli
```

In the desired environment, install `daggerml`

```sh
pip install daggerml
```

## Initialize

```sh
dml config user testi@testico
dml repo create my-repo
dml config repo my-repo
dml config branch main
dml status
```

### CLI Usage

```sh
dml --help
dml COMMAND --help
dml COMMAND SUBCOMMAND --help
```

> [!TIP]
> Shell completion is available for bash/zsh via [argcomplete](https://github.com/kislyuk/argcomplete).

## Basic Usage

### Create a dag

```{code-cell} python
import daggerml as dml

print(f"{dml.__version__ = }")
dag = dml.new(name="dag_no_1", message="Example DAG creation")
```

### Adding data to our dag

We want to track some data flow, so let's start with the simplest case possible: literals.

We can add a literal with `dag.put`, and get the value back with `node.value()`.

```{code-cell} python
node0 = dag.put(3)
node1 = dag.put("example")
node0.value(), node1.value()
```

daggerml has native support for collections like lists, sets, and maps (dictionaries).

```{code-cell} python
node2 = dag.put({"node0": node0, "node1": node1, "misc": [None, False]})
node3 = dag.put([node0, node1, node2])
node3.value()
```

```{code-cell} python
node3[1:]
```

Note that we passed both python objects and `dml.Node` objects to `dag.put`, and the result was the same (from a data perspective). The difference is, if you pass a `dml.Node` object, then we can add the corresponding edge in the dag (we can track that dependency).

### Accessing data

#### value

Getting the value (as you saw above):

```{code-cell} python
node3.value()
```

```{note}
Calling `dml.Node.value()` on a collection unrolls the data recursively
returning only python datastructures and `dml.Resources`.
```

#### collections

Collection nodes (like nodes 2 and 3) should be treated like the collections they are.

```{tip}
Collection elements should be accessed via the methods described here when feasible.
```

1. You can index into lists and maps and you get a node back.

  ```{code-cell} python
  node2["node0"], node3[0]
  ```

2. You can also get the keys of a dictionary (as a node):

  ```{code-cell} python
  node2.keys().value()
  ```

3. You can get the length of any collection:

```{code-cell} python
node2.len().value(), node3.len().value()
```

4. Use them as iterators:

```{code-cell} python
[node.value() for node in node2]
```

```{code-cell} python
[node.value() for node in node3]
```

5. You can call `.items` for dictionaries.

A key thing to keep in mind is that when you index, you get a different node than the one you put in (but with the same underlying value). For example,

```{code-cell} python
node0 = dag.put(1)
node1 = dag.put([node0])
```

We see that `node1` is just the list containing `node0`, so the values of `node0` and `node1[0]` should be the same. But the node IDs are not.

```{code-cell} python
node0, node1[0]
```

### Committing results

Now that we have some stuff, we might want to commit. So let's say this dag was just to create this collection. Let's commit it.

```{code-cell} python
# we don't care about the return value yet.
_ = dag.commit(node3)
print(dag.dml("dag", "list"))
```

### Loading dag results

When we committed the dag above, we made that value importable by any other dag. We added that dag to the working tree, and now others can see it.

```{code-cell} python
dag = dml.new(name="dag_no_2", message="Second Dag")
node = dag.load("dag_no_1")
node.value()
```

### Real data

In the real world we're dealing with datasets on s3, or behind some data layer abstraction like snowflake, hive, or some bespoke software optimized for your company's needs. We also deal with infrastructure that we spin up to test things. For these things daggerml has the concept of a `dml.Resource`. It's a datum type like `int`, `float`, `string`, etc., but it represents a unique opaque blob.

```{code-cell} python
rnode = dag.put(dml.Resource("my_ns:my_unique_id", data="asdf"))
resource = rnode.value()
resource
```

### Exceptions

To "fail" a dag, you just commit an instance of `dml.Error`. The value is then a node that raises an error when you try to get its value.

```{code-cell} python
dag = dml.new("failed-dag", "I'm doomed")
dag.commit(dml.Error("my unique error message"))
```

When we go to access it:

```{code-cell} python
---
tags: [raises-exception]
---

dag = dml.new("foopy", "gonna get an error")
node = dag.load("failed-dag")
node.value()
```

### Dags as context managers

```{tip}
You can use a dag as a context manager to fail dags when an exception is thrown.
```

```{code-cell} python
---
tags: [raises-exception]
---

with dml.new("failed-dag2", "I'm doomed") as dag:
  dag.put(1/0)
```

The error was re-raised, but the dag still failed.

```{code-cell} python
---
tags: [raises-exception]
---

dag = dml.new("foopy", "gonna get an error")
node = dag.load("failed-dag2")
node.value()
```

And we can see that the context manager kept the stack trace, which means now that stacktrace is stored in daggerml.

## Using the API Class

The [Api][api] class provides methods to interact with the DAGs.
Here is an example of how to use the [Api]{.title-ref} class:

```{code-cell} python
with dml.Dml() as api:
  dag = api.new(name="example_dag", message="Example DAG creation")
```

```{code-cell} python
import json

with dml.Dml() as api:
  print(json.dumps(api("status"), indent=2))
```
