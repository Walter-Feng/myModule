import numpy as np
import band
import re
import json
import math

KPOINT_MATCH = re.compile(r"(?P<num>[\d]+)[ ]+(?P<x>[\.\d]+)[ ]+(?P<y>[\.\d]+)[ ]+(?P<z>[\.\d]+)[ ]+#[ ]+(?P<name>\S+)")
FILENAME_MATCH = re.compile(r"(?P<filename>[a-zA-z \\\-_\d]+?\.json)")

def path_k_points_generate(start_coord,end_coord,samples):
    return np.array([start_coord + (end_coord-start_coord)*i/(samples-1) for i in range(samples)])

def array_split(array,split_list):
    result = []
    counter = 0
    for i in split_list:
        result.append(array[counter:counter+i])
        counter = counter + i
    
    return result

def split_array_heal(array):
    INIT_FLAG = False
    result = []

    for i in array:
        if INIT_FLAG:
            i.insert(0,mem[-1])
            result.append(i)
        INIT_FLAG = True
        mem = i

    return result

def np_array_append_math_inf(array,num):
    if num<0:
        return array
    else:
        return np.append(array,np.array([math.inf for i in range(num)]))

def np_array_fill_math_inf(array,total):
    length = len(array)
    return np_array_append_math_inf(array,total-length)

def entos_json_band_coordinates_list(band_path_dict):
    n_samples = band_path_dict['n_samples']

    start_coordinate = np.array(band_path_dict['symmetry_point_start'])
    end_coordinate = np.array(band_path_dict['symmetry_point_end'])

    coordinates_list = [start_coordinate + (end_coordinate - start_coordinate) * i / (n_samples - 1) for i in range(n_samples)]

    return coordinates_list

def entos_json_band_eigenvalues_list(band_path_dict):
    tot_number = len(band_path_dict['sample_0']['density_re'])
    n_samples = band_path_dict['n_samples']

    eigenvalues = np.array([np_array_fill_math_inf(np.array(band_path_dict['sample_'+str(i)]['eigenvalues']),tot_number) for i in range(n_samples)])

    return eigenvalues

def entos_json_band_label_list(band_path_dict):
    return [band_path_dict['label_start'] , band_path_dict['label_end']]

def entos_json_band_parse(band_path_dict):
    return entos_json_band_coordinates_list(band_path_dict), entos_json_band_eigenvalues_list(band_path_dict), entos_json_band_label_list(band_path_dict)

def entos_json_band_to_bands(band_path_dict):
    coordinates_list,eigenvalues_list,label_list = entos_json_band_parse(band_path_dict)

    return band.bands(coordinates_list,eigenvalues_list,start_label = label_list[0], end_label = label_list[1], unit = 'Hartree')

def entos_json_named_structure_to_full_bands(named_structure_dict):
    n_band_paths = named_structure_dict['n_band_paths']
    
    return band.full_bands([entos_json_band_to_bands(named_structure_dict['band_path_' + str(n)]) for n in range(n_band_paths)])

def entos_json_file_full_extract(json_dir):
    with open(json_dir,'r') as f:
        temp = f.read()
        inp = json.loads(temp)
        namelist = [i for i in inp]

        return namelist,list(map(entos_json_named_structure_to_full_bands,[inp[i] for i in inp]))

def dftb_kpoints(dftb_string):

    INIT_FLAG = False
    labels_list = []
    array = []
    num_list = []

    for kpoints in KPOINT_MATCH.finditer(dftb_string):
        kpoint = kpoints.groupdict()

        num_list.append(eval(kpoint['num']))
        label_current = kpoint['name']
        current = np.array([eval(kpoint['x']),eval(kpoint['y']),eval(kpoint['z'])])

        if INIT_FLAG:
            labels_list.append([label_mem,label_current])
            array.append(path_k_points_generate(mem,current,eval(kpoint['num'])+1))

        INIT_FLAG = True
        label_mem = kpoint['name']
        mem = np.array([eval(kpoint['x']),eval(kpoint['y']),eval(kpoint['z'])])

    

    return labels_list,num_list,np.array(array)

def dftb_evals(dftb_out_string,num_list):

    array = []

    lists = dftb_out_string.split("\n")
    lists.remove('')
    for i in lists:
        bands = i.split()
        del bands[0]
        array.append(list(map(eval,bands)))

    return split_array_heal(array_split(array,num_list))


def dftb_to_full_bands(dftb_dir):
    with open(dftb_dir + "/dftb_in.hsd",'r') as f:
        inputfile = f.read()
        labels_list,num_list,k_points_list = dftb_kpoints(inputfile)

    with open(dftb_dir + "/band_tot.dat",'r') as f:
        outputfile = f.read()
        evals = dftb_evals(outputfile,num_list)

    return band.full_bands([band.bands(k_points_list[i],evals[i],start_label=labels_list[i][0],end_label=labels_list[i][1]) for i in range(len(k_points_list))])
