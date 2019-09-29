flatten = lambda l: [item for sublist in l for item in sublist]

transpose = lambda l: list(map(list, zip(*l)))