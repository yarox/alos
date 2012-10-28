from numpy import cumsum, sum, searchsorted, random


def weighted_choice(weights):
    t = cumsum(weights)
    s = sum(weights)
    return searchsorted(t, random.random(1) * s)[0]
