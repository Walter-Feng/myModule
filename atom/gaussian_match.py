import re
import atom
import utils

###########################################################
#
#
#            INPUT     MATCH
#
#
###########################################################

CHK_MATCH = re.compile(r"^[ ]*%(?P<chk>\S+)$", re.MULTILINE)

METHOD_MATCH = re.compile(r"^[ ]*#[ ]+(?P<type>.+?)[ ]+(?P<method>\S+)[ ]*\/[ ]*(?P<basis>\S+)[ ]+(?P<option>.*)$",
                          re.MULTILINE)

CHARGE_SPIN_MATCH = re.compile(r"^[ ]*(?P<charge>\d+)[ ]+(?P<spin>\d+)[ ]*$", re.MULTILINE)

ATOMS_MATCH = re.compile(r"[ ]*(?P<label>[a-zA-Z]+)[ ]*(?P<x>[\d\.\-]+)[ ]*(?P<y>[\d\.\-]+)[ ]*(?P<z>[\d\.\-]+)")

GEOM_MATCH = re.compile(r"^(?P<geom>[ ]+\d+.*)$", re.MULTILINE)


###########################################################
#
#
#            LOG     MATCH
#
#
###########################################################

LOG_COORD_MATCH = re.compile(
    r"^[ ]*Input orientation:.+?[\-]+.+?Coordinates \(Angstroms\).+?[\-]+[\S](?P<coords>.+?)[\S][\-]+$",
    re.DOTALL | re.MULTILINE)

LOG_STD_COORD_MATCH = re.compile(
    r"^[ ]*Standard orientation:.+?[\-]+.+?Coordinates \(Angstroms\).+?[\-]+[\S](?P<coords>.+?)[\S][\-]+$",
    re.DOTALL | re.MULTILINE)

LOG_EVALS_MATCH = re.compile(
    r"^[ ]*(?P<evals>Alpha[ ]+occ\.[ ]+eigenvalues[ ]+--[ ]+.+?)Condensed to atoms.+?$",
    re.DOTALL | re.MULTILINE)

LOG_OCC_EVALS_MATCH = re.compile(
    r"^[ ]*Alpha[ ]+occ\.[ ]+eigenvalues[ ]+--[ ]+(?P<evals>.+?)$",
    re.MULTILINE
)

LOG_VIRT_EVALS_MATCH = re.compile(
    r"^[ ]*Alpha[ ]+virt\.[ ]+eigenvalues[ ]+--[ ]+(?P<evals>.+?)$",
    re.MULTILINE
)

LOG_HARMONIC_MATCH = re.compile(
    r"^[ ]*Harmonic(?P<info>.+?)Thermochemistry.+?$",
    re.DOTALL | re.MULTILINE
)

LOG_FREQ_MATCH = re.compile(
    r"^[ ]*Frequencies[ ]+--[ ]+(?P<freqs>.+?)$",
    re.MULTILINE
)

LOG_FREQ_RED_MASS_MATCH = re.compile(
    r"^[ ]*Red\. masses[ ]+--[ ]+(?P<masses>.+?)$",
    re.MULTILINE
)

LOG_FREQ_CONST_MATCH = re.compile(
    r"^[ ]*Frc consts[ ]+--[ ]+(?P<consts>.+?)$",
    re.MULTILINE
)

LOG_IR_INTEN_MATCH = re.compile(
    r"^[ ]*IR Inten[ ]+--[ ]+(?P<inten>.+?)$",
    re.MULTILINE
)

def read_coord_from_log(log_str):

    coords_sets = []

    for i in LOG_COORD_MATCH.finditer(log_str):
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

    for i in LOG_COORD_MATCH.finditer(log_str):
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

    for i in LOG_HARMONIC_MATCH.finditer(log_str):

        i = i.groupdict()['info']

        occ_evals = utils.flatten([ list( map(float, (j.groupdict())['evals'].split() ) ) for j in LOG_OCC_EVALS_MATCH.finditer(i)])
        virt_evals = utils.flatten([ list( map(float, (j.groupdict())['evals'].split() ) ) for j in LOG_VIRT_EVALS_MATCH.finditer(i)])

        freq_sets.append({"occ":occ_evals, "virt":virt_evals})

    return eval_sets

def read_freq_from_log(log_str):

    freq_sets = []

    for i in LOG_HARMONIC_MATCH.finditer(log_str):

        i = i.groupdict()['info']

        freqs = utils.flatten([ list( map(float, (i.groupdict())['freqs'].split() ) ) for j in LOG_FREQ_MATCH.finditer(i)])
        red_masses = utils.flatten([ list( map(float, (i.groupdict())['masses'].split() ) ) for j in LOG_FREQ_RED_MASS_MATCH.finditer(i)])
        freq_consts = utils.flatten([ list( map(float, (i.groupdict())['consts'].split() ) ) for j in LOG_FREQ_CONST_MATCH.finditer(i)])
        ir_inten = utils.flatten([ list( map(float, (i.groupdict())['inten'].split() ) ) for j in LOG_IR_INTEN_MATCH.finditer(i)])

        assert(len(freqs) == len(red_masses))
        assert(len(freqs) == len(freq_consts))
        assert(len(freqs) == len(ir_inten))

    evals_sets.append(utils.transpose[freqs,red_masses,freq_consts,ir_inten])

    return freq_sets