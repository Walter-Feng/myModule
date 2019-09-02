import numpy as np
import math

class band(object):

    def __init__(self,k_points,energies,start_label = 'Start',end_label = 'End',color = 'blue'):
        self.__k_points = np.array(k_points)
        self.__energies = np.array(energies)
        self.__length = len(k_points)
        self.color = color
        self.start_label = start_label
        self.end_label = end_label

    def get_k_points(self):
        return self.__k_points

    def get_energies(self):
        return self.__energies

    def get_step(self):
        np_arrayed_k_points = np.array(self.__k_points)
        return math.sqrt(np.dot(np_arrayed_k_points[1]-np_arrayed_k_points[0],np_arrayed_k_points[1]-np_arrayed_k_points[0]))

    def flatten(self):
        step = band.get_step(self)
        self.__xarray = np.array(list(step*i for i in range(self.__length)))

# containing several bands over a certain k_points list
class bands(band):
    def __init__(self,k_points,bands_energies,start_label = 'Start',end_label = 'End'):
        self.__k_points = np.array(k_points)
        self.__bands_energies = np.array(bands_energies)
        self.__length = len(k_points)
        self.colors = ['blue' for i in self.__length]
        self.start_label = start_label
        self.end_label = end_label


    def get_band(self,index):
        np_arrayed_energies = np.array(self.__energies)
        np_arrayed_energies.transpose()
        return band(self.__k_points,np_arrayed_energies[index],start_label = self.start_label,end_label = self.end_label, color = self.colors[index])

    def color_sync(self,color):
        self.colors = [color for i in self.__length]

# combine a list of objects of class `band` into object of class `bands`
def band_combine(band_list):
    k_points = band_list[0].get_k_points()
    bands_energies = np.array([i.get_energies() for i in band_list])
    bands_energies.transpose()

    result = bands(k_points,bands_energies,start_label = band_list.start_label,end_label = band_list.end_label)

    result.colors = [i.color for i in band_list]

    return result 


class all_bands(object):
    def __init__(self,bands_list):
        self.__k_points_list = np.array([band.get_k_points(i) for i in bands_list])
        self.__energies_list = np.array([band.get_energies(i) for i in bands_list])
        self.labels_list = [[i.start_label,i.end_label] for i in bands_list]
        self.colors_list = [i.colors for i in bands_list]
    
    def color_sync(self):
        self.colors_list = [self.colors_list[0] for i in self.colors_list]

    def flatten(self):
        x_array_list = np.array([[math.sqrt(np.dot(i[1]-i[0],i[1]-i[0])) * j for j in range(i)] for i in self.__k_points_list])

        step_counter = 0
        x_array_deviation_list = []

        for i in [[j[-1] for j in x_array_list]]:
            x_array_deviation_list.append(step_counter)
            step_counter += i

        self.__x_array = np.array([x_array_list[i] + x_array_deviation_list[i] for i in range(len(x_array_list))])


