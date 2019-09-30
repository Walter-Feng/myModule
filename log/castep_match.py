import re

ENERGY_MATCH = re.compile(r"^[ ]*Final energy, E[ ]+=[ ]*(?P<energy>\S+)[ ]+(?P<unit>\S+)$",
                          re.MULTILINE)
ENTHALPY_MATCH = re.compile(
    r"^[ ]*LBFGS: finished iteration[ ]+(?P<iteration>\S+)[ ]+with enthalpy=[ ]*(?P<enthalpy>\S+)[ ]+(?P<unit>\S+)$",
    re.MULTILINE
)

VOLUME_MATCH = re.compile(
    r"^[ ]*Current cell volume =[ ]+(?P<vol>\S+)[ ]+(?P<unit>\S+)$"
)

LATTICE_PARAM_MATCH = re.compile(
    r'''
    ^[ ]*Lattice[ ]+parameters\(A\)[ ]+Cell[ ]+Angles[ ]*\n
    [ ]+a[ ]+=[ ]+(?P<a>\S+)[ ]+alpha[ ]+=[ ]+(?P<alpha>\S+)[ ]*\n
    [ ]+a[ ]+=[ ]+(?P<b>\S+)[ ]+alpha[ ]+=[ ]+(?P<beta>\S+)[ ]*\n
    [ ]+a[ ]+=[ ]+(?P<c>\S+)[ ]+alpha[ ]+=[ ]+(?P<gamma>\S+)[ ]*$
    '''
    , re.VERBOSE
)

CELL_MATCH = re.compile(
    r'''
    ^[ ]*\-+[ ]*\n[ ]*Cell[ ]+Contents[ ]*\n[ ]*\-+[ ]*\s+x+\s+(?P<atoms>x.+?)x+?x+$
    '''
    , re.VERBOSE | re.DOTALL
)

ATOM_MATCH = re.compile(
    r'''
    ^[ ]*x[ ]+(?P<atom>\S+)[ ]+(?P<atom_num>\d+)[ ]+(?P<u>\S+)[ ]+(?P<v>\S+)[ ]+(?P<w>\S+)[ ]+x$
    '''
)

LBFG_CONVERGE_FAIL_MATCH = re.compile("LBFGS: WARNING - Geometry optimization failed to converge after")

LBFG_FINAL_MATCH = re.compile("LBFGS: Final Configuration:")