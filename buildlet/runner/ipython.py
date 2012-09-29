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

from .simple import SimpleRunner


class IPythonParallelRunner(SimpleRunner):

    @classmethod
    def run_parent(cls, task):
        client = parallel.Client()
        view = client.load_balanced_view()
        (root, G, jobs) = cls.create_tree(task)
        results = cls.submit_jobs(view, G, jobs)
        view.wait(results.values())
        return results[root].get()

    @staticmethod
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

    @staticmethod
    def submit_jobs(cls, view, G, jobs):
        """Submit jobs via client where G describes dependencies."""
        results = {}
        for node in nx.topological_sort(G):
            deps = [results[n] for n in G.predecessors(node)]
            with view.temp_flags(after=deps):
                results[node] = view.apply_async(run_task, jobs[node])
        return results


def run_task(task):
    SimpleRunner.run(task)
    # TBD: Should I return task object?
    # return task
