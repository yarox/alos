from __future__ import division
from utils import weighted_choice


class AntLike(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.fitness = 0
        self.solution = []
        self.visited = []

    def search(self, graph, max_steps):
        self.solution.append(self.start)
        steps = 0

        while (self.solution[-1] != self.end) or (steps < max_steps):
            self.step(graph)
            steps += 1

    def evaluate(self):
        pass

    def step(self, graph):
        current = self.solution[-1]
        neighbors = set(graph.neighbors(current)) - set(self.visited)
        weights = [graph[current][n]['weight'] for n in neighbors]
        next = neighbors[weighted_choice(weights)]

        self.solution.append(next)
        self.visited.append(current)

    def __len__(self):
        return len(self.solution)

    def __contains__(self, item):
        return item in zip(self.solution, self.solution[1:])

    def __cmp__(self, other):
        return cmp(self.fitness, other.fitness)


class BinaryAnt(AntLike):
    def evaluate(self):
        if self.solution[-1] == self.end:
            self.fitness = 1


class ProportionalAnt(AntLike):
    def evaluate(self):
        if self.solution[-1] == self.end:
            self.fitness = 1 / len(self)
