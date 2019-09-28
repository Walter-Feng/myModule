import numpy as np 
import matplotlib.pyplot as plt


class dos(object):
    def __init__(self,energy_grid,density):
        assert(len(energy_grid) == len(density))
        self.energy_grid = energy_grid
        self.density = density

    def integral(self):
        integral = 0
        sectors = np.transpose(np.array([self.energy_grid[:-1],self.energy_grid[1:]]))
        density_pairs = np.transpose(np.array([self.density[:-1],self.density[1:]]))
        for i in range(len(self.energy_grid) - 1):
            sector = sectors[i]
            interval = sector[1] - sector[0]
            density_pair = density_pairs[i]
            integral += (density_pair[0] + density_pair[1]) * interval / 2

        return integral

    def cdf(self):
        integral = 0
        sectors = np.transpose(np.array([self.energy_grid[:-1],self.energy_grid[1:]]))
        density_pairs = np.transpose(np.array([self.density[:-1],self.density[1:]]))

        cdf = []
        for i in range(len(self.energy_grid) - 1):
            sector = sectors[i]
            interval = sector[1] - sector[0]
            density_pair = density_pairs[i]
            integral += (density_pair[0] + density_pair[1]) * interval / 2
            cdf.append([sector[0] + interval /2, integral])
            
        cdf = np.transpose(np.array(cdf))

        return cdf_dos(cdf[0],cdf[1])

    def plot(self,*args,**kwargs):
        plt.plot(self.energy_grid,self.density,*args,**kwargs)

    def subplot(self,subplot,*args,**kwargs):
        subplot.plot(self.energy_grid,self.density,*args,**kwargs)


class cdf_dos(object):
    def __init__py(self,energy_grid,density):
        self.energy_grid = energy_grid
        self.density = density

    def pdf(self):

        sectors = np.transpose(np.array([self.energy_grid[:-1],self.energy_grid[1:]]))
        density_pairs = np.transpose(np.array([self.density[:-1],self.density[1:]]))

        pdf = []
        for i in range(len(self.energy_grid) - 1):
            sector = sectors[i]
            interval = sector[1] - sector[0]
            density_pair = density_pairs[i]
            differential = (density_pair[1] - density_pair[0]) / interval
            pdf.append([sector[0] + interval /2, differential])
            
        pdf = np.transpose(np.array(pdf))

        return dos(pdf[0],pdf[1])

    def plot(self,*args,**kwargs):
        plt.plot(self.energy_grid,self.density,*args,**kwargs)

    def subplot(self,subplot,*args,**kwargs):
        subplot.plot(self.energy_grid,self.density,*args,**kwargs)
