from utils import weightify, connect_db
from rules import ant_system_update
from ants import ProportionalAnt
from random import uniform
from networkx import tutte_graph


graph = tutte_graph()

start, end = 44, 33
generations, max_steps = 250, 25

agents_list = [5, 10, 15, 50, 100]
rho_list = [0.01, 0.5]


if __name__ == '__main__':
    db = connect_db('alos-experiment0')
    weightify(graph, uniform, 0, 1)

    for rho in rho_list:
        for agents in agents_list:

            # Database setup
            name = '{0}_{1}_{2}'
            collection_agents = db[name.format('agents', agents, rho)]
            collection_pheromones = db[name.format('pheromones', agents, rho)]

            for i in range(generations):
                population = [ProportionalAnt(start, end) for x in range(agents)]
                info = []

                # Construct solutions
                for j, agent in enumerate(population):
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
                for a, b in graph.edges():
                    weight = graph[a][b]['weight']
                    increase = sum([agent.fitness for agent in population
                                    if (a, b) in agent or (b, a) in agent])

                    graph[a][b]['weight'] = ant_system_update(rho, weight, increase)

                # Log pheromone info
                collection_pheromones.insert({'generation': i,
                                              'pheromones': graph.edges(data=True)})
