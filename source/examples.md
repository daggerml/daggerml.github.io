# Example Usage

## Initializing and Basic Operations

Firstly, `dml_util` expects both `DML_S3_BUCKET` and `DML_S3_PREFIX` to be set. This is where we'll store data. For this example, we set it to random nonsense (we won't be using s3 here).

```{code-cell} python
from contextlib import redirect_stderr, redirect_stdout

from daggerml import  Dml, Error
from dml_util import funkify

# Create a dml instance
dml = Dml()
```

```{code-cell} python
# Create a new DAG
dag = dml.new('my_dag', 'example dag')
# Put simple values
node1 = dag._put(list(range(5)))
# you can always get the value of a node
node1.value()
```

Because our node is a list, we can do list stuff with it...

```{code-cell} python
# Indexing and slicing
print(f"{node1[0] = } -- {node1[0].value()}")

# Create complex structures
complex_node = dag._put({'x': node1, 'y': 'z'})

# Iterate and access items
for k, v in complex_node.items():
    print(f"{k = !s}, {v = } -- {v.value() = !r}")

# Commit the DAG
dag.result = complex_node
```

## Calling functions

Let's define a function that takes $n\ge 2$ arguments, sums up all but the last, and then divides by the last.

```{code-cell} python
@funkify
def my_funk(dag):
    numer = sum(dag.argv[1:-1].value())
    return numer / dag.argv[-1].value()

dag = dml.new('funk-dag', 'dag to build a funk')
dag.my_funk = my_funk
with redirect_stdout(None), redirect_stderr(None):
    result = dag.my_funk(*range(5))
print(f"{result = } -- {result.value() = }")
```

And we can save this as our dag's "result" and then import it later without having to consider the infrastructure it's running on, or anything else.

```{code-cell} python
dag.result = dag.my_funk

try:
    with dml.new("new-dag", "my cool new dag that will unforunately fail") as dag:
        dag.funk = dml.load("funk-dag").result
        with redirect_stdout(None), redirect_stderr(None):
            dag.funk(1, 2, 3, 4, 0, name="bad-guy")  # note we're dividing by zero!
except Error as e:
    print("ruh roh! We divided by zero...")
    print(e)
```

And because we used the dag as a context manager, that error is stored as the dag's result, and we can query it later.

```{code-cell} python
print(dml("dag", "describe", "new-dag")["error"])
```

Or in another dag:

```{code-cell} python
dag = dml.new("newest")
try:
    dml.load("new-dag")["bad-guy"].value()
except Error as e:
    print("reraised?", "ZeroDivisionError" in str(e))
```

This `funkify` decorator can be used to send your code into the cloud, or have a function run in a different environment, or do whatever you want.

For more, read the examples on the `daggerml` and `dml-util` repos.