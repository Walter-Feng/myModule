import atom

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


class gaussian_input(object):
    def __init__(self):
        self.xc = 'hf'
        self.basis_set = '6-31g'
        self.opt = False
        self.modredundant = False
        self.modredundant_string = ''
        self.freq = False
        self.raman = False
        self.titlecard = 'Title Card Required'
        self.filename = 'Noname'
        self.chkfilename = self.filename
        self.geom = False
        self.geom_string = ''
        self.charge = 0
        self.spin = 1
        self.filestring = ''
        self.atoms = None

    def tostring(self):
        chkstring = '%' + 'chk=' + self.chkfilename + '.chk'

        methodstring = '#'
        if self.opt:
            methodstring += ' opt'
            if self.modredundant:
                methodstring += '=modredundant'

        if self.freq:
            methodstring += ' freq'
            if self.raman:
                methodstring += '(raman,savenormalmodes)'

        methodstring += ' ' + self.xc
        methodstring += '/' + self.basis_set
        if self.geom_string:
            methodstring += ' geom=connectivity'

        charge_spin_string = str(self.charge) + ' ' + str(self.spin)

        atoms_string = ''
        for i in self.atoms:
            atoms_string += ' ' + i.get_label().ljust(18)
            for j in i.get_cartesian():
                atoms_string += str(j).ljust(16)
            atoms_string += '\n'

        self.filestring = chkstring + '\n' + methodstring + '\n\n' + self.titlecard + '\n\n'
        self.filestring += charge_spin_string + '\n'
        self.filestring += atoms_string + '\n' + self.geom_string
        self.filestring += '\n\n' + self.modredundant_string
        self.filestring += '\n\n'

    def chkfile_sync(self):
        self.chkfilename = self.filename

    def write(self, dir='', postfix='.com'):
        with open(dir+self.filename+postfix, 'w') as f:
            f.write(self.filestring)

