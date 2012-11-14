from __future__ import division
from pymongo import Connection
import numpy


def weighted_choice(weights):
    t = numpy.cumsum(weights)
    s = numpy.sum(weights)
    return numpy.searchsorted(t, numpy.random.random(1) * s)[0]


def weightify(graph, generator, *args, **kwargs):
    for i, j in graph.edges():
        graph[i][j]['weight'] = generator(*args, **kwargs)


def smooth(x, window_size=11):
    if len(x) < window_size:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_size < 3:
        return x

    s = numpy.r_[x[window_size - 1:0:-1], x, x[-1:-window_size:-1]]
    w = numpy.ones(window_size, 'd')
    y = numpy.convolve(w / w.sum(), s, mode='valid')

    return y[:len(x)]


def connect_db(db_name):
    connection = Connection()
    connection.drop_database(db_name)
    return connection[db_name]
