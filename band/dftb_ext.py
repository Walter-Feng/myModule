import numpy as np
import band
import re
import math

DFTB_KPOINT_MATCH = re.compile(r"(?P<num>[\d]+)[ ]+(?P<x>[\.\d]+)[ ]+(?P<y>[\.\d]+)[ ]+(?P<z>[\.\d]+)[ ]+#[ ]+(?P<name>\S+)")


def kpoints(dftb_string):

    INIT_FLAG = False
    labels_list = []
    array = []
    num_list = []

    for kpoints in DFTB_KPOINT_MATCH.finditer(dftb_string):
        kpoint = kpoints.groupdict()

        num_list.append(eval(kpoint['num']))
        label_current = kpoint['name']
        current = np.array([eval(kpoint['x']),eval(kpoint['y']),eval(kpoint['z'])])

        if INIT_FLAG:
            labels_list.append([label_mem,label_current])
            array.append(band.path_k_points_generate(mem,current,eval(kpoint['num'])+1))

        INIT_FLAG = True
        label_mem = kpoint['name']
        mem = np.array([eval(kpoint['x']),eval(kpoint['y']),eval(kpoint['z'])])

    

    return labels_list,num_list,np.array(array)

def evals(dftb_out_string,num_list):

    array = []

    lists = dftb_out_string.split("\n")
    lists.remove('')
    for i in lists:
        bands = i.split()
        del bands[0]
        array.append(list(map(eval,bands)))

    return band.split_array_heal(band.array_split(array,num_list))


def to_full_bands(dftb_dir):
    with open(dftb_dir + "/dftb_in.hsd",'r') as f:
        inputfile = f.read()
        labels_list,num_list,k_points_list = kpoints(inputfile)

    with open(dftb_dir + "/band_tot.dat",'r') as f:
        outputfile = f.read()
        eigenvalues = evals(outputfile,num_list)

    return band.full_bands([band.bands(k_points_list[i],eigenvalues[i],start_label=labels_list[i][0],end_label=labels_list[i][1]) for i in range(len(k_points_list))])

