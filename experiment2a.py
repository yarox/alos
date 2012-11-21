from __future__ import division

import itertools
import rules
import ants

from utils import weightify, connect_db
from random import uniform, choice
from networkx import tutte_graph


graph = tutte_graph()

start, end = 44, 33
generations, max_steps = 250, 25

agents_list = [5, 10, 15, 50, 100]

kinds = [ants.ProportionalAnt, ants.BinaryAnt]
updates = [(rules.ant_system_update, 0.01),
           (rules.bush_mosteller_update, 0.9),
           (rules.incremental_learning_update, 0.01)]

methods = list(itertools.product(kinds, updates))


if __name__ == '__main__':
    db = connect_db('alos-experiment2a')
    weightify(graph, uniform, 0, 1)

    for agents in agents_list:
        # Database setup
        name = '{0}_{1}'
        collection_agents = db[name.format('agents', agents)]
        collection_pheromones = db[name.format('pheromones', agents)]

        for i in range(generations):
            ant_kind, (rule, learning_rate) = choice(methods)
            population = [ant_kind(start, end) for x in range(agents)]
            info = []

            # Construct solutions
            for j, agent in enumerate(population):
                agent.search(graph, max_steps)
                agent.evaluate()

                if ant_kind == ants.BinaryAnt and agent.solution:
                    fitness = 1 / len(agent.solution)
                else:
                    fitness = agent.fitness

                info.append({'generation': i,
                             'agent': j,
                             'fitness': fitness,
                             'solution': agent.solution})

            # Log generation info
            collection_agents.insert(info)
            print('# generation {0}'.format(i))

            # Update pheromones
            for a, b in graph.edges():
                weight = graph[a][b]['weight']
                increase = sum([agent.fitness for agent in population
                                if (a, b) in agent or (b, a) in agent])

                graph[a][b]['weight'] = rule(learning_rate, weight, increase)

            # Log pheromone info
            collection_pheromones.insert({'generation': i,
                                          'pheromones': graph.edges(data=True)})
