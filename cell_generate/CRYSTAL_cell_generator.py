import re
import argparse
import scipy
import os
import scipy.optimize
import numpy as np
import math

FILE_HEADER = ''

VOLUME_FLAG = True
VOLUME_START = 0.5
VOLUME_END = 3.0
VOLUME_N_SAMPLE = 30

A = 4.3358
C = 8.3397

targetstring = "4.3358 8.3397"

fix_vol = True

##########################################################
#
#
# PBS
#
#
##########################################################

JOB_NAME = "CRYSTAL17"
PARTITION = "medium"
NODES = "1"
nodes = eval(NODES)
TASKS_PER_NODE = "16"
tasks_per_node = eval(TASKS_PER_NODE)
CPUS_PER_TASK = "1"
cpus_per_task = eval(CPUS_PER_TASK)
TIME = "200:00:00"

MPIEXEC_THREAD = str(tasks_per_node * nodes)

ENV = "module add apps/crystal-14-v1.0.4-mpi"
COMMAND = 'mpirun -np ' + str(MPIEXEC_THREAD) + ' Pcrystal'
OPTION = ''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    with open("bashscript.sh", "w") as bash:
        with open(args.target, 'r') as fhandle:
            f = fhandle.read()

            for i in range(VOLUME_N_SAMPLE):
                amp = math.pow(VOLUME_START - (VOLUME_START - VOLUME_END) * i / (VOLUME_N_SAMPLE - 1))
                f.replace(targetstring, str(A * amp) + " " + str(C * amp))

                if not os.path.exists((FILE_HEADER+ str(i) + '_dir/').replace('-', '_')):
                    os.makedirs((FILE_HEADER + str(i) + '_dir/').replace('-', '_'))
                    with open(FILE_HEADER + str(i) + "_dir/" + "INPUT") as inputfile:
                        inputfile.write(f)

                    with open(FILE_HEADER + str(i) + "_dir/" + "PBS") as PBSfile:
                        pbstring = "#PBS -N " +  JOB_NAME + "\n"
                        pbstring += "#PBS -l nodes=" + NODES + ":ppn=" + TASKS_PER_NODE + "\n"
                        pbstring += "#PBS -q " + PARTITION + "\n"
                        pbstring += "#PBS -l walltime=" + TIME + "\n"
                        pbstring += "nprocs=`cat $PBS_NODEFILE | wc -l`" + "\n" + "\n"
                        
                        pbstring += "cd $PBS_O_WORKDIR" + "\n" + "\n"

                        pbstring += ENV + "\n" + "\n"
                        pbstring += COMMAND + "\n"
                        pbstring += 'mv ' + JOB_NAME +  '.o*' + ' ' + 'OUTPUT' + '\n'

                        PBSfile.write(pbstring)

                    directory = os.getcwd()

                    bash.write(('cd ' + directory + '/' + FILE_HEADER + str(i).replace('.','_') + '_dir/' + ' && ' + 'qsub '  + 'PBS' + '\n'))



