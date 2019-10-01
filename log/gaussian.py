from log import gaussian_match
import atom
import utils
import math_funcs
import matplotlib.pyplot as plt
import numpy as np

class gaussian_log(object):
    def __init__(self):
        self.coords = None
        self.freqs = None
        self.evals = None
        self.el_energies = None
        self.last_coord = None
        self.freq = None
        self.eval = None
        self.el_energy = None
        self.is_error = True

    def ir_spectrum(self,start=400,end=4000,step=0.2,sigma=10):

        xarray = []
        spectrum_array = []
        for i in np.arange(start,end,step):
            xarray.append(i)
            inten = 0
            for j in self.freq:
                inten += math_funcs.lorenzian(i,j[0],sigma) * j[3]
            spectrum_array.append(inten)

        return xarray,spectrum_array

    def ir_spectrum_plt(self,*args,subplot=None,start=400,end=4000,step=0.2,sigma=10,**kwargs):

        xarray, spectrum_array = self.ir_spectrum(start=start,end=end,step=step,sigma=sigma)

        if subplot is None:
            plt.plot(xarray,spectrum_array,*args,**kwargs)

        else:
            subplot.plot(xarray,spectrum_array,*args,**kwargs)

    def ir_spectrum_plt_show(self,*args,subplot=None,start=400,end=4000,step=0.2,sigma=10,**kwargs):

        xarray, spectrum_array = self.ir_spectrum(start=start,end=end,step=step,sigma=sigma)

        if subplot is None:
            plt.plot(xarray,spectrum_array,*args,**kwargs)

        else:
            subplot.plot(xarray,spectrum_array,*args,**kwargs)

        plt.show()


def read_el_energy_from_log(log_str):
    return [float(i.groupdict()['el_energy']) for i in gaussian_match.LOG_EL_ZERO_POINT_MATCH.finditer(log_str)]

def read_coord_from_log(log_str):

    coords_sets = []

    for i in gaussian_match.LOG_COORD_MATCH.finditer(log_str):
        i = i.groupdict()['coords'].split('\n')
        i.remove('')
        i.remove(' ')
        coords_sets.append(list(map(lambda x: atom.atom( int(x.split()[1]) ,
                                                         cartesian = list(map(float, x.split()[3:]))
                                                         )
                                   ,i)
                               )
                          )

    return coords_sets


def read_std_coord_from_log(log_str):

    coords_sets = []

    for i in gaussian_match.LOG_COORD_MATCH.finditer(log_str):
        i = i.groupdict()['coords'].split('\n')
        i.remove('')
        i.remove(' ')
        coords_sets.append(list(map(lambda x: atom.atom( int(x.split()[1]) ,
                                                         cartesian = list(map(float, x.split()[3:]))
                                                         )
                                   ,i)
                               )
                          )

    return coords_sets


def read_eval_from_log(log_str):

    eval_sets = []

    for i in gaussian_match.LOG_HARMONIC_MATCH.finditer(log_str):

        i = i.groupdict()['info']

        occ_evals = utils.flatten([ list( map(float, (j.groupdict())['evals'].split() ) ) for j in gaussian_match.LOG_OCC_EVALS_MATCH.finditer(i)])
        virt_evals = utils.flatten([ list( map(float, (j.groupdict())['evals'].split() ) ) for j in gaussian_match.LOG_VIRT_EVALS_MATCH.finditer(i)])

        eval_sets.append({"occ":occ_evals, "virt":virt_evals})

    return eval_sets


def read_freq_from_log(log_str):

    freq_sets = []

    for i in gaussian_match.LOG_HARMONIC_MATCH.finditer(log_str):

        i = i.groupdict()['info']

        freqs = utils.flatten([ list( map(float, (j.groupdict())['freqs'].split() ) ) for j in gaussian_match.LOG_FREQ_MATCH.finditer(i)])
        red_masses = utils.flatten([ list( map(float, (j.groupdict())['masses'].split() ) ) for j in gaussian_match.LOG_FREQ_RED_MASS_MATCH.finditer(i)])
        freq_consts = utils.flatten([ list( map(float, (j.groupdict())['consts'].split() ) ) for j in gaussian_match.LOG_FREQ_CONST_MATCH.finditer(i)])
        ir_inten = utils.flatten([ list( map(float, (j.groupdict())['inten'].split() ) ) for j in gaussian_match.LOG_IR_INTEN_MATCH.finditer(i)])

        assert(len(freqs) == len(red_masses))
        assert(len(freqs) == len(freq_consts))
        assert(len(freqs) == len(ir_inten))

    freq_sets.append(utils.transpose([freqs,red_masses,freq_consts,ir_inten]))

    return freq_sets

def read_log(log_str):
    g_log = gaussian_log()
    g_log.coords = read_coord_from_log(log_str)
    g_log.el_energies = read_el_energy_from_log(log_str)
    if gaussian_match.LOG_NORMAL_TERMINATION_MATCH.finditer(log_str):
        g_log.is_error = False
    else:
        g_log.is_error = True

    g_log.freqs = read_freq_from_log(log_str)
    g_log.evals = read_eval_from_log(log_str)

    g_log.last_coord = g_log.coords[-1]
    g_log.freq = g_log.freqs[-1]
    g_log.el_energy = g_log.el_energies[-1]
    g_log.eval = g_log.evals[-1]

    return g_log
