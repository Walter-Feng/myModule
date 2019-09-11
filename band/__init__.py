import numpy as np
import math

###################################
#
#
#    Global regular expression matches
#
#
###################################

FCC_SPECIAL_POINT_DICT = {
    'G': [0,0,0],
    'X': [0.0,0.5,0.5],
    'W': [0.25,0.75,0.5],
    'K': [0.375,0.75,0.375],
    'L': [0.5,0.5,0.5],
    'U': [0.25,0.625,0.625]
}

###################################
#
#         Classes 
#
###################################

class band(object):

    def __init__(self,k_points,evals,start_label = 'Start',end_label = 'End',color = 'b',unit = 'eV'):
        self.__k_points = np.array(k_points)
        self.__evals = np.array(evals)
        self.__length = len(k_points)
        self.color = color
        self.start_label = start_label
        self.end_label = end_label
        self.__unit = unit

    def length(self):
        return self.__length

    def get_k_points(self):
        return self.__k_points

    def get_evals(self):
        return self.__evals

    def get_unit(self):
        return self.__unit

    def get_step(self):
        np_arrayed_k_points = np.array(self.__k_points)
        return math.sqrt(np.dot(np_arrayed_k_points[1]-np_arrayed_k_points[0],np_arrayed_k_points[1]-np_arrayed_k_points[0]))

    def flatten(self):
        step = band.get_step(self)
        self.xarray = np.array(list(step*i for i in range(self.__length)))

    def Hartree_to_eV(self):
        if self.__unit == 'Hartree':
            self.__evals = self.__evals * 27.21138624598
            self.__unit = 'eV'
        

    def eV_to_Hartree(self):
        if self.__unit == 'eV':
            self.__evals = self.__evals / 27.21138624598
            self.__unit = 'Hartree'

# containing several bands over a certain k_points list, which is assumed be between two special points
class bands(object):
    def __init__(self,k_points,bands_evals,start_label = 'Start',end_label = 'End', unit = 'eV'):
        self.__k_points = k_points
        self.__bands_evals = bands_evals
        self.__length = len(k_points)
        self.__n_evals = len(bands_evals[0])
        self.colors = ['b' for i in range(self.__n_evals)]
        self.start_label = start_label
        self.end_label = end_label
        self.__unit = unit

    def length(self):
        return self.__length

    def get_k_points(self):
        return self.__k_points

    def n_evals(self):
        return self.__n_evals

    def get_evals(self):
        return self.__bands_evals

    def get_unit(self):
        return self.__unit

    def get_step(self):
        np_arrayed_k_points = np.array(self.__k_points)
        return math.sqrt(np.dot(np_arrayed_k_points[1]-np_arrayed_k_points[0],np_arrayed_k_points[1]-np_arrayed_k_points[0]))

    def flatten(self):
        step = band.get_step(self)
        self.xarray = list(step*i for i in range(self.__length))

    def get_band(self,index):
        np_arrayed_evals = np.array(self.__bands_evals)
        np_arrayed_evals = np.transpose(np_arrayed_evals)
        return band(self.__k_points,np_arrayed_evals[index],start_label = self.start_label,end_label = self.end_label, color = self.colors[index])

    def color_sync(self,color):
        self.colors = [color for i in range(self.__n_evals)]

    def get_bands(self,start_index,end_index):
        np_arrayed_evals = self.__bands_evals
        np_arrayed_evals = np_arrayed_evals
        temp = np_arrayed_evals[start_index:end_index]
        temp = np.transpose(temp)

        result =  bands(self.__k_points,temp,start_label = self.start_label,end_label = self.end_label)

        result.colors = self.colors[start_index:end_index]

        return result


# a special class made for entos and its resembles, which take the paths among special points separately
class full_bands(object):
    def __init__(self,bands_list):
        self.__k_points_list = [i.get_k_points() for i in bands_list]
        self.__evals_list = [i.get_evals() for i in bands_list]
        self.__length = len(bands_list)
        self.__n_evals = len((bands_list[0].get_evals())[0])
        self.__unit = bands_list[0].get_unit()
        self.labels_list = [[i.start_label,i.end_label] for i in bands_list]
        self.colors_list = [i.colors for i in bands_list]
    
    def get_k_points_list(self):
        return self.__k_points_list

    def get_evals_list(self):
        return self.__evals_list

    def n_evals(self):
        return self.__n_evals
    
    def length(self):
        return self.__length
        
    def get_unit(self):
        return self.__unit

    def color_sync(self):
        self.colors_list = [self.colors_list[0] for i in self.colors_list]

    def color_unify(self,color):
        self.color_list = [[color for j in self.colors_list]]

    def flatten(self):
        x_array_list = [[math.sqrt(np.dot(np.array(i[1])-np.array(i[0]),np.array(i[1])-np.array(i[0]))) * j for j in range(len(i))] for i in self.__k_points_list]

        step_counter = 0
        x_array_deviation_list = []
        x_ticks_list = [0]

        for i in [j[-1] for j in x_array_list]:
            x_array_deviation_list.append(step_counter)
            step_counter = step_counter + i
            x_ticks_list.append(step_counter)

        self.x_array = [[j + x_array_deviation_list[i] for j in x_array_list[i]] for i in range(len(x_array_list))]

        self.x_ticks = x_ticks_list


    def labels_flatten(self):
        x_ticks_label = [self.labels_list[0][0]]
        for i in range(len(self.labels_list)-1):
            if self.labels_list[i][1]==self.labels_list[i+1][0]:
                x_ticks_label.append(self.labels_list[i][1])
            else:
                x_ticks_label.append(self.labels_list[i][1] + '|' + self.labels_list[i+1][0])
        x_ticks_label.append(self.labels_list[len(self.labels_list)-1][1])
        self.flattened_labels = x_ticks_label

    # decompose into object `bands`, namely part of the bands(eigenvalues) between two special points
    def decompose(self,index):
        result = bands(self.__k_points_list[index],self.__evals_list[index], start_label=self.labels_list[index][0],end_label=self.labels_list[index][1])

        return result

    def get_bands(self,start_index,end_index):
        length = self.__length

        return full_bands([self.decompose(i).get_bands(start_index,end_index) for i in range(length)])

    def Hartree_to_eV(self):
        if self.__unit == 'Hartree':
            self.__evals_list = [[[i * 27.21138624598 for i in j] for j in k] for k in self.__evals_list]
            self.__unit = 'eV'       

    def eV_to_Hartree(self):
        if self.__unit == 'eV':
            self.__evals_list = [[[i / 27.21138624598 for i in j] for j in k] for k in self.__evals_list]
            self.__unit = 'Hartree'

    def find_zero_point(self,HOMO_index):
        return max(flatten([[j[HOMO_index] for j in i] for i in self.__evals_list]))

    def get_band_gap(self,HOMO_index,LUMO_index):
        Fermi_energy = max(flatten([[j[HOMO_index] for j in i] for i in self.__evals_list]))
        LUMO_energy = min(flatten([[j[LUMO_index] for j in i] for i in self.__evals_list]))
        self.band_gap = LUMO_energy - Fermi_energy
        return self.band_gap

    def print_band_gap(self):
        print('Band gap : ' + str(self.band_gap) + ' ' + self.__unit)


    def set_zero_point(self,HOMO_index):
        self.__evals_list = [[[i - self.find_zero_point(HOMO_index) for i in j] for j in k] for k in self.__evals_list]



#################################
#
#
#         Functions
#
#
################################

def array_cmp(array_1,array_2):
    if len(array_1)!=len(array_2):
        return False
    else:
        for i in range(len(array_1)):
            if array_1[i] != array_2[i]:
                return False

        return True

def split_in_list(target_list,ref_list):
    array = []
    sub_array = []
    for i in range(len(target_list)):
        sub_array.append(target_list[i])
        if (ref_list[i]):
            array.append(sub_array)
            sub_array=[]
        
    if sub_array!=[]:
        array.append(sub_array)
    
    return array

# combine a list of objects of class `band` into object of class `bands`
def band_combine(band_list):
    k_points = band_list[0].get_k_points()
    bands_evals = np.array([i.get_evals() for i in band_list])
    bands_evals = np.transpose(bands_evals)

    result = bands(k_points,bands_evals,start_label = band_list.start_label,end_label = band_list.end_label)

    result.colors = [i.color for i in band_list]

    return result


# generate a list of k points between two special points
def path_k_points_generate(start_coord,end_coord,samples):
    return np.array([start_coord + (end_coord-start_coord)*i/(samples-1) for i in range(samples)])

# split the array into subarrays with different length specified by split_list
# example:  [1,2,3,4,5,6] --split by [2,3,1]---> [[1,2,3],[4,5],[6]]
def array_split(array,split_list):
    result = []
    counter = 0
    for i in split_list:
        result.append(array[counter:counter+i])
        counter = counter + i
    
    return result

# add the starting special point of each subarray from the previous subarray, a bit like 'healing' or 'complementing' each band
# example [1,2,3,4,5,6,7] ---split by [1,2,2,2] ----> [[1],[2,3],[4,5],[6,7]] ----heal----> [[1,2,3],[3,4,5],[5,6,7]]
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

def dict_inv_enquiry(dictionary,value):
    for i in dictionary:
        if array_cmp(dictionary[i],value):
            return i
        
    return value

def dict_inv_search(dictionary,value):
    for i in dictionary:
        if array_cmp(dictionary[i],value):
            return True

    return False

def split_dict(target_list,dictionary):

    array = []
    sub_array = []

    for i in target_list:
        sub_array.append(i)
        for j in dictionary:
            if array_cmp(dictionary[j],i):
                array.append(sub_array)
                sub_array=[]
        
    if sub_array!=[]:
        array.append(sub_array)
    
    return array

def filter_dict(target_list,dictionary):
    
    return list(filter(lambda x:dict_inv_search(dictionary,x),target_list))


flatten = lambda l: [item for sublist in l for item in sublist]


def filter_convert_dict(target_list,dictionary):

    filtered_list = list(filter(lambda x:dict_inv_search(dictionary,x),target_list))

    return list(map(lambda x: dict_inv_enquiry(dictionary,x),filtered_list))

def label_list_heal(label_list):
    return [[label_list[i],label_list[i+1]] for i in range(len(label_list)-1)]


def to_full_bands_template(k_points_list,eigenvalues,labels_list):
    return full_bands([bands(k_points_list[i],eigenvalues[i],start_label=labels_list[i][0],end_label=labels_list[i][1]) for i in range(len(k_points_list))])

