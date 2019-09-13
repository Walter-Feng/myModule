import numpy as np
import math


##################################
#
#    Global variables
#
#################################

PERIODIC_TABLE = {
    1:  "H",
    2:  "He",
    3:  "Li",
    4:  "Be",
    5:  "B",
    6:  "C",
    7:  "N",
    8:  "O",
    9:  "F",
    10:	"Ne",
    11:	"Na",
    12:	"Mg",
    13:	"Al",
    14:	"Si",
    15: "P",
    16: "S",
    17:	"Cl",
    18:	"Ar",
    19: "K",
    20:	"Ca",
    21:	"Sc",
    22:	"Ti",
    23: "V",
    24:	"Cr",
    25:	"Mn",
    26:	"Fe",
    27:	"Co",
    28:	"Ni",
    29:	"Cu",
    30:	"Zn",
    31:	"Ga",
    32:	"Ge",
    33:	"As",
    34:	"Se",
    35:	"Br",
    36:	"Kr",
    37:	"Rb",
    38:	"Sr",
    39: "Y",
    40:	"Zr",
    41:	"Nb",
    42:	"Mo",
    43:	"Tc",
    44:	"Ru",
    45:	"Rh",
    46:	"Pd",
    47:	"Ag",
    48:	"Cd",
    49:	"In",
    50:	"Sn",
    51:	"Sb",
    52:	"Te",
    53: "I",
    54:	"Xe",
    55:	"Cs",
    56:	"Ba",
    57:	"La",
    58:	"Ce",
    59:	"Pr",
    60:	"Nd",
    61:	"Pm",
    62:	"Sm",
    63:	"Eu",
    64:	"Gd",
    65:	"Tb",
    66:	"Dy",
    67:	"Ho",
    68:	"Er",
    69:	"Tm",
    70:	"Yb",
    71:	"Lu",
    72:	"Hf",
    73:	"Ta",
    74: "W",
    75:	"Re",
    76:	"Os",
    77:	"Ir",
    78:	"Pt",
    79:	"Au",
    80:	"Hg",
    81:	"Tl",
    82:	"Pb",
    83:	"Bi",
    84:	"Po",
    85:	"At",
    86:	"Rn",
    87:	"Fr",
    88:	"Ra",
    89:	"Ac",
    90:	"Th",
    91:	"Pa",
    92: "U",
    93:	"Np",
    94:	"Pu",
    95:	"Am",
    96:	"Cm",
    97:	"Bk",
    98:	"Cf",
    99:	"Es",
    100: "Fm",
    101: "Md",
    102: "No",
    103: "Lr",
    104: "Rf",
    105: "Db",
    106: "Sg",
    107: "Bh",
    108: "Hs",
    109: "Mt",
    110: "Ds",
    111: "Rg",
    112: "Cn",
    113: "Nh",
    114: "Fl",
    115: "Mc",
    116: "Lv",
    117: "Ts",
    118: "Og"
}


####################################
#
#        Classes
#
####################################

class atom(object):

    def __init__(self, num, cartesian=None, unit="angstrom"):

        if cartesian is None:
            cartesian = [0, 0, 0]
        self.__atom_num = num
        self.__label = PERIODIC_TABLE[num]
        self.__cartesian = cartesian
        self.__unit = unit

    def get_atom_num(self):
        return self.__atom_num

    def get_label(self):
        return self.__label

    def get_cartesian(self):
        return self.__cartesian

    def get_unit(self):
        return self.__unit

    def set_atom_num(self, num):
        self.__atom_num = num
        self.__label = PERIODIC_TABLE[num]

    def set_label(self, label):
        self.__label = label
        if dict_inv_search(label, PERIODIC_TABLE):
            self.__atom_num = dict_inv_enquiry(label, PERIODIC_TABLE)
        else:
            raise Exception("Element {} is not found in periodic table.".format(label))

    def set_cartesian(self, cartesian):
        self.__cartesian = cartesian

    def unit_convert_to_bohr(self):
        if self.__unit == 'angstrom':
            self.__cartesian = [i / 0.529177210903 for i in self.__cartesian]

        if self.__unit == 'SI':
            self.__cartesian = [i / 5.29177210903e-11 for i in self.__cartesian]
            
        self.__unit = 'bohr'

    def unit_convert_to_angstrom(self):
        if self.__unit == 'bohr':
            self.__cartesian = [i * 0.529177210903 for i in self.__cartesian]

        if self.__unit == 'SI':
            self.__cartesian = [i * 1e10 for i in self.__cartesian]

        self.__unit = 'angstrom'

#########################################
#
#        Functions
#
########################################


def is_member(value, iterable):
    for i in iterable:
        if value == i:
            return True

    return False


def dict_inv_enquiry(value, dictionary):
    for i in dictionary:
        if dictionary[i] == value:
            return i
        
    return value


def dict_inv_search(value, dictionary):
    for i in dictionary:
        if dictionary[i] == value:
            return True

    return False


def rot(a_vec, b_vec):
    x = np.linalg.det([[a_vec[1], a_vec[2]], [b_vec[1], b_vec[2]]])
    y = - np.linalg.det([[a_vec[0], a_vec[2]], [b_vec[0], b_vec[2]]])
    z = np.linalg.det([[a_vec[0], a_vec[1]], [b_vec[0], b_vec[1]]])

    return [x, y, z]


def norm(vec):
    return np.dot(np.array(vec), np.array(vec))


def ortho_mat(vec):
    z = np.array(vec) / math.sqrt(norm(vec))
    if z[0] == 0:
        x = np.array([1, 0, 0])
    else:
        x = np.array([- (z[1] + z[2]) / z[0], 1, 1])

    x = x / math.sqrt(norm(x))

    y = np.array(rot(z, x))

    y = y / math.sqrt(norm(y))

    return np.array([x, y, z])


def rotation(coordinate, ref_point, ref_vec, deg):

    reference_point = np.array(ref_point)
    translated_cartesian = np.array(coordinate) - reference_point

    tr_basis_mat = ortho_mat(ref_vec).transpose()

    coefficient = np.linalg.solve(tr_basis_mat, translated_cartesian)

    coefficient = np.array([coefficient[0] * math.cos(deg) - coefficient[1] * math.sin(deg),
                            coefficient[0] * math.sin(deg) + coefficient[1] * math.cos(deg),
                            coefficient[2]])

    return list(tr_basis_mat.dot(coefficient) + reference_point)


def remove_axis_vec(coordinate, ref_point, ref_vec):

    reference_point = np.array(ref_point)
    translated_cartesian = np.array(coordinate) - reference_point

    tr_basis_mat = ortho_mat(ref_vec).transpose()

    coefficient = np.linalg.solve(tr_basis_mat, translated_cartesian)

    coefficient = np.array([coefficient[0], coefficient[1], 0])

    return list(tr_basis_mat.dot(coefficient))


def bond_length(a_atom, b_atom):
    ab = np.array(a_atom.get_cartesian()) - np.array(b_atom.get_cartesian())

    return math.sqrt(np.dot(ab, ab))


def bond_angle(a_atom, center_atom, b_atom):
    ac = np.array(a_atom.get_cartesian()) - np.array(center_atom.get_cartesian())
    bc = np.array(b_atom.get_cartesian()) - np.array(center_atom.get_cartesian())

    return math.acos(np.dot(ac, bc) / math.sqrt(norm(ac)) / math.sqrt(norm(bc)))


def bond_dihedral_angle(a_atom, b_atom, c_atom, d_atom):
    axis = np.array(b_atom.get_cartesian()) - np.array(c_atom.get_cartesian())

    axis_removed_ab = remove_axis_vec(a_atom.get_cartesian(), b_atom.get_cartesian(), axis)
    axis_removed_dc = remove_axis_vec(d_atom.get_cartesian(), c_atom.get_cartesian(), axis)

    return math.acos(np.dot(axis_removed_ab, axis_removed_dc)
                     / math.sqrt(norm(axis_removed_ab))
                     / math.sqrt(norm(axis_removed_dc)))


# all atoms in `group' should be bound to a_atom
def set_bond_length(a_atom, b_atom, length, group=None):
    vec = np.array(b_atom.get_cartesian()) - np.array(a_atom.get_cartesian())
    change = (math.sqrt(norm(vec)) - length) / math.sqrt(norm(vec)) * vec

    if group is not None:
        for i in group:
            i.set_cartesian(list(np.array(i.get_cartesian()) + change))
    else:
        a_atom.set_cartesian(list(np.array(a_atom.get_cartesian()) + change))


# all atoms in `group' should be bound to a_atom
def set_bond_angle(a_atom, center_atom, b_atom, angle, group=None):
    original_angle = bond_angle(a_atom, center_atom, b_atom)
    ac = np.array(a_atom.get_cartesian()) - np.array(center_atom.get_cartesian())
    bc = np.array(b_atom.get_cartesian()) - np.array(center_atom.get_cartesian())
    axis = np.array(rot(ac, bc))

    change = angle - original_angle

    if group is not None:
        for i in group:
            i.set_cartesian(rotation(i.get_cartesian(), center_atom.get_cartesian(), axis, change))

    else:
        a_atom.set_cartesian(rotation(a_atom.get_cartesian(), center_atom.get_cartesian(), axis, change))


# all atoms in `group' should be bound to a_atom
def set_bond_dihedral_angle(a_atom, b_atom, c_atom, d_atom, angle, group=None):
    axis = np.array(b_atom.get_cartesian()) - np.array(c_atom.get_cartesian())
    original_angle = bond_dihedral_angle(a_atom, b_atom, c_atom, d_atom)

    change = angle - original_angle

    if group is not None:
        for i in group:
            i.set_cartesian(rotation(i.get_cartesian(), b_atom, axis, change))

    else:
        a_atom.set_cartesian(rotation(a_atom.get_cartesian(), b_atom, axis, change))
