from itertools import groupby
from pymongo import Connection
from numpy import mean
from utils import smooth

from experiment1 import graph, start, end, generations, updates_list, kinds_list

import pylab
import networkx as nx


db = Connection()['alos-experiment1']
pos = nx.spring_layout(graph)
path = nx.shortest_path(graph, source=start, target=end)
print('> shortest path is {0}, with fitness {1}'.format(path, 1.0 / len(path)))

for update, learning_rate in updates_list:
    for kind in kinds_list:

        # Database setup
        name = '{0}_{1}_{2}'
        collection_agents = db[name.format('agents', update.__name__, kind.__name__)]
        collection_pheromones = db[name.format('pheromones', update.__name__, kind.__name__)]

        mean_fitness = []
        best_fitness = []
        best_solutions = []

        info = sorted(collection_agents.find(), key=lambda x: x['generation'])

        for group, generation in groupby(info, key=lambda x: x['generation']):
            #fitness = [agent['fitness'] for agent in generation]
            fitness, solutions = zip(*[(agent['fitness'], agent['solution']) for agent in generation])

            mean_fitness.append(mean(fitness))
            best_fitness.append(max(fitness))

            solutions = [solution for solution in solutions if solution]
            if solution:
                best_solutions.append(min(solutions, key=lambda x: len(x)))

        fig, ax1 = pylab.subplots()

        ax1.plot(mean_fitness)
        ax1.plot(best_fitness)

        #ax1.plot(smooth(mean_fitness, generations / 10))
        #ax1.plot(smooth(best_fitness, generations / 10))

        ax1.axhline(1.0 / len(path), ls='dashed')

        ax1.set_xlabel('Generations')
        ax1.set_ylabel('Fitness')

        ax1.set_ylim(0, top=max(best_fitness) * 0.05 + ax1.get_ylim()[1])
        ax1.set_xlim(0, right=len(mean_fitness) - 1)

        ax1.legend(('Mean', 'Best', 'Max'), 'best')

        fig.savefig('fitness_{0}_{1}.pdf'.format(update.__name__, kind.__name__))

        fig = pylab.figure()
        info = collection_pheromones.find_one({'generation': generations - 1})
        colors = [edge[2]['weight'] for edge in info['pheromones']]

        best_solution = min(best_solutions, key=lambda x: len(x))
        best_solution = zip(best_solution, best_solution[1:])

        nx.draw(graph, pos, node_color='#A0CBE2', with_labels=False)
        nx.draw_networkx_nodes(graph, pos, nodelist=[start, end], node_color='red')
        nx.draw_networkx_edges(graph, pos, edge_color='green', width=10,
                               with_labels=False, edgelist=best_solution)
        nx.draw_networkx_edges(graph, pos, edge_color=colors, width=4,
                               edge_cmap=pylab.cm.Blues, with_labels=False)
        nx.draw_networkx_edges(graph, pos, alpha=0.5, style='dashed')

        pylab.savefig('pheromones_{0}_{1}.pdf'.format(update.__name__, kind.__name__))
