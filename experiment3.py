from functools import partial
from ants import ProportionalAnt


def ant_system_update(rho, weight, pheromone):
    return (1 - rho) * weight + pheromone


def solve(graph, start, end, AgentCreator, update_rule, agents, generations):
    for i in range(generations):
        population = [AgentCreator(start, end) for x in range(agents)]

        # Construct solutions
        for agent in population:
            agent.search(graph, max_steps)
            agent.evaluate()

        # Update pheromones
        for a, b in graph.edges():
            weight = graph[a][b]['weights']
            pheromone = sum([agent.fitness for agent in population if (a, b) in agent])
            graph[a][b]['weights'] = update_rule(weight, pheromone)


graph = None
start, end = None, None
generations, max_steps = 100, 100

agents_list = [5, 10, 50, 100]
rho_list = [0, 0.5, 1]

for agents in agents_list:
    for rho in rho_list:
        update_rule = partial(ant_system_update, rho=rho)
        solve(graph, start, end, ProportionalAnt, update_rule, agents, generations)
