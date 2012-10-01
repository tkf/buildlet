import multiprocessing

from .baseparallel import BaseParallelRunner


class MultiprocessingRunner(BaseParallelRunner):

    """
    Task runner class based on :class:`multiprocessing.Pool`.
    """

    def __init__(self, num_proc=2):
        self.num_proc = num_proc
        self.pool = multiprocessing.Pool(num_proc)

    def submit_tasks(self):
        self.cached_sorted_nodes = self.sorted_nodes()
        self.cached_predecessors = dict((n, self.graph.predecessors(n))
                                        for n in self.cached_sorted_nodes)
        self.results = {}
        self.submit_ready_tasks()

    def submit_ready_tasks(self):
        results = self.results
        for node in self.cached_sorted_nodes:
            predecessors = self.cached_predecessors[node]
            if node not in results and \
               all(p in results and results[p].ready() for p in predecessors):
                results[node] = self.pool.apply_async(
                    self.run_func, [self.nodetaskmap[node]])

    def wait_tasks(self):
        while True:
            for r in self.results.values():
                # This would raise an error if there is one in subprocesses
                r.get()
            if set(self.nodetaskmap) == set(self.results):
                break
            self.submit_ready_tasks()
