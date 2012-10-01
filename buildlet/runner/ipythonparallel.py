import IPython.parallel

from .baseparallel import BaseParallelRunner


class IPythonParallelRunner(BaseParallelRunner):

    """
    Task runner class using IPython parallel interface.

    See `The IPython task interface`_ and `DAG Dependencies`_
    in `IPython Documentation`_.

    .. _The IPython task interface:
       http://ipython.org/ipython-doc/dev/parallel/parallel_task.html

    .. _DAG Dependencies:
       http://ipython.org/ipython-doc/dev/parallel/dag_dependencies.html

    .. _IPython Documentation:
       http://ipython.org/ipython-doc/dev/

    """

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
        for r in self.results.values():
            r.get()
