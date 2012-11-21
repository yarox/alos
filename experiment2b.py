from __future__ import division

import itertools

from utils import weightify, connect_db
from random import uniform
from networkx import tutte_graph
from rules import ant_system_update
from ants import ProportionalAnt


graph = tutte_graph()

start, end = 44, 33
generations, max_steps = 250, 25

agents_list = [5, 10, 15, 50, 100]
learning_rate = 0.01


if __name__ == '__main__':
    db = connect_db('alos-experiment2b')
    weightify(graph, uniform, 0, 1)

    for agents in agents_list:
        # Database setup
        name = '{0}_{1}'
        collection_agents = db[name.format('agents', agents)]
        collection_pheromones = db[name.format('pheromones', agents)]

        for i in range(generations):
            population = [ProportionalAnt(start, end) for x in range(agents)]
            explorer = population.pop()
            info = []

            # Send the explorer agent
            explorer.search(graph, max_steps)
            explorer.evaluate()

            info.append({'generation': i,
                         'agent': 0,
                         'fitness': explorer.fitness,
                         'solution': explorer.solution})

            # Update pheromones
            for a, b in graph.edges():
                weight = graph[a][b]['weight']

                if (a, b) in explorer or (b, a) in explorer:
                    increase = explorer.fitness
                else:
                    increase = 0

                graph[a][b]['weight'] = ant_system_update(learning_rate, weight, increase)

            # Construct solutions
            for j, agent in enumerate(population, start=1):
                agent.search(graph, max_steps)
                agent.evaluate()

                info.append({'generation': i,
                             'agent': j,
                             'fitness': agent.fitness,
                             'solution': agent.solution})

            # Log generation info
            collection_agents.insert(info)
            print('# generation {0}'.format(i))

            # Update pheromones
            for a, b in explorer.edges_travelled():
                weight = graph[a][b]['weight']
                increase = sum([agent.fitness for agent in population
                                if (a, b) in agent or (b, a) in agent])

                graph[a][b]['weight'] = ant_system_update(learning_rate, weight, increase)

            # Log pheromone info
            collection_pheromones.insert({'generation': i,
                                          'pheromones': graph.edges(data=True)})
