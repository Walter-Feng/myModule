import dos
import json

class entos_dos(object):
    def __init__(self,dos_dictionary):
        tot_dos = dos_dictionary['total_density_of_states']
        self.tot_dos = dos.dos(tot_dos['energy_grids'],tot_dos['density'])

        proj_dos = dos_dictionary['projected_density_of_states']
        n_ao = proj_dos['n_ao']
        self.n_ao = n_ao
        self.proj_dos = [dos.dos(proj_dos['orbital_' + str(i)]['energy_grids'],proj_dos['orbital_' + str(i)]['density']) for i in range(n_ao)]

        gp_dos = dos_dictionary['gross_population_density_of_states']
        n_ao = proj_dos['n_ao']
        self.gp_dos = [dos.dos(gp_dos['orbital_' + str(i)]['energy_grids'],gp_dos['orbital_' + str(i)]['density']) for i in range(n_ao)]

        self.fermi_energy = dos_dictionary['Fermi_energy']

def file_extract(json_dir):
    with open(json_dir,'r') as f:
        temp = f.read()
        inp = json.loads(temp)

        return entos_dos(inp['density_of_states'])