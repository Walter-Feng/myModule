import math

def lorenzian(x, x0, sigma):
    return 0.5 * sigma / math.pi / ((x - x0) * (x - x0) + (0.5 * sigma) * (0.5 * sigma))
