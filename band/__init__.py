import numpy as np
import math



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
        self.__k_points = np.array(k_points)
        self.__bands_evals = np.array(bands_evals)
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
        self.xarray = np.array(list(step*i for i in range(self.__length)))

    def get_band(self,index):
        np_arrayed_evals = np.array(self.__bands_evals)
        np_arrayed_evals = np.transpose(np_arrayed_evals)
        return band(self.__k_points,np_arrayed_evals[index],start_label = self.start_label,end_label = self.end_label, color = self.colors[index])

    def color_sync(self,color):
        self.colors = [color for i in range(self.__n_evals)]

    def get_bands(self,start_index,end_index):
        np_arrayed_evals = np.array(self.__bands_evals)
        np_arrayed_evals = np.transpose(np_arrayed_evals)
        temp = np_arrayed_evals[start_index:end_index]
        temp = np.transpose(temp)

        result =  bands(self.__k_points,temp,start_label = self.start_label,end_label = self.end_label)

        result.colors = self.colors[start_index:end_index]

        return result


# a special class made for entos and its resembles, which take the paths among special points separately
class full_bands(object):
    def __init__(self,bands_list):
        self.__k_points_list = np.array([i.get_k_points() for i in bands_list])
        self.__evals_list = np.array([i.get_evals() for i in bands_list])
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
        x_array_list = np.array([[math.sqrt(np.dot(i[1]-i[0],i[1]-i[0])) * j for j in range(len(i))] for i in self.__k_points_list])

        step_counter = 0
        x_array_deviation_list = []
        x_ticks_list = [0]

        for i in x_array_list[:,-1]:
            x_array_deviation_list.append(step_counter)
            step_counter = step_counter + i
            x_ticks_list.append(step_counter)

        self.x_array = np.array([x_array_list[i] + x_array_deviation_list[i] for i in range(len(x_array_list))])

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
            self.__evals_list = self.__evals_list * 27.21138624598
            self.__unit = 'eV'       

    def eV_to_Hartree(self):
        if self.__unit == 'eV':
            self.__evals_list = self.__evals_list / 27.21138624598
            self.__unit = 'Hartree'

    def find_zero_point(self,HOMO_index):
        return np.amax(self.__evals_list[:,:,HOMO_index].flatten())

    def set_zero_point(self,HOMO_index):
        self.__evals_list = self.__evals_list - self.find_zero_point(HOMO_index)



#################################
#
#
#         Functions
#
#
################################

# combine a list of objects of class `band` into object of class `bands`
def band_combine(band_list):
    k_points = band_list[0].get_k_points()
    bands_evals = np.array([i.get_evals() for i in band_list])
    bands_evals = np.transpose(bands_evals)

    result = bands(k_points,bands_evals,start_label = band_list.start_label,end_label = band_list.end_label)

    result.colors = [i.color for i in band_list]

    return result

