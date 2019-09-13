import numpy as np
import re
import band
import json
import math

ENTOS_FILENAME_MATCH = re.compile(r"(?P<filename>[a-zA-z \\\-_\d]+?\.json)")


def band_coordinates_list(band_path_dict):
    n_samples = band_path_dict['n_samples']

    start_coordinate = np.array(band_path_dict['k_point_start'])
    end_coordinate = np.array(band_path_dict['k_point_end'])

    coordinates_list = [start_coordinate + (end_coordinate - start_coordinate) * i / (n_samples - 1) for i in range(n_samples)]

    return coordinates_list

def band_eigenvalues_list(band_path_dict):
    tot_number = len(band_path_dict['sample_0']['density_re'])
    n_samples = band_path_dict['n_samples']

    eigenvalues = np.array([band.np_array_fill_math_inf(np.array(band_path_dict['sample_'+str(i)]['eigenvalues']),tot_number) for i in range(n_samples)])

    return eigenvalues

def band_label_list(band_path_dict):
    return [band_path_dict['label_start'] , band_path_dict['label_end']]

def band_parse(band_path_dict):
    return band_coordinates_list(band_path_dict), band_eigenvalues_list(band_path_dict), band_label_list(band_path_dict)

def band_to_bands(band_path_dict):
    coordinates_list,eigenvalues_list,label_list = band_parse(band_path_dict)

    return band.bands(coordinates_list,eigenvalues_list,start_label = label_list[0], end_label = label_list[1], unit = 'Hartree')

def named_structure_to_full_bands(named_structure_dict):
    n_band_paths = named_structure_dict['n_band_paths']
    
    return band.full_bands([band_to_bands(named_structure_dict['band_path_' + str(n)]) for n in range(n_band_paths)])

def file_full_extract(json_dir):
    with open(json_dir,'r') as f:
        temp = f.read()
        inp = json.loads(temp)
        namelist = [i for i in inp]

        return namelist,list(map(named_structure_to_full_bands,[inp[i] for i in inp]))