import band
import math
import numpy as np
import matplotlib.pyplot as plt

def band_add_plot(band_object):
    band_object.flatten()
    plt.plot(band_object.xarray, band_object.evals, band_object.color)

def bands_add_plot_all(bands_object):
    bands_object.flatten()
    map(band_add_plot,[bands_object.get_band(i) for i in bands_object.n_evals()])

def bands_add_plot(bands_object,start_index,end_index):
    bands_object.flatten()
    map(band_add_plot,[bands_object.get_band(i) for i in range(start_index,end_index)])

def full_bands_add_plot_all(full_bands_object,**kwargs):
    full_bands_object.flatten()
    for i in range(full_bands_object.length()):
        for j in range(full_bands_object.n_evals()):
            temp = full_bands_object.get_evals_list()[i]
            plt.plot(full_bands_object.x_array[i],temp[:,j],full_bands_object.colors_list[i][j],**kwargs)

def full_bands_add_plot(full_bands_object,start_index,end_index,**kwargs):
    full_bands_object.flatten()
    for i in range(full_bands_object.length()):
        for j in range(start_index,end_index):
            temp = full_bands_object.get_evals_list()[i]
            plt.plot(full_bands_object.x_array[i],temp[:,j],full_bands_object.colors_list[i][j],**kwargs)


def full_bands_axes(full_bands_object):
    ax = plt.axes()
    ax.xaxis.grid(True)

    full_bands_object.flatten()
    full_bands_object.labels_flatten()

    plt.xlim(full_bands_object.x_ticks[0],full_bands_object.x_ticks[-1])
    plt.ylabel('Energy ('+ full_bands_object.get_unit() + ')')
    plt.xticks(full_bands_object.x_ticks,full_bands_object.flattened_labels)
