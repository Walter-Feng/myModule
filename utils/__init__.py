import numpy as np

flatten = lambda l: [item for sublist in l for item in sublist]

transpose = lambda l: list(map(list, zip(*l)))

def pick_indexed_element(target_list,index):
    return[i[index] for i in target_list]


def np_sort_by_column(target_list, index):
    return target_list[target_list[:, index].argsort()]

