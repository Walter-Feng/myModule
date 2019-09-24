import atom
import re
from atom import gaussian

class pyscf_rhf_input(object):
    def __init__(self, filename='NONAME'):
        self.basis_set = '6-31g'
        self.filename = filename
        self.option = 'NOT DEFINED'
        self.filestring = ''
        self.atoms = None

    def tostring(self):

        self.filestring =  "import pyscf, math \n" \
                           "import numpy \n" \
                           "from pyscf import gto, scf, mcscf,dft \n" \
                           "\n" \
                           "numpy.set_printoptions(threshold=numpy.inf)\n" \
                           "\n" \
                           "mol = gto.Mole()\n" \
                           "mol.build( \n" \
                           "atom =\n" \
                           "'''\n"

        atoms_string = ''
        for i in self.atoms:
            atoms_string += ' ' + i.get_label().ljust(18)
            for j in i.get_cartesian():
                atoms_string += str(float(j)).ljust(16)
            atoms_string += '\n'

        self.filestring += atoms_string
        self.filestring += '\n\n'
        self.filestring += 'basis=' + self.basis_set + "\n\n"
        self.filestring += ")\n\n"
        self.filestring += "print(\"AO_LABELS:\")\n"
        self.filestring += "print(gto.ao_labels(mol))\n"
        self.filestring += "print(\"AO_LABELS_END\")\n\n"

        self.filestring += "mf = scf.RHF(mol) \n"
        self.filestring += "mf.kernel()\n\n"

        self.filestring += "mf.analyze()\n\n"

        self.filestring += "print(\"MO_COEFF:\")\n"
        self.filestring += "print(mf.mo_coeff)\n"
        self.filestring += "print(\"MO_COEFF_END\")\n"

    def write(self, directory='', postfix='.com'):

        if directory == '':
            with open(directory+self.filename+postfix, 'w') as f:
                f.write(self.filestring)

        else:
            if re.match(r"^.+?\/$", directory):
                with open(directory+self.filename+postfix, 'w') as f:
                    f.write(self.filestring)

            else:
                if re.match(r"^.+\.in$", directory):
                    with open(directory, 'w') as f:
                        self.filename = directory[:-5]
                        self.tostring()

                        f.write(self.filestring)

                else:
                    with open(directory+postfix, 'w') as f:
                        self.filename = directory
                        self.tostring()

                        f.write(self.filestring)

class pyscf_dft_input(object):
    def __init__(self, xc='b3lyp', filename='NONAME'):
        self.basis_set = '6-31g'
        self.xc = xc
        self.filename = filename
        self.option = 'NOT DEFINED'
        self.filestring = ''
        self.atoms = None

    def tostring(self):

        self.filestring =  "import pyscf, math \n" \
                           "import numpy \n" \
                           "from pyscf import gto, scf, mcscf,dft \n" \
                           "\n" \
                           "numpy.set_printoptions(threshold=numpy.inf)\n" \
                           "\n" \
                           "mol = gto.Mole()\n" \
                           "mol.build( \n" \
                           "atom =\n" \
                           "'''\n"

        atoms_string = ''
        for i in self.atoms:
            atoms_string += ' ' + i.get_label().ljust(18)
            for j in i.get_cartesian():
                atoms_string += str(float(j)).ljust(16)
            atoms_string += '\n'

        self.filestring += atoms_string
        self.filestring += '\n\n'
        self.filestring += 'basis=' + self.basis_set + "\n\n"
        self.filestring += ")\n\n"
        self.filestring += "print(\"AO_LABELS:\")\n"
        self.filestring += "print(gto.ao_labels(mol))\n"
        self.filestring += "print(\"AO_LABELS_END\")\n\n"

        self.filestring += "mf = dft.RKS(mol) \n"
        self.filestring += "mf.xc = \"" + self.xc + "\"\n"
        self.filestring += "mf.kernel()\n\n"

        self.filestring += "mf.analyze()\n\n"

        self.filestring += "print(\"MO_COEFF:\")\n"
        self.filestring += "print(mf.mo_coeff)\n"
        self.filestring += "print(\"MO_COEFF_END\")\n"

    def write(self, directory='', postfix='.com'):

        if directory == '':
            with open(directory+self.filename+postfix, 'w') as f:
                f.write(self.filestring)

        else:
            if re.match(r"^.+?\/$", directory):
                with open(directory+self.filename+postfix, 'w') as f:
                    f.write(self.filestring)

            else:
                if re.match(r"^.+\.in$", directory):
                    with open(directory, 'w') as f:
                        self.filename = directory[:-5]
                        self.chkfilename = directory[:-5]
                        self.tostring()

                        f.write(self.filestring)

                else:
                    with open(directory+postfix, 'w') as f:
                        self.filename = directory
                        self.tostring()

                        f.write(self.filestring)



# The string should be analogous to: " H  1.0000  -1.0000000 1.00000  INFO"
def atom_template(atom_string):
    split_string = atom_string.split()
    label = split_string[0]
    cartesian = list(map(float, split_string[1:4]))

    return atom.atom(atom.dict_inv_enquiry(label, atom.PERIODIC_TABLE), cartesian=cartesian)


def xyz_file_read_to_rhf(file_directory):
    with open(file_directory, 'r') as f:
        filestring = f.read()

        atom_list = [atom_template(i.group(0)) for i in gaussian.ATOMS_MATCH.finditer(filestring)]
        result = pyscf_rhf_input()

        result.atoms = atom_list
        return result

def xyz_file_read_to_dft(file_directory):
    with open(file_directory, 'r') as f:
        filestring = f.read()

        atom_list = [atom_template(i.group(0)) for i in gaussian.ATOMS_MATCH.finditer(filestring)]
        result = pyscf_dft_input()

        result.atoms = atom_list
        return result