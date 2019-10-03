import re

LATTICE_MATCH = re.compile(r"^[ ]*\*+[ ]*\n[ ]*(?P<lattice>LATTICE[ ]+PARAMETERS.+?)\*+[ ]*$",re.MULTILINE|re.DOTALL)

FINAL_GEOMETRY_MATCH = re.compile(r"(?P<result>FINAL OPTIMIZED GEOMETRY.+)",re.MULTILINE|re.DOTALL)

ATOMS_MATCH = re.compile(
    r"^[ ]*\*+[ ]*\n[ ]*ATOMS[ ]+IN.+?\*+[ ]*\n(?P<atoms>.+?)[ ]*T = ATOM BELONGING TO THE ASYMMETRIC UNIT[ ]*$",
        re.MULTILINE | re.DOTALL)

OPT_TOTAL_ENERGY_MATCH = re.compile(
    r"^[ ]*TOTAL ENERGY.+?(?P<fuck>[\-\+\dE]+\.[\-\+\dE]+).+?(?P<fuck2>[\-\+\.\dE]+)[ ]*$",
    re.MULTILINE)

OPT_MATCH = re.compile(r"[ ]*(OPT)+(OPT)+(?P<opt>.+)FINAL OPTIMIZED GEOMETRY",re.DOTALL)

INIT_MATCH = re.compile(r"EEEEEE(?P<init>.+?)(OPT)+(OPT)+")

