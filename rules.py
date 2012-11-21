

def ant_system_update(rho, weight, increase):
    return (1 - rho) * weight + increase

def bush_mosteller_update(alpha, weight, increase):
    return alpha * weight + (1 - alpha) * increase

def incremental_learning_update(delta, weight, increase):
    return weight + delta * increase
