import re

ENERGY_MATCH = re.compile(r"^[ ]*Final energy, E[ ]+=[ ]*(?P<energy>\S+)[ ]+(?P<unit>\S+)$",
                          re.MULTILINE)
ENTHALPY_MATCH = re.compile(
    r"^[ ]*LBFGS: finished iteration[ ]+(?P<iteration>\S+)[ ]+with enthalpy=[ ]*(?P<enthalpy>\S+)[ ]+(?P<unit>\S+)$",
    re.MULTILINE
)

VOLUME_MATCH = re.compile(
    r"^[ ]*Current cell volume =[ ]+(?P<vol>\S+)[ ]+(?P<unit>\S+)$", re.MULTILINE
)

LATTICE_PARAM_MATCH = re.compile(
    r'''
    [ ]*Lattice[ ]+parameters\(A\)[ ]+Cell[ ]+Angles[ ]*\n
    [ ]+a[ ]+=[ ]+(?P<a>\S+)[ ]+alpha[ ]+=[ ]+(?P<alpha>\S+)[ ]*\n
    [ ]+b[ ]+=[ ]+(?P<b>\S+)[ ]+beta[ ]+=[ ]+(?P<beta>\S+)[ ]*\n
    [ ]+c[ ]+=[ ]+(?P<c>\S+)[ ]+gamma[ ]+=[ ]+(?P<gamma>\S+)[ ]*
    '''
    , re.VERBOSE | re.MULTILINE
)

CELL_MATCH = re.compile(
    r'''
    [ ]*\-+[ ]*\n[ ]*Cell[ ]+Contents[ ]*\n[ ]*\-+[ ]*\s+x+\s+(?P<atoms>x.+?)x+?x+
    '''
    , re.VERBOSE | re.DOTALL | re.MULTILINE
)

ATOM_MATCH = re.compile(
    r'''
    ^[ ]*x[ ]+(?P<atom>\S+)[ ]+(?P<atom_num>\d+)[ ]+(?P<u>\S+)[ ]+(?P<v>\S+)[ ]+(?P<w>\S+)[ ]+x$
    '''
    , re.MULTILINE | re.VERBOSE
)

LBFG_CONVERGE_FAIL_MATCH = re.compile("LBFGS: WARNING - Geometry optimization failed to converge after")

LBFG_FINAL_MATCH = re.compile("LBFGS: Final Configuration:")