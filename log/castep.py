from log import castep_match


class castep(object):
    def __init__(self):
        self.energies = []
        self.energy_unit = "kj/mol"
        self.cells = []
        self.vols = []
        self.vol_unit = "A**3"
        self.cell_params = []
        self.is_terminated = False
        self.LBFG_is_converged = False
        self.final_energy = None
        self.final_cell = None
        self.final_vol = None
        self.final_cell_param = None


def read_energy_from_castep(castep_str):
    return [[float(i.groupdict()['energy']),i.groupdict()['unit']] for i in castep_match.ENERGY_MATCH.finditer(castep_str)]


def read_enthalpy_from_castep(castep_str):
    return [[float(i.groupdict()['enthalpy']),i.groupdict()['unit']] for i in castep_match.ENTHALPY_MATCH.finditer(castep_str)]


def read_volume_from_castep(castep_str):
    return [[float(i.groupdict()['vol']),i.groupdict()['unit']] for i in castep_match.VOLUME_MATCH.finditer(castep_str)]


def read_lattice_param_from_castep(castep_str):

    lattice_params = []

    for i in castep_match.LATTICE_PARAM_MATCH.finditer(castep_str):
        param_set = i.groupdict()
        lattice_param = {
            "a": float(param_set['a']),
            "b": float(param_set['b']),
            "c": float(param_set['c']),
            "alpha": float(param_set['alpha']),
            "beta": float(param_set['beta']),
            "gamma": float(param_set['gamma'])
        }
        lattice_params.append(lattice_param)

    return lattice_params


def read_cell_from_castep(castep_str):

    cells = []

    for i in castep_match.CELL_MATCH.finditer(castep_str):
        cell_table = i.groupdict()['atoms']

        atoms = []

        for j in castep_match.ATOM_MATCH.finditer(cell_table):
            atom = j.groupdict()
            atoms.append([atom['atom'],float(atom['u']),float(atom['v']),float(atom['w'])])

        cells.append(atoms)

    return cells

def pick_first_element(listable):
    return list(map(lambda x:x[0],listable))

def read_castep(castep_str):
    castep_obj = castep()

    castep_obj.energies = pick_first_element(read_energy_from_castep(castep_str))
    castep_obj.cell_params = read_lattice_param_from_castep(castep_str)
    castep_obj.vols = pick_first_element(read_volume_from_castep(castep_str))
    castep_obj.cells = read_cell_from_castep(castep_str)

    castep_obj.energy_unit = read_energy_from_castep(castep_str)[0][1]
    castep_obj.vol_unit = read_volume_from_castep(castep_str)[0][1]
    if castep_match.LBFG_FINAL_MATCH.search(castep_str):
        castep_obj.is_terminated = False
    else:
        castep_obj.is_terminated = True

    if castep_match.LBFG_CONVERGE_FAIL_MATCH.search(castep_str):
        castep_obj.LBFG_is_converged = False
    else:
        castep_obj.LBFG_is_converged = True

    castep_obj.final_energy = castep_obj.energies[-1]
    castep_obj.final_cell = castep_obj.cells[-1]
    castep_obj.final_cell_param = castep_obj.cell_params[-1]
    castep_obj.final_vol = castep_obj.vols[-1]

    return castep_obj
