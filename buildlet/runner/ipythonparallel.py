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

import IPython.parallel

from .simple import SimpleRunner
from .mixinparallel import MixInParallelRunner


class IPythonParallelRunner(MixInParallelRunner, SimpleRunner):

    def submit_tasks(self):
        self.client = IPython.parallel.Client()
        self.view = view = self.client.load_balanced_view()
        self.results = results = {}
        for node in self.sorted_nodes():
            deps = [results[n] for n in self.graph.predecessors(node)]
            with view.temp_flags(after=deps):
                results[node] = view.apply_async(self.run_func,
                                                 self.nodetaskmap[node])

    def wait_tasks(self):
        self.view.wait(self.results.values())
