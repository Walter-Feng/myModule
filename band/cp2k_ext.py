import numpy as np
import band
import re
import math

CP2K_OCC_MATCH = re.compile(r"[ ]*Number[ ]+of[ ]+occupied[ ]+orbitals:[ ]+?(?P<occorbital>\d+)")

CP2K_SET_MATCH = re.compile(r'''
[ ]*KPOINTS\| Number of K-Point Sets[ ]*\d+[\s\S]*KPOINTS\| Number of K-Points in Set[ ]+(?P<setnr>\d+)[ ]*(?P<totalpoints>\d+)(?P<content>[\s\S]*?(?=\n.*?[ ]SET|$))
''',re.DOTALL)

# special points search in cp2k
CP2K_SPOINTS_MATCH = re.compile(r'''
[ ]*
  KPOINTS\| [ ]+ Special [ ]+ K-Point [ ]+ (?P<pointnr>\S+) [ ]+ (?P<name>\S+) [ ]+ (?P<a>\S+) [ ]+ (?P<b>\S+) [ ]+ (?P<c>\S+)
''', re.VERBOSE)

# 
CP2K_POINTS_MATCH = re.compile(r'''
[ ]*
  Nr\. [ ]+ (?P<nr>\d+) [ ]+
  Spin [ ]+ (?P<spin>\d+) [ ]+
  K-Point [ ]+ (?P<a>\S+) [ ]+ (?P<b>\S+) [ ]+ (?P<c>\S+) [ ]*
  \n
[ ]* (?P<npoints>\d+) [ ]* \n
(?P<values>
  [\s\S]*?(?=\n.*?[ ] KPOINTS|Nr)  # match everything until next 'Nr.' or EOL
)
''', re.VERBOSE)

def extract(cp2k_filestr):

    all_sets_evals_list = []
    all_sets_k_points_list = []
    all_sets_labels_list = []
    all_sets_num_list = []

    for kpoint_set in CP2K_SET_MATCH.finditer(cp2k_filestr):

        labels_list = []
        evals_list = []

        set_content = kpoint_set.group('content')

        HEAD_FLAG = False

        for point in CP2K_SPOINTS_MATCH.finditer(set_content):
            spoint = point.groupdict()
            if HEAD_FLAG:
                labels_list.append([temp['name'],spoint['name']])
            HEAD_FLAG = True
            temp = spoint
        
        spnum = eval(temp['pointnr'])

        xticksmax = ( eval(kpoint_set.group('totalpoints')) - 1) / (spnum - 1)

        all_sets_num_list.append([1,[xticksmax for i in range(spnum-1)]])
        all_sets_labels_list.append(labels_list)
        all_sets_k_points_list.append(np.array([[eval(point.groupdict()['a']),eval(point.groupdict()['b']), eval(point.groupdict()['c'])] for point in CP2K_SPOINTS_MATCH.finditer(set_content)]))

        for point in CP2K_POINTS_MATCH.finditer(set_content):
            results = point.groupdict()
            results['values'] = ",".join(results['values'].split())
            line = eval('['+results['values']+']')
            evals_list.append(line)

    return all_sets_labels_list,all_sets_num_list,all_sets_k_points_list,all_sets_evals_list

def to_full_bands(cp2k_filestr):
    pass
    # all_sets_labels_list,all_sets_num_list,all_sets_k_points_list,all_sets_evals_list = extract(cp2k_filestr)

    # return [ for i in (all_sets_num_list)]

def file_full_extract(cp2k_filestr):
    pass
