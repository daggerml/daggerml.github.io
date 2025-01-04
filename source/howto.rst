.. _howto:

============
How-To Guide
============

This guide will walk you through the most useful aspects of DaggerML, including creating and managing DAGs, using the API, and running tests.

Basic Usage
===========

The Basics
----------

Let's go over some of the basic operations on dags. Once a dag is created, you
can add nodes as leaves (literal nodes) and commit values. The nodes you add can
be collections of values or of other nodes.

Creating a DAG
~~~~~~~~~~~~~~

.. code-block:: python

    import daggerml as dml

    # Create a new DAG
    dag = dml.new(name="example_dag", message="Example DAG creation")

    # Add nodes to the DAG
    node0 = dag.put(3)
    node1 = dag.put("example")
    node2 = dag.put({node0, node1})
    node3 = dag.put({"node0": node0.value(), "node1": node1, "node2": node2})
    node4 = dag.put([node2, node3])
    assert node4.value() == [node2.value(), node3.value()]
    # Commit the DAG
    dag.commit(node3)

DaggerML is a Python library that provides a simple interface for creating and
managing Directed Acyclic Graphs (DAGs). A DAG is a collection of nodes that are
connected by edges, where each edge represents a dependency between two nodes.
The library provides a set of classes and methods that allow you to create,
manipulate, and visualize DAGs.

To create a new DAG, you can use the `Dag` class from the `daggerml.core` module. Here is an example:

.. code-block:: python

    import daggerml as dml

    # Create a new DAG
    dag = dml.new(name="example_dag", message="Example DAG creation")

    # Add nodes to the DAG
    node1 = dag.put(3)
    node2 = dag.put("example")
    node3 = dag.put([node1, node2])

    # Commit the DAG
    dag.commit(node3)

Creating a DAG
--------------

To create a new DAG, you can use the `Dag` class from the `daggerml.core` module. Here is an example:

.. code-block:: python

    import daggerml as dml

    # Create a new DAG
    dag = dml.new(name="example_dag", message="Example DAG creation")

    # Add nodes to the DAG
    node1 = dag.put(3)
    node2 = dag.put("example")
    node3 = dag.put([node1, node2])

    # Commit the DAG
    dag.commit(node3)

Using the API Class
-------------------

The `Api` class provides methods to interact with the DAGs. Here is an example of how to use the `Api` class:

.. code-block:: python

    import daggerml as dml

    # Create an API instance
    api = dml.Api(config_dir="path/to/config/directory")

    # Create a new DAG using the API
    dag = api.new_dag(name="example_dag", message="Example DAG creation")

    # Add nodes to the DAG
    node1 = dag.put(3)
    node2 = dag.put("example")
    node3 = dag.put([node1, node2])

    # Commit the DAG
    dag.commit(node3)

Loading and Dumping a DAG
-------------------------

You can load and dump a DAG using the `load` and `dump` methods of the `Dag` class:

.. code-block:: python

    from daggerml.core import Dag

    # Load a DAG from a file
    dag = Dag.load("path/to/dag_file")

    # Dump the DAG to a file
    dag.dump("path/to/dag_file")

Advanced Usage
==============

Dealing with the API
--------------------

The `Api` class wraps the core functionality of DaggerML (`daggerml-cli`) in a
python interface. You can speficy the repo when instantiating the `Api` class,
use the default repo, or create and initialize a temporary repo.

Standard Usage
~~~~~~~~~~~~~~

To use the default repo, you can create an instance of the `Api` class without
specifying a repo. Here is an example:

.. code-block:: python

    import daggerml as dml

    # Create an API instance
    api = dml.Api()
    # Create a new DAG using the API
    dag = api.new_dag(name="example_dag", message="Example DAG creation")

Using a Temporary Repo
~~~~~~~~~~~~~~~~~~~~~~

To use a temporary repo, you can create an instance of the `Api` class without
specifying a repo and specifying `initialize=True`. Here is an example:

.. code-block:: python
    
    import daggerml as dml

    # Create an API instance with a temporary repo
    api = dml.Api(initialize=True)
    # do whatever you want with the API
    api.cleanup()

You can also use the `Api` class as a context manager to automatically clean up
the temporary repo:

.. code-block:: python

    import daggerml as dml

    with dml.Api(initialize=True) as api:
        # do whatever you want with the API
        pass

Using a Specific Repo
~~~~~~~~~~~~~~~~~~~~~

To use a specific repo, you can create an instance of the `Api` class and specify
the repo path. Here is an example:

.. code-block:: python

    import daggerml as dml

    # Create an API instance with a specific repo
    api = dml.Api(config_dir="path/to/config/directory")
    # Create a new DAG using the API
    dag = api.new_dag(name="example_dag", message="Example DAG creation")

Conclusion
----------

This guide provided an overview of the most useful aspects of DaggerML, including creating and managing DAGs, using the API, and running tests. For more detailed information, refer to the API documentation and the test suite.