import re

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

LOG_EL_ZERO_POINT_MATCH = re.compile(
    r"^[ ]*Sum of electronic and zero-point Energies=[ ]+(?P<el_energy>\S+)$",
    re.MULTILINE
)

LOG_NORMAL_TERMINATION_MATCH = re.compile(r"Normal Termination")