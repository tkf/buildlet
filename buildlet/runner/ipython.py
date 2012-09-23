"""
Task runner using IPython parallel interface.

See `The IPython task interface`_ and `IPython Documentation`_
in `IPython Documentation`_.

.. _The IPython task interface:
   http://ipython.org/ipython-doc/dev/parallel/parallel_task.html

.. _DAG Dependencies:
   http://ipython.org/ipython-doc/dev/parallel/dag_dependencies.html

.. _IPython Documentation:
   http://ipython.org/ipython-doc/dev/

"""

import itertools

import networkx as nx
from IPython import parallel


def run(task):
    task.pre_run()
    try:
        if task.is_finished():
            task.load()
        else:
            run_parallel(task)
    finally:
        task.post_run()


def run_parallel(task):
    client = parallel.Client()
    view = client.load_balanced_view()
    (root, G, jobs) = create_tree(task)
    results = submit_jobs(view, G, jobs)
    view.wait(results.values())
    return results[root].get()


def create_tree(task):
    G = nx.DiGraph()
    jobs = {}
    counter = itertools.count()

    def creator(i, t):
        jobs[i] = t
        for p in t.get_parents():
            k = counter()
            G.add_node(k)
            G.add_edge(i, k)
            creator(k, p)

    root = counter()
    creator(counter(), task)
    return (root, G, jobs)


def run_task(task):
    task.run()
    # TBD: Should I return task object?
    # return task


def submit_jobs(view, G, jobs):
    """Submit jobs via client where G describes dependencies."""
    results = {}
    for node in nx.topological_sort(G):
        deps = [results[n] for n in G.predecessors(node)]
        with view.temp_flags(after=deps):
            results[node] = view.apply_async(run_task, jobs[node])
    return results
