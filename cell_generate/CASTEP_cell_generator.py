import re
import argparse
import scipy
import os
import scipy.optimize
import numpy as np
import math

FILE_HEADER = ''

##########################################################################
#
#
#   CELL PARAMETERS
#
#
##########################################################################

A = np.array([1,0,0])
B = np.array([0,1,0])
C = np.array([0,0,1])

a = 1
b = 1
c = 1

alpha = math.pi/2
beta = math.pi/2
gamma = math.pi/2

KPOINT_X = 7
KPOINT_Y = 7
KPOINT_Z = 7


A_MUL = 1
B_MUL = 1
C_MUL = 1

AMP_FLAG = False
A_AMPINDEX = 4
B_AMPINDEX = 4 
C_AMPINDEX = 5
STEP = 0.1

VOLUME_FLAG = True
VOLUME_START = 0.5
VOLUME_END = 3.0
VOLUME_N_SAMPLE = 30

fix_all_cell = False
fix_vol = True
symmetry_generate = True
####################################################################
#
#
# PARAM PARMETERS
#
#
#####################################################################

TASK = "geometryoptimisation"
TASK_OPTION_LIST = [
    "SinglePoint",
	"BandStructure",
	"GeometryOptimization",
	"MolecularDynamics",
	'Optics',
	'Phonon','frequencies',
	'Efield'
	'Phonon+Efield',
	'TransitionStateSearch',
	'MagRes',
	'Elnes',
	'ElectronicSpectroscopy'
]
XC = "PW91"
CL_LIST = [
    	"LDA",
	"PW91",
	"PBE",
	"RPBE",
	"WC",
	"PBESOL",
	"HF",
	"HF-LDA",
	"sX",
	"sX-LDA",
	"PBE0",
	"B3LYP",
	"HSE03",
	"HSE06"
]
SEDC_APPLY = False
SEDC_SCHEME = "OBS"
SEDC_SCHEME_LIST=[
    "TS",
    "OBS",
    "G06",
    "JCHS"
]
BASIS_PRICISION = "precise"
OPT_STRATEGY_BIAS = "3"
MAX_SCF_CYCLES = "1000"
ELEC_ENERGY_TOL = "1.0e-6 eV"
GEOM_ENERGY_TOL = "5.0e-6 eV"
GEOM_FORCE_TOL = "0.01 eV/ang"
GEOM_STRESS_TOL = "0.01 GPa"
GEOM_MAX_ITER = "300"
GEOM_DISP_TOL = "0.001 ang"
GEOM_MODULUS_EST = "40 GPa"
POPN_CALCULATE = "true"
ENERGY_UNIT = "kj/mol"
NUM_DUMP_CYCLES = "30"

##########################################################
#
#
# SBATCH 
#
#
##########################################################

JOB_NAME = "CASTEP"
PARTITION = "cpu"
NODES = "1"
nodes = eval(NODES)
TASKS_PER_NODE = "24"
tasks_per_node = eval(TASKS_PER_NODE)
CPUS_PER_TASK = "1"
cpus_per_task = eval(CPUS_PER_TASK)
TIME = "14-00:00:00"
MAIL_TYPE = "FAIL"

MPIEXEC_THREAD = str(tasks_per_node * nodes) 
COMMAND = 'castep.mpi'
OPTION = ''

BASHRCDIR = '/mnt/storage/home/dj19970/.bashrc'

def F(z,A,B,c,alpha,beta):
    A_norm = np.dot(A,A)
    B_norm = np.dot(B,B)
    x = - (A[1]*B[2]*z - A[1] * math.sqrt(B_norm) * c * math.cos(alpha) - A[2] * B[1] * z + B[1] * math.sqrt(A_norm) * c * math.cos(beta))/(A[1] * B[0] - B[1] * A[0])
    y = (A[0]*B[2]*z - A[0] * math.sqrt(B_norm) * c * math.cos(alpha) - A[2] * B[0] * z + B[0] * math.sqrt(A_norm) * c * math.cos(beta))/(A[1] * B[0] - B[1] * A[0])
    return (z - c ** 2 + x ** 2 + y ** 2)


def derive_angle(vector1,vector2):
    A_norm = np.dot(vector1,vector1)
    B_norm = np.dot(vector2,vector2)
    ip = np.dot(vector1,vector2)
    result = ip / math.sqrt(A_norm) / math.sqrt(B_norm)
    return result

def derive_vector(a,b,c,alpha,beta,gamma):
    A = np.array([a,0,0])
    B = np.array([b * math.cos(gamma), b * math.sin(gamma),0])
    A_norm = np.dot(A,A)
    B_norm = np.dot(B,B)
    z = scipy.optimize.broyden1(lambda a:F(a,A,B,c,alpha,beta), c, f_tol=1e-12)
    x = - (A[1]*B[2]*z - A[1] * math.sqrt(B_norm) * c * math.cos(alpha) - A[2] * B[1] * z + B[1] * math.sqrt(A_norm) * c * math.cos(beta))/(A[1] * B[0] - B[1] * A[0])
    y = (A[0]*B[2]*z - A[0] * math.sqrt(B_norm) * c * math.cos(alpha) - A[2] * B[0] * z + B[0] * math.sqrt(A_norm) * c * math.cos(beta))/(A[1] * B[0] - B[1] * A[0])
    C = np.array([x,y,z])
    return np.array([A,B,C])

def deg_rad_convert(deg):
    return (deg/180 * math.pi)

def rad_deg_convert(rad):
    return (rad / math.pi * 180)

COORD_MATCH = re.compile(r"%block[ ]+positions_frac[\s]*(?P<Atoms>.+)[\s]*%endblock[ ]+positions_frac",re.DOTALL)

ATOM_MATCH = re.compile(r"(?P<name>\S+)[ ]+(?P<x>\S+)[ ]+(?P<y>\S+)[ ]+(?P<z>\S+)")

ABC_MATCH = re.compile(r"%block[ ]+lattice_abc[\s]*(?P<a>\S+?)[ ]+(?P<b>\S+?)[ ]+(?P<c>\S+?)[\s]*(?P<alpha>\S+?)[ ]+(?P<beta>\S+?)[ ]+(?P<gamma>\S+?)[\s]*%endblock[ ]+lattice_abc")

KPOINT_MATCH = re.compile(r"kpoint_mp_grid[ ]+(?P<x>\S+?)[ ]+(?P<y>\S+?)[ ]+(?P<z>\S+?)")


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description=__doc__)
#     parser.add_argument('target', metavar='template', type=str, help="the template cell file")

#     args = parser.parse_args()

#     #DO THE ITERATION HERE

#     filename = args.template

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target',type=str)
    args = parser.parse_args()

    with open("bashscript.sh","w") as bash:
        with open(args.target, 'r') as fhandle:
            f = fhandle.read()
            filestring = ""
            unit_vector = []
            atoms = []


            abc = ABC_MATCH.search(f)
            abc = abc.groupdict()
            a = eval(abc['a'])
            b = eval(abc['b'])
            c = eval(abc['c'])
            alpha = deg_rad_convert(eval(abc['alpha']))
            beta = deg_rad_convert(eval(abc['beta']))
            gamma = deg_rad_convert(eval(abc['gamma']))

            coord = COORD_MATCH.search(f)
            coord = coord.groupdict()
            atoms = coord['Atoms']
            Atoms = []

            for i in ATOM_MATCH.finditer(atoms):
                coord = i.groupdict()
                Atoms.append([coord['name'],eval(coord['x']),eval(coord['y']),eval(coord['z'])])

            if AMP_FLAG:
                for A_STEP in range(-A_AMPINDEX,A_AMPINDEX):
                    # Use either of the codes (and you need to adjust the indent):
                    # for B_STEP in range(-B_AMPINDEX,B_AMPINDEX):
                    B_STEP = A_STEP 
                    for C_STEP in range(-C_AMPINDEX,C_AMPINDEX):
                        result = []
                        coordstring = ""
                        for i in range(0,A_MUL):
                            for j in range(0,B_MUL):
                                for k in range(0,C_MUL):
                                    for atom in Atoms:
                                        result.append([atom[0],atom[1]/A_MUL + i/A_MUL,atom[2]/A_MUL + j/A_MUL,atom[3]/C_MUL + k/C_MUL])
                                        #result.append([atom[0],atom[1]/A_MUL + i/A_MUL,atom[2]/B_MUL + j/B_MUL,atom[3]/C_MUL + k/C_MUL])
                        for l in result:
                            coordstring = coordstring + l[0] + ' ' + str(l[1]) + ' ' + str(l[2]) + ' ' + str(l[3]) + '\n'
                        if not os.path.exists((FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP) + '_dir/').replace('-','_')):
                            os.makedirs((FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP) + '_dir/').replace('-','_'))
                        with open((FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP) + '_dir/' + FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP)+'.cell').replace('-','_'),'w') as inputfile:
                            filestring = "! " + FILE_HEADER + " A_STEP:" + str(A_STEP)+' B_STEP:'+str(B_STEP)+' C_STEP:'+str(C_STEP) + '\n'
                            filestring +='!\n'
                            filestring += '%block lattice_abc\n'
                            filestring += str((1 + STEP * A_STEP) * a) + ' ' + str((1 + STEP * B_STEP) * b) + ' ' + str((1 + STEP * C_STEP) * c)+'\n'
                            filestring += str(rad_deg_convert(alpha)) + ' ' + str(rad_deg_convert(beta)) + ' ' + str(rad_deg_convert(gamma)) + '\n'
                            filestring += '%endblock lattice_abc\n'
                            filestring += '!\n'
                            filestring += '%block positions_frac\n'
                            for t in result:
                                filestring += t[0] + ' ' + str(t[1]) + ' ' + str(t[2]) + ' ' + str(t[3]) + '\n'
                            filestring += '%endblock positions_frac\n'
                            filestring += '!\n'
                            filestring += 'kpoint_mp_grid' + ' ' + str(KPOINT_X) + ' ' + str(KPOINT_Y) + ' ' + str(KPOINT_Z) + '\n'
                            if symmetry_generate:
                                filestring += 'symmetry_generate' + '\n'
                            if fix_all_cell:
                                filestring += 'fix_all_cell ' + 'true' + '\n'
                            filestring += '!'

                            inputfile.write(filestring)                                

                        paramstring = 'task : ' + TASK + '\n'
                        paramstring += 'xc_functional : ' + XC + '\n'
                        if SEDC_APPLY:
                            paramstring += 'SEDC_APPLY : ' + 'TRUE' + '\n'
                            paramstring += 'SEDC_SCHEME : ' + SEDC_SCHEME + '\n'
                        else:
                            paramstring += 'SEDC_APPLY : ' + 'FALSE' + '\n'
                        paramstring += 'basis_precision : ' + BASIS_PRICISION + '\n'
                        paramstring += 'fix_occupancy : ' + "false" + '\n'
                        paramstring += 'opt_strategy_bias : ' + OPT_STRATEGY_BIAS + '\n'
                        paramstring += 'max_scf_cycles : ' + MAX_SCF_CYCLES + '\n'
                        paramstring += 'geom_force_tol : ' + GEOM_FORCE_TOL + '\n'
                        paramstring += 'elec_energy_tol : ' + ELEC_ENERGY_TOL + '\n'
                        paramstring += 'geom_stress_tol : ' + GEOM_STRESS_TOL + '\n'
                        paramstring += 'geom_max_iter : ' + GEOM_MAX_ITER + '\n'
                        paramstring += 'geom_disp_tol : ' + GEOM_DISP_TOL + '\n'
                        paramstring += 'geom_modulus_est : ' + GEOM_MODULUS_EST + '\n'
                        paramstring += 'popn_calculate : ' + POPN_CALCULATE + '\n'
                        paramstring += 'energy_unit : ' + ENERGY_UNIT + '\n'
                        paramstring += 'num_dump_cycles : ' + NUM_DUMP_CYCLES + '\n'
                        paramstring += 'write_formatted_density : TRUE'

                        with open((FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP) + '_dir/' + FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP)+'.param').replace('-','_'),'w') as paramfile:
                            paramfile.write(paramstring)

                        directory = os.getcwd()
                        sbatchstring = '#!/bin/sh' + '\n'
                        sbatchstring += '#SBATCH --job-name=' + JOB_NAME + '\n'
                        sbatchstring += '#SBATCH --partition=' + PARTITION + '\n'
                        sbatchstring += '#SBATCH --nodes=' + NODES + '\n'
                        sbatchstring += '#SBATCH --tasks-per-node=' + TASKS_PER_NODE + '\n'
                        sbatchstring += '#SBATCH --cpus-per-task=' + CPUS_PER_TASK + '\n'
                        sbatchstring += '#SBATCH --time=' + TIME + '\n'
                        # sbatchstring += '#SBATCH --mail-type=' + MAIL_TYPE + '\n'
                        sbatchstring += '\n'
                        sbatchstring += 'cd $SLURM_SUBMIT_DIR' + '\n'
                        # sbatchstring += 'source ' + BASHRCDIR + '\n'
                        sbatchstring += 'module load ' + 'apps/castep/18.1' + '\n'
                        # sbatchstring += '\n'
                        # sbatchstring += '. mpi.sh' + '\n'
                        sbatchstring += '\n'
                        sbatchstring += 'mpiexec -n ' + MPIEXEC_THREAD + ' ' +  COMMAND + ' ' + (FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP)).replace("-","_") + ' ' + OPTION + '\n'

                        with open((FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP) + '_dir/' + FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP)+'.sh').replace('-','_'),'w') as sbatchfile:
                            sbatchfile.write(sbatchstring)

                        bash.write(('cd ' + directory + '/'+ FILE_HEADER + str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP) + '_dir/' + ' && ' + 'sbatch '  + FILE_HEADER+str(A_STEP)+'_'+str(B_STEP)+'_'+str(C_STEP)+'.sh' + '\n').replace("-","_"))
                    
                    else:
                        if VOLUME_FLAG:
                            for loop in [VOLUME_START + i * (VOLUME_END-VOLUME_START) / (VOLUME_N_SAMPLE - 1) for i in range(VOLUME_N_SAMPLE)]:
                                result = []
                                coordstring = ""
                                for i in range(0,A_MUL):
                                    for j in range(0,B_MUL):
                                        for k in range(0,C_MUL):
                                            for atom in Atoms:
                                                result.append([atom[0],atom[1]/A_MUL + i/A_MUL,atom[2]/A_MUL + j/A_MUL,atom[3]/C_MUL + k/C_MUL])
                                                #result.append([atom[0],atom[1]/A_MUL + i/A_MUL,atom[2]/B_MUL + j/B_MUL,atom[3]/C_MUL + k/C_MUL])
                                for l in result:
                                    coordstring = coordstring + l[0] + ' ' + str(l[1]) + ' ' + str(l[2]) + ' ' + str(l[3]) + '\n'
                                if not os.path.exists((FILE_HEADER+str(loop) + '_dir/').replace('-','_')):
                                    os.makedirs((FILE_HEADER+str(loop) + '_dir/').replace('-','_'))
                                with open((FILE_HEADER+str(loop) + '_dir/' + FILE_HEADER+str(loop)+'.cell').replace('-','_'),'w') as inputfile:
                                    filestring = "! " + FILE_HEADER + " A_STEP:" + str(A_STEP)+' B_STEP:'+str(B_STEP)+' C_STEP:'+str(C_STEP) + '\n'
                                    filestring +='!\n'
                                    filestring += '%block lattice_abc\n'
                                    filestring += str(math.pow(loop,1/3) * a) + ' ' + str(math.pow(loop,1/3) * b) + ' ' + str(math.pow(loop,1/3) * c)+'\n'
                                    filestring += str(rad_deg_convert(alpha)) + ' ' + str(rad_deg_convert(beta)) + ' ' + str(rad_deg_convert(gamma)) + '\n'
                                    filestring += '%endblock lattice_abc\n'
                                    filestring += '!\n'
                                    filestring += '%block positions_frac\n'
                                    for t in result:
                                        filestring += t[0] + ' ' + str(t[1]) + ' ' + str(t[2]) + ' ' + str(t[3]) + '\n'
                                    filestring += '%endblock positions_frac\n'
                                    filestring += '!\n'
                                    filestring += 'kpoint_mp_grid' + ' ' + str(KPOINT_X) + ' ' + str(KPOINT_Y) + ' ' + str(KPOINT_Z) + '\n'
                                    if symmetry_generate:
                                        filestring += 'symmetry_generate' + '\n'
                                    if fix_all_cell:
                                        filestring += 'fix_all_cell ' + 'true' + '\n'
                                    filestring += '!'

                                    inputfile.write(filestring)                                

                                paramstring = 'task : ' + TASK + '\n'
                                paramstring += 'xc_functional : ' + XC + '\n'
                                if SEDC_APPLY:
                                    paramstring += 'SEDC_APPLY : ' + 'TRUE' + '\n'
                                    paramstring += 'SEDC_SCHEME : ' + SEDC_SCHEME + '\n'
                                else:
                                    paramstring += 'SEDC_APPLY : ' + 'FALSE' + '\n'
                                paramstring += 'basis_precision : ' + BASIS_PRICISION + '\n'
                                paramstring += 'fix_occupancy : ' + "false" + '\n'
                                paramstring += 'opt_strategy_bias : ' + OPT_STRATEGY_BIAS + '\n'
                                paramstring += 'max_scf_cycles : ' + MAX_SCF_CYCLES + '\n'
                                paramstring += 'geom_force_tol : ' + GEOM_FORCE_TOL + '\n'
                                paramstring += 'elec_energy_tol : ' + ELEC_ENERGY_TOL + '\n'
                                paramstring += 'geom_stress_tol : ' + GEOM_STRESS_TOL + '\n'
                                paramstring += 'geom_max_iter : ' + GEOM_MAX_ITER + '\n'
                                paramstring += 'geom_disp_tol : ' + GEOM_DISP_TOL + '\n'
                                paramstring += 'geom_modulus_est : ' + GEOM_MODULUS_EST + '\n'
                                paramstring += 'popn_calculate : ' + POPN_CALCULATE + '\n'
                                paramstring += 'energy_unit : ' + ENERGY_UNIT + '\n'
                                paramstring += 'num_dump_cycles : ' + NUM_DUMP_CYCLES + '\n'
                                paramstring += 'write_formatted_density : TRUE'

                                with open((FILE_HEADER+str(loop) + '_dir/' + FILE_HEADER+str(loop)+'.param').replace('-','_'),'w') as paramfile:
                                    paramfile.write(paramstring)

                                directory = os.getcwd()
                                sbatchstring = '#!/bin/sh' + '\n'
                                sbatchstring += '#SBATCH --job-name=' + JOB_NAME + '\n'
                                sbatchstring += '#SBATCH --partition=' + PARTITION + '\n'
                                sbatchstring += '#SBATCH --nodes=' + NODES + '\n'
                                sbatchstring += '#SBATCH --tasks-per-node=' + TASKS_PER_NODE + '\n'
                                sbatchstring += '#SBATCH --cpus-per-task=' + CPUS_PER_TASK + '\n'
                                sbatchstring += '#SBATCH --time=' + TIME + '\n'
                                # sbatchstring += '#SBATCH --mail-type=' + MAIL_TYPE + '\n'
                                sbatchstring += '\n'
                                sbatchstring += 'cd $SLURM_SUBMIT_DIR' + '\n'
                                # sbatchstring += 'source ' + BASHRCDIR + '\n'
                                sbatchstring += 'module load ' + 'apps/castep/18.1' + '\n'
                                # sbatchstring += '\n'
                                # sbatchstring += '. mpi.sh' + '\n'
                                sbatchstring += '\n'
                                sbatchstring += 'mpiexec -n ' + MPIEXEC_THREAD + ' ' +  COMMAND + ' ' + (FILE_HEADER+str(loop)).replace("-","_") + ' ' + OPTION + '\n'

                                with open((FILE_HEADER+str(loop) + '_dir/' + FILE_HEADER+str(loop)+'.sh').replace('-','_'),'w') as sbatchfile:
                                    sbatchfile.write(sbatchstring)

                                bash.write(('cd ' + directory + '/'+ FILE_HEADER + str(loop) + '_dir/' + ' && ' + 'sbatch '  + FILE_HEADER+str(loop)+'.sh' + '\n').replace("-","_"))


