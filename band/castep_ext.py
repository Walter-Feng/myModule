import numpy as np
import band
import re
import math

CASTEP_MATCH = re.compile(r"^[ ]*(?P<index>\d+)[ ]+(?P<x>\S+)[ ]+(?P<y>\S+)[ ]+(?P<z>\S+)[ ]+(?P<fl_x>\S+)(?P<evals>.+)$",re.MULTILINE)

FCC_SPECIAL_POINT_DICT = {
    'G': [0,0,0],
    'X': [0.0,0.5,0.5],
    'W': [0.25,0.75,0.5],
    'K': [0.375,0.75,0.375],
    'L': [0.5,0.5,0.5],
    'U': [0.25,0.625,0.625]
}


def extract(enhanced_band_dir):
    with open(enhanced_band_dir,"r") as f:
        string = f.read()

        packs = np.array(list(map(lambda x:list(map(eval,x)),[list(i.groups())[:-2] for i in CASTEP_MATCH.finditer(string)])))

        coordinates_list = packs[:,1:4]
        

        evals_list = np.array([list(map(float,i.groupdict()['evals'].split())) for i in CASTEP_MATCH.finditer(string)])
        
        fl_x_list = np.array([float(i.groupdict()['fl_x']) for i in CASTEP_MATCH.finditer(string)])
 
        return coordinates_list,fl_x_list,evals_list

def to_full_bands(enhanced_band_dir,dictionary):
    coordinates_list,fl_x_list,evals_list = extract(enhanced_band_dir)

    coordinates_list_search_result = [band.dict_inv_search(band.FCC_SPECIAL_POINT_DICT,i) for i in coordinates_list]

    evals_list = band.split_in_list(evals_list,coordinates_list_search_result)
    evals_list = band.split_array_heal(evals_list)

    k_points_list = band.split_dict(coordinates_list,dictionary)
    k_points_list = band.split_array_heal(k_points_list)

    x_ticks_list = band.filter_dict(coordinates_list,dictionary)
    label_list = band.filter_convert_dict(x_ticks_list,dictionary)

    labels_list = band.label_list_heal(label_list)

    return band.to_full_bands_template(k_points_list,evals_list,labels_list)





