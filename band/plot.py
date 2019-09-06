import band
import band.cp2k_ext
import band.castep_ext
import band.dftb_ext
import band.entos_ext
import band.crystal_ext
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

def add_vline(xticks_array,color):
    for point in xticks_array:
        plt.axvline(x=point, color=color)

def full_bands_add_plot_all(full_bands_object,label="NULL",*args,**kwargs):
    full_bands_object.flatten()
    for i in range(full_bands_object.length()):
        for j in range(full_bands_object.n_evals()):
            plt.plot(full_bands_object.x_array[i],[ bands[j] for bands in full_bands_object.get_evals_list()[i]],full_bands_object.colors_list[i][j],*args, **kwargs)

    if label != "NULL":
        plt.plot(full_bands_object.x_array[0],[ bands[0] for bands in full_bands_object.get_evals_list()[0]], full_bands_object.colors_list[0][0],label=label,*args, **kwargs)

def full_bands_add_sub_plot_all(subplot,full_bands_object,*args,**kwargs):
    full_bands_object.flatten()
    for i in range(full_bands_object.length()):
        for j in range(full_bands_object.n_evals()):
            subplot.plot(full_bands_object.x_array[i],[ bands[j] for bands in full_bands_object.get_evals_list()[i]],full_bands_object.colors_list[i][j],*args,**kwargs)

def full_bands_add_plot(full_bands_object,start_index,end_index,label="NULL",*args,**kwargs):
    full_bands_object.flatten()
    for i in range(full_bands_object.length()):
        for j in range(start_index,end_index):
            plt.plot(full_bands_object.x_array[i],[ bands[j] for bands in full_bands_object.get_evals_list()[i]],full_bands_object.colors_list[i][j],*args, **kwargs)

    if label != "NULL":
        plt.plot(full_bands_object.x_array[0],[ bands[start_index] for bands in full_bands_object.get_evals_list()[0]], full_bands_object.colors_list[0][start_index],label=label,*args, **kwargs)


def full_bands_add_sub_plot(subplot,full_bands_object,start_index,end_index,*args,**kwargs):
    full_bands_object.flatten()
    for i in range(full_bands_object.length()):
        for j in range(start_index,end_index):
            subplot.plot(full_bands_object.x_array[i],[ bands[j] for bands in full_bands_object.get_evals_list()[i]],full_bands_object.colors_list[i][j],*args, **kwargs)


def full_bands_axes(full_bands_object,xlim_add = 0):
    ax = plt.axes()
    ax.xaxis.grid(True)

    full_bands_object.flatten()
    full_bands_object.labels_flatten()

    plt.xlim(full_bands_object.x_ticks[0],full_bands_object.x_ticks[-1] + xlim_add)
    plt.ylabel('Energy ('+ full_bands_object.get_unit() + ')')
    plt.xticks(full_bands_object.x_ticks,full_bands_object.flattened_labels)

def full_bands_axes_sub_plot(subplot,full_bands_object,xlim_add = 0):

    full_bands_object.flatten()
    full_bands_object.labels_flatten()

    subplot.set_xticks(full_bands_object.x_ticks)
    subplot.set_xtickslabels(full_bands_object.flattened_labels)
    subplot.set_xlim(full_bands_object.x_ticks[0],full_bands_object.x_ticks[-1] + xlim_add)

    subplot.ylabel('Energy ('+ full_bands_object.get_unit() + ')')

    add_vline(full_bands_object.x_ticks,'black')

def flattened_full_bands_add_plot_all(flattened_full_bands_obj, *args, **kwargs):
    for i in range(flattened_full_bands_obj.n_evals):
            plt.plot(flattened_full_bands_obj.x_array,flattened_full_bands_obj.bands_evals[:,i],*args,**kwargs)

def flattened_full_bands_add_plot(flattened_full_bands_obj, start_index, end_index, *args, **kwargs):
    plt.plot(*band.flatten([[flattened_full_bands_obj.x_array,flattened_full_bands_obj.bands_evals[:,i]] for i in range(start_index,end_index)]),*args,**kwargs)

def flattened_full_bands_axes(flattened_full_bands_obj,xlim_add = 0):
    ax = plt.axes()
    ax.xaxis.grid(True)

    plt.xlim(flattened_full_bands_obj.x_array[0],flattened_full_bands_obj.x_array[-1] + xlim_add)
    plt.ylabel('Energy ('+ flattened_full_bands_obj.get_unit() + ')')
    plt.xticks(flattened_full_bands_obj.x_ticks,flattened_full_bands_obj.labels_list)