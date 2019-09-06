import numpy as np 
import band
import re

TICKS_MATCH = re.compile(r"[ ]*@[ ]+XAXIS[ ]+TICK[ ]+(?P<index>\d+)[ ]*,[ ]+(?P<tick>\S+)[ ]*")

TICKS_LABEL_MATCH = re.compile(r"[ ]*@[ ]+XAXIS[ ]+TICKLABEL[ ]+(?P<index>\d+?)[ ]*,[ ]*\"[ ]*\([ ]*(?P<x>\d+)[ ]*,[ ]*(?P<y>\d+)[ ]*,[ ]*(?P<z>\d+)[ ]*\)\/(?P<shrink>\d+)\"[ ]*")

EVALS_MATCH = re.compile(r"^[ ]+(?P<evals>.+)$",re.MULTILINE)

class flattened_full_bands(object):
    def __init__(self,special_k_points,x_ticks,bands_evals,labels_list, unit = 'eV'):
        self.special_k_points = special_k_points
        self.x_ticks = x_ticks
        self.bands_evals = np.array(bands_evals)[:,1:]
        self.length = len(bands_evals)
        self.n_evals = len(bands_evals[0])
        self.labels_list = labels_list
        self.unit = unit
        self.x_array = np.array(bands_evals)[:,0]

    def get_length(self):
        return self.length

    def get_x_ticks(self):
        return self.x_ticks

    def get_special_k_points(self):
        return self.special_k_points

    def get_evals(self):
        return self.bands_evals

    def get_unit(self):
        return self.unit

    def Hartree_to_eV(self):
        if self.unit == 'Hartree':
            self.bands_evals = self.bands_evals * 27.21138624598
            self.unit = 'eV'

    def find_zero_point(self,HOMO_index):
        return np.amax(self.bands_evals[:,HOMO_index].flatten())

    def set_zero_point(self,HOMO_index):
        self.bands_evals = self.bands_evals - self.find_zero_point(HOMO_index)


def get_ticks(crystal_str):
    return [float(i.groupdict()['tick']) for i in TICKS_MATCH.finditer(crystal_str)]

def get_tick_labels(special_k_points,dictionary):
    return list(map(lambda x:band.dict_inv_enquiry(dictionary,x),special_k_points))

def get_special_k_points(crystal_str):
    return [ list(map(eval,[i.groupdict()['x']+'/'+i.groupdict()['shrink'],i.groupdict()['y']+'/'+i.groupdict()['shrink'],i.groupdict()['z']+'/'+i.groupdict()['shrink']])) for i in TICKS_LABEL_MATCH.finditer(crystal_str) ]

def get_x_evals(crystal_str):
    return [ list(map(float,i.groupdict()['evals'].split())) for i in EVALS_MATCH.finditer(crystal_str)]

def to_flattened_full_bands(crystal_dir,dictionary):
    with open(crystal_dir,'r') as f:
        crystal_str = f.read()
        ticks = get_ticks(crystal_str)
        special_k_points = get_special_k_points(crystal_str)
        tick_labels = get_tick_labels(special_k_points,dictionary)
        evals = get_x_evals(crystal_str)
        return flattened_full_bands(special_k_points,ticks,evals,tick_labels,unit='Hartree')




