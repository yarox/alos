from utils import weightify, connect_db
from rules import bush_mosteller_update, incremental_learning_update
from ants import ProportionalAnt, BinaryAnt
from random import uniform
from networkx import tutte_graph


graph = tutte_graph()

start, end = 44, 33
generations, max_steps = 250, 25

updates_list = [(bush_mosteller_update, 0), (incremental_learning_update, 1)]
kinds_list = [BinaryAnt, ProportionalAnt]


if __name__ == '__main__':
    db = connect_db('alos-experiment1')
    weightify(graph, uniform, 0, 1)

    for update, learning_rate in updates_list:
        for kind in kinds_list:

            # Database setup
            name = '{0}_{1}_{2}'
            collection_agents = db[name.format('agents', update.__name__, kind.__name__)]
            collection_pheromones = db[name.format('pheromones', update.__name__, kind.__name__)]

            for i in range(generations):
                agent = kind(start, end)
                info = []

                # Construct solutions
                agent.search(graph, max_steps)
                agent.evaluate()

                info.append({'generation': i,
                             'agent': 0,
                             'fitness': agent.fitness,
                             'solution': agent.solution})

                # Update pheromones
                for a, b in agent.edges_travelled():
                    weight = graph[a][b]['weight']
                    graph[a][b]['weight'] = update(learning_rate, weight, agent.fitness)

                # Log generation info
                collection_agents.insert(info)
                print('# generation {0}. Fitness {1}'.format(i, agent.fitness))

                # Log pheromone info
                collection_pheromones.insert({'generation': i,
                                              'pheromones': graph.edges(data=True)})
