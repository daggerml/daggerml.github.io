---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# How-To Guide

```{code-cell} python
:tags: [remove-input,remove-stdout,remove-stderr]

# import os
# from atexit import register
# from tempfile import TemporaryDirectory

# tmpd = TemporaryDirectory()
# register(tmpd.cleanup)

# os.environ["DML_CONFIG_DIR"] = f"{tmpd.name}/config"
# os.environ["DML_PROJECT_DIR"] = f"{tmpd.name}/project"
# os.mkdir(os.environ["DML_CONFIG_DIR"])
# os.mkdir(os.environ["DML_PROJECT_DIR"])

# import daggerml as dml
# dml.Api().init()

```

This guide will walk you through the most useful aspects of DaggerML,
including creating and managing DAGs, using the API, and running tests.

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
print(dag.api("repo", "list"))
```

```{code-cell} python
node2 = dag.put({"node0": node0, "node1": node1, "misc": [None, False]})
node3 = dag.put([node0, node1, node2])
node3.value()
```

Note that we passed both python objects and `dml.Node` objects to `dag.put`, and the result was the same (from a data perspective). The difference is, if you pass a `dml.Node` object, then we can add the corresponding edge in the dag (we can track that dependency).

### Accessing data

#### value

Getting the value (as you saw above):

```{code-cell} python
node3.value()
```

Note that it unrolls the whole thing and returns a python object all the way down.

#### collections

Collection nodes (like nodes 2 and 3) should be treated like the collections they are.

```{code-cell} python
print(dag.api("dag", "list"))
```

1. You can index into lists and maps and you get a node back. This means you can have much larger and deeper collections without loading them into memory, but more importantly, we can track the execution.

  ```{code-cell} python
  node2["node0"], node3[0]
  ```

  ```{code-cell} python
  print(dag.api("dag", "list"))
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
print(dag.api("dag", "list"))
```

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
print(dag.api("dag", "list"))
```

```{code-cell} python
# we don't care about the return value yet.
_ = dag.commit(node3)
print(dag.api("dag", "list"))
```

### Loading dag results

When we committed the dag above, we made that value importable by any other dag. We added that dag to the working tree, and now others can see it.

```{code-cell} python
dag = dml.new(name="dag_no_2", message="Second Dag")
node = dag.load("dag_no_1")
node.value()
```

### Function calling

```{code-cell} python

import daggerml.executor as dx

def foo(fndag):
  import torch
  n = fndag.expr[1].value()
  fndag.commit(torch.arange(n).tolist())

lx = dx.Local()
fn = lx.make_fn(dag, foo, 'conda', 'torch')
resp = lx.run(dag, fn, 5)
resp.get_result().value()
```

### Real data

In the real world we're dealing with datasets on s3, or behind some data layer abstraction like snowflake, hive, or some bespoke software optimized for your company's needs. We also deal with infrastructure that we spin up to test things. For these things daggerml has the concept of a `dml.Resource`. It's a datum type like `int`, `float`, `string`, etc., but it represents a unique opaque blob.

```{code-cell} python
rnode = dag.put(dml.Resource("my_ns:my_unique_id", data="asdf"))
resource = rnode.value()
resource
```

### Storing data

#### S3

```python3
s3 = dx.S3(BUCKET, PREFIX)
tarball = s3.tar(dag, ".")
```

#### Docker

```python
dkr = dx.Dkr()
img = dkr.build(dag, tarball, ['-f', 'tests/assets/Dockerfile'], s3).get_result()
```

### Calling a docker image as a function

```python
def add_one(fndag):
  _, *nums = fndag.expr.value()
  return dag.commit([x + 1 for x in nums])

# put the function on s3
script = s3.scriptify(dag, add_one)
fn_node = dkr.make_fn(dag, img, script).get_result()
result = dkr.run(dag, fn_node, 1, 2, 3, s3=s3).get_result()
result.value()
```

```sh
[2, 3, 4]
```

### Exceptions

To "fail" a dag, you just commit an instance of `dml.Error`. The value is then a node that raises an error when you try to get its value.

```{code-cell} python
dag = dml.new("failed-dag", "I'm doomed")
dag.commit(dml.Error("my unique error message"))
dag = dml.new("foopy", "gonna get an error")
node = dag.load("failed-dag")
try:
  node.value()
except dml.Error as e:
  print(e)
```

does it need more text?

```{code-cell} python

try:
  with dml.new("failed-dag2", "I'm doomed") as dag:
    dag.put(1/0)
except ZeroDivisionError:
  pass
dag = dml.new("foopy", "gonna get an error")
node = dag.load("failed-dag2")
try:
  node.value()
except dml.Error as e:
  print("error raised while getting node value...")
  print(e)
```

## Using the API Class

The [Api]{.title-ref} class provides methods to interact with the DAGs.
Here is an example of how to use the [Api]{.title-ref} class:

``` python
import daggerml as dml

with dml.Api(initialize=True) as api:
  dag = api.new_dag(name="example_dag", message="Example DAG creation")
```

## Loading and Dumping a DAG

You can load and dump a DAG using the [load]{.title-ref} and
[dump]{.title-ref} methods of the [Dag]{.title-ref} class:

``` python
from daggerml.core import Dag

# Load a DAG from a file
dag = Dag.load("path/to/dag_file")

# Dump the DAG to a file
dag.dump("path/to/dag_file")
```
