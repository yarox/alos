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

        while (self.solution[-1] != self.end) and (steps < max_steps):
            try:
                self.step(graph)
            except RuntimeError:
                break

            steps += 1

    def evaluate(self):
        pass

    def step(self, graph):
        current = self.solution[-1]
        neighbors = list(set(graph.neighbors(current)) - set(self.visited))

        if not neighbors:
            raise RuntimeError('agent trapped')

        weights = [graph[current][n]['weight'] for n in neighbors]
        next = neighbors[weighted_choice(weights)]

        self.solution.append(next)
        self.visited.append(current)

    def reached_end(self):
        return self.solution[-1] == self.end

    def __len__(self):
        return len(self.solution)

    def __contains__(self, item):
        return item in zip(self.solution, self.solution[1:])

    def __cmp__(self, other):
        return cmp(self.fitness, other.fitness)


class BinaryAnt(AntLike):
    def evaluate(self):
        if self.reached_end():
            self.fitness = 1
        else:
            self.fitness = 0
            self.solution = []


class ProportionalAnt(AntLike):
    def evaluate(self):
        if self.reached_end():
            self.fitness = 1 / len(self)
        else:
            self.fitness = 0
            self.solution = []
