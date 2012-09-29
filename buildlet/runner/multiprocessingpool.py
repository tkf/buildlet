"""
Task runner based on :class:`multiprocessing.Pool`.
"""

import multiprocessing

from .simple import SimpleRunner
from .mixinparallel import MixInParallelRunner


class MultiprocessingRunner(MixInParallelRunner, SimpleRunner):

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
            if all(p in results and results[p].ready() for p in predecessors):
                self.pool.apply_async(self.run_func, self.nodetaskmap[node],
                                      callback=self.submit_ready_tasks)
                # Otherwise, there are unfinished tasks. this will be
                # called when all the unfinished tasks are finished.

    def wait_tasks(self):
        while True:
            for r in self.results.values():
                r.wait()
            if set(self.nodetaskmap) == set(self.results):
                break
