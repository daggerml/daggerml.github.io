# Example Usage

## Initializing and Basic Operations

```python
import daggerml as dml

# Create a new DAG
dag = dml.new('my_dag', 'example dag')
# Put simple values
node1 = dag.put([42])

# Access node properties
print(node1.value())  # [42]
print(node1.len().value())  # 1
print(node1.type().value())  # 'list'

# Indexing and slicing
first_item = node1[0]
print(first_item.value())  # 42

# Create complex structures
complex_node = dag.put({'x': node1, 'y': 'z'})

# Iterate and access items
for k, v in complex_node.items():
    print(k.value(), v.value())

# Commit the DAG
dag.commit(node1)
```

## Loading Previous DAGs

```python
d0 = dml.new('d0', 'd0')
d0.commit(42)

# Load value from previous DAG
d1 = dml.new('d1', 'd1')
loaded_node = d1.load('d0')
print(loaded_node.value())  # 42
```

## Asynchronous Function Handling

```python
from daggerml import Resource

# Assume ASYNC is a Resource representing an async function
dag = dml.new('async_dag', 'async example')
# Put async function
async_node = dag.put(ASYNC)

# Call with arguments and timeout
result = async_node(1, 2, 3, timeout=1000)
print(result.value())  # Function result
```

## Catching errors

```python
with dml.new('d0', '"failed" dag') as dag:
    # raises a ZeroDivision error
    print(1/0)
dag = dml.new('d1', 'user dag')
try:
    dag.load("d0")
except dml.Error as e:
    print(f"got error: {e}")
```


## Dml class

### Specifying global flags
Specify global args (like `repo`, `config_dir`, `user`, etc.) by passing them to the `Dml` constructor.

```python
dml_ = dml.Dml()
# run cli commands
status = dml_('status')

# Create a new DAG
dag = dml_.new('my_dag', 'example dag')
dag.commit(42)
```

### Temporary db
Create a temporary database and dml instance by using the `Dml` class as a context manager.

```python
with dml.Dml() as dml_:
   # Check current status
   status = dml_('status')

   # Create a new DAG
   dag = dml_.new('my_dag', 'example dag')
   dag.commit(42)
```