import atom
import re

XC_LIST = [
    'B3LYP','B3P86','O3LYP',   # Becke Three-Parameter Hybrid Functionals
    'APFD','wB97XD',    # Functionals Including Dispersion
    'LC-wHPBE','CAM-b3LYP','wB97XD',     # Long-Range-Corrected Functionals
    'MN15','M11','SOGGA11X','N12SX','MN12SX', # Functionals from the Truhlar Group
    'PW6B05', 'PW6B95D3', 'M08HX', 'M06', 'M06HF', 'M062X',
    'M05', 'M052X',
    'PBE1PBE','HSEH1PBE','OHSE2PBE','OHSE1PBE','PBEh1PBE', # Functionals Employing PBE Correlation
    'B1B95','B1LYP','mPW1PW91','mPW1LYP','mPW1PBE','mPW3PBE', # Becke One-Parameter Hybrid Functionals
    'TPSSh', 'tHCTHhyb', 'BMK', # Functionals with τ-Dependent Gradient-Corrected Correlation
    'HISSbPBE', 'X3LYP', # Older Functionals
    'BHandH', 'BHandHLYP', # Half-and-Half Functionals
    'hf',   # Hartree-Fock method
    'mp2', 'mp4' # Moller-Plesset perturbation theory
    ]


BASIS_SET = [
    'sto-3g', 'sto-6g', 'sto-3g*', 'sto-6g*',
    '3-21g','3-21+g','3-21+g*','3-21+g**',
    '6-31g','6-311g', '6-31+g','6-31++g',
    'cc-pvdz','cc-pvtz','lanl2dz','lanl2mb','sdd','dgdzvp','dgdzvp2','gen','genecp'
]

CHK_MATCH = re.compile(r"^[ ]*%(?P<chk>\S+)$", re.MULTILINE)

METHOD_MATCH = re.compile(r"^[ ]*#[ ]+(?P<type>.+?)[ ]+(?P<method>\S+)[ ]*\/[ ]*(?P<basis>\S+)[ ]+(?P<option>.*)$",
                          re.MULTILINE)

CHARGE_SPIN_MATCH = re.compile(r"^[ ]*(?P<charge>\d+)[ ]+(?P<spin>\d+)[ ]*$", re.MULTILINE)

ATOMS_MATCH = re.compile(r"[ ]*(?P<label>[a-zA-Z]+)[ ]*(?P<x>[\d\.\-]+)[ ]*(?P<y>[\d\.\-]+)[ ]*(?P<z>[\d\.\-]+)")

GEOM_MATCH = re.compile(r"^(?P<geom>[ ]+\d+.*)$", re.MULTILINE)


class gaussian_input(object):
    def __init__(self, filename='NONAME'):
        self.xc = 'hf'
        self.basis_set = '6-31g'
        self.opt = False
        self.modredundant = False
        self.modredundant_string = ''
        self.freq = False
        self.raman = False
        self.methodstring = 'NOT DEFINED'
        self.titlecard = 'Title Card Required'
        self.filename = filename
        self.chkfilename = self.filename
        self.geom = False
        self.geom_string = ''
        self.option = 'NOT DEFINED'
        self.charge = 0
        self.spin = 1
        self.filestring = ''
        self.atoms = None

    def tostring(self):
        chkstring = '%' + 'chk=' + self.chkfilename + '.chk'

        if self.methodstring == 'NOT DEFINED':
            self.methodstring = '#'
            if self.opt:
                self.methodstring += ' opt'
                if self.modredundant:
                    self.methodstring += '=modredundant'

            if self.freq:
                self.methodstring += ' freq'
                if self.raman:
                    self.methodstring += '(raman,savenormalmodes)'

            self.methodstring += ' ' + self.xc
            self.methodstring += '/' + self.basis_set
            if self.geom_string:
                self.methodstring += ' geom=connectivity'

        charge_spin_string = str(self.charge) + ' ' + str(self.spin)

        atoms_string = ''
        for i in self.atoms:
            atoms_string += ' ' + i.get_label().ljust(18)
            for j in i.get_cartesian():
                atoms_string += str(float(j)).ljust(16)
            atoms_string += '\n'

        self.filestring = chkstring + '\n' + self.methodstring + '\n\n' + self.titlecard + '\n\n'
        self.filestring += charge_spin_string + '\n'
        self.filestring += atoms_string + '\n' + self.geom_string
        self.filestring += '\n\n' + self.modredundant_string
        self.filestring += '\n\n'

    def chkfile_sync(self):
        self.chkfilename = self.filename

    def write(self, directory='', postfix='.com'):

        if directory == '':
            with open(directory+self.filename+postfix, 'w') as f:
                f.write(self.filestring)

        else:
            if re.match(r"^.+?\/$", directory):
                with open(directory+self.filename+postfix, 'w') as f:
                    f.write(self.filestring)

            else:
                if re.match(r"^.+\.com$", directory):
                    with open(directory, 'w') as f:
                        self.filename = directory[:-5]
                        self.chkfilename = directory[:-5]
                        self.tostring()

                        f.write(self.filestring)

                else:
                    with open(directory+postfix, 'w') as f:
                        self.chkfilename = directory
                        self.filename = directory
                        self.tostring()

                        f.write(self.filestring)

    def filestring_regenerate(self):
        self.methodstring = 'NOT DEFINED'
        self.tostring()


# The string should be analogous to: " H      1.0000  -1.0000000 1.00000  INFO"
def atom_template(atom_string):
    split_string = atom_string.split()
    label = split_string[0]
    cartesian = list(map(float, split_string[1:4]))

    return atom.atom(atom.dict_inv_enquiry(label, atom.PERIODIC_TABLE), cartesian=cartesian)


def gaussian_input_read(file_directory, verbose=0):
    with open(file_directory, 'r') as f:
        filestring = f.read()

        atom_list = [atom_template(i.group(0)) for i in ATOMS_MATCH.finditer(filestring)]

        methodstring = METHOD_MATCH.search(filestring)
        method_dict = methodstring.groupdict()
        methodstring = methodstring.group(0)
        type = method_dict['type']
        method = method_dict['method']
        basis = method_dict['basis']
        option = method_dict['option']

        charge_spin_string = CHARGE_SPIN_MATCH.search(filestring)
        charge_spin_string = charge_spin_string.groupdict()
        charge = int(charge_spin_string['charge'])
        spin = int(charge_spin_string['spin'])

        geom_string = "\n".join([i.groupdict()['geom'] for i in GEOM_MATCH.finditer(filestring)])

        result = gaussian_input()

        if verbose == 0:
            result.methodstring = methodstring
        else:
            result.type = type
            result.xc = method
            result.basis_set = basis
            result.option = option

            if verbose == 1:
                result.option = option

        result.charge = charge
        result.spin = spin
        result.atoms = atom_list
        result.geom_string = geom_string

        return result


def xyz_file_read(file_directory):
    with open(file_directory, 'r') as f:
        filestring = f.read()

        atom_list = [atom_template(i.group(0)) for i in ATOMS_MATCH.finditer(filestring)]
        result = gaussian_input()

        result.atoms = atom_list
        return result