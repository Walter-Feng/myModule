import quartz
import jobsys
import math
import os

expectation_printer = {
    "type": "expectation",
    "print_level": 1,
    "grade": 10
}

generic_printer = {
    "type": "generic",
    "print_level": 2
}

total_input = open("autoscript.sh", "w")
cwd = os.getcwd()

## Model 1 - cubic decay ##
if not os.path.exists('cubic_decay'):
    os.makedirs('cubic_decay')

model = quartz.quartz()

model.model = quartz.model['cubic_decay']
model.initial = quartz.initial([[1.0]], [0.0], math.pow(math.pi, -0.25))

### establish DVR ###
filename = "dvr/"
dir = 'cubic_decay/'
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = "dvr"
model.grid = [800]
model.ranges = [[-20, 20]]
model.dt = 0.005
model.steps = 2000
model.printer = generic_printer
model.print_json = True
model.json = "log.json"

model.to_json(dir + filename + 'input.json')

###### expectation ######
model.printer = expectation_printer
model.json = "exp_log.json"
model.to_json(dir + filename + 'exp_input.json')

with open(dir + filename + "PBS" , 'w') as pbsfile :
    pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS" + "\n")

with open(dir + filename + "PBS_exp", 'w') as pbsfile:
    pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS_exp" + "\n")


##### establish cwa ####
filename = "cwa/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = 'cwa'
model.grid = [30, 30]
model.ranges = [[-5, 5], [-5, 5]]
model.dt = 0.005
model.steps = 2000
model.printer = generic_printer
model.json = "log.json"

model.to_json(dir + filename + 'input.json')

###### expectation ######
model.printer = expectation_printer
model.json = "exp_log.json"
model.to_json(dir + filename + 'exp_input.json')

with open(dir + filename + "PBS" , 'w') as pbsfile :
    pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS" + "\n")

with open(dir + filename + "PBS_exp", 'w') as pbsfile:
    pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS_exp" + "\n")

##### establish cwa_smd ####
filename = "cwa_smd/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = 'cwa_smd'
model.grid = [30, 30]
model.ranges = [[-5, 5], [-5, 5]]
model.dt = 0.005
model.steps = 2000
model.printer = generic_printer
for i in range(3,11):
    if not os.path.exists(dir + filename + str(i)):
        os.makedirs(dir + filename + str(i))

    model.grade = i
    model.json = "log.json"

    model.to_json(dir + filename + str(i) + '/input.json')

###### expectation ######
    model.printer = expectation_printer
    model.json = "exp_log.json"
    model.to_json(dir + filename + str(i) + '/exp_input.json')

    with open(dir + filename + str(i) + "/PBS" , 'w') as pbsfile :
        pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS" + "\n")

    with open(dir + filename + str(i) + "/PBS_exp", 'w') as pbsfile:
        pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS_exp" + "\n")
##### establish dvr_smd ####
filename = "dvr_smd/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = 'dvr_smd'
model.grid = [30, 30]
model.ranges = [[-5, 5], [-5, 5]]
model.dt = 0.005
model.steps = 2000
model.printer = generic_printer
for i in range(3,11):
    if not os.path.exists(dir + filename + str(i)):
        os.makedirs(dir + filename + str(i))

    model.grade = i
    model.json = "log.json"
    model.printer = generic_printer

    model.to_json(dir + filename + str(i) + '/input.json')

###### expectation ######
    model.printer = expectation_printer
    model.json = "exp_log.json"
    model.to_json(dir + filename + str(i) + '/exp_input.json')

    with open(dir + filename + str(i) + "/PBS", 'w') as pbsfile:
        pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS" + "\n")

    with open(dir + filename + str(i) + "/PBS_exp", 'w') as pbsfile:
        pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS_exp" + "\n")







## Model 2 - Anharmonic ##
if not os.path.exists('anharmonic'):
    os.makedirs('anharmonic')

model = quartz.quartz()

model.model = quartz.model['anharmonic']
model.initial = quartz.initial([[1.0]], [-1.0], math.pow(math.pi, -0.25))

### establish DVR ###
filename = "dvr/"
dir = 'anharmonic/'
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = "dvr"
model.grid = [800]
model.ranges = [[-20, 20]]
model.dt = 0.005
model.steps = 2000
model.printer = generic_printer
model.print_json = True
model.json = "log.json"

model.to_json(dir + filename + 'input.json')

###### expectation ######
model.printer = expectation_printer
model.json = "exp_log.json"
model.to_json(dir + filename + 'exp_input.json')

with open(dir + filename + "PBS" , 'w') as pbsfile :
    pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS" + "\n")

with open(dir + filename + "PBS_exp", 'w') as pbsfile:
    pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS_exp" + "\n")


##### establish cwa ####
filename = "cwa/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = 'cwa'
model.grid = [30, 30]
model.ranges = [[-5, 5], [-5, 5]]
model.dt = 0.005
model.steps = 2000
model.printer = generic_printer
model.json = "log.json"

model.to_json(dir + filename + 'input.json')

###### expectation ######
model.printer = expectation_printer
model.json = "exp_log.json"
model.to_json(dir + filename + 'exp_input.json')

with open(dir + filename + "PBS" , 'w') as pbsfile :
    pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS" + "\n")

with open(dir + filename + "PBS_exp", 'w') as pbsfile:
    pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS_exp" + "\n")

##### establish cwa_smd ####
filename = "cwa_smd/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = 'cwa_smd'
model.grid = [30, 30]
model.ranges = [[-5, 5], [-5, 5]]
model.dt = 0.005
model.steps = 2000
model.printer = generic_printer
for i in range(3,11):
    if not os.path.exists(dir + filename + str(i)):
        os.makedirs(dir + filename + str(i))

    model.grade = i
    model.json = "log.json"

    model.to_json(dir + filename + str(i) + '/input.json')

###### expectation ######
    model.printer = expectation_printer
    model.json = "exp_log.json"
    model.to_json(dir + filename + str(i) + '/exp_input.json')

    with open(dir + filename + str(i) + "/PBS" , 'w') as pbsfile :
        pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS" + "\n")

    with open(dir + filename + str(i) + "/PBS_exp", 'w') as pbsfile:
        pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS_exp" + "\n")
##### establish dvr_smd ####
filename = "dvr_smd/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = 'dvr_smd'
model.grid = [30, 30]
model.ranges = [[-5, 5], [-5, 5]]
model.dt = 0.005
model.steps = 2000
model.printer = generic_printer
for i in range(3,11):
    if not os.path.exists(dir + filename + str(i)):
        os.makedirs(dir + filename + str(i))

    model.grade = i
    model.json = "log.json"
    model.printer = generic_printer

    model.to_json(dir + filename + str(i) + '/input.json')

###### expectation ######
    model.printer = expectation_printer
    model.json = "exp_log.json"
    model.to_json(dir + filename + str(i) + '/exp_input.json')

    with open(dir + filename + str(i) + "/PBS", 'w') as pbsfile:
        pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS" + "\n")

    with open(dir + filename + str(i) + "/PBS_exp", 'w') as pbsfile:
        pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS_exp" + "\n")












## Model 3 - double_well ##
if not os.path.exists('double_well'):
    os.makedirs('double_well')

model = quartz.quartz()

model.model = quartz.model['double_well']
model.initial = quartz.initial([[0.5]], [-2.5], math.pow(math.pi / 2.0, -0.25), phase_factor=[2.0])
model.mass = [1836]

### establish DVR ###
filename = "dvr/"
dir = 'double_well/'
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = "dvr"
model.grid = [400]
model.ranges = [[-10, 10]]
model.dt = 1.0
model.steps = 10000
model.printer = generic_printer
model.print_json = True
model.json = "log.json"

model.to_json(dir + filename + 'input.json')

###### expectation ######
model.printer = expectation_printer
model.json = "exp_log.json"
model.to_json(dir + filename + 'exp_input.json')

with open(dir + filename + "PBS" , 'w') as pbsfile :
    pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS" + "\n")

with open(dir + filename + "PBS_exp", 'w') as pbsfile:
    pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS_exp" + "\n")


##### establish cwa ####
filename = "cwa/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = 'cwa'
model.grid = [50,50]
model.ranges = [[-10,10],[-10,10]]
model.dt = 1.0
model.steps = 10000
model.printer = generic_printer
model.json = "log.json"

model.to_json(dir + filename + 'input.json')

###### expectation ######
model.printer = expectation_printer
model.json = "exp_log.json"
model.to_json(dir + filename + 'exp_input.json')

with open(dir + filename + "PBS" , 'w') as pbsfile :
    pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS" + "\n")

with open(dir + filename + "PBS_exp", 'w') as pbsfile:
    pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                     env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
    pbs.time = "8:00:00"
    pbs.tasks_per_node = 4
    pbs.save_output = True
    pbsfile.write(pbs.to_string())
    total_input.write("cd " + cwd + '/' + dir + filename + " && " + "qsub " + "PBS_exp" + "\n")

##### establish cwa_smd ####
filename = "cwa_smd/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = 'cwa_smd'
model.grid = [50,50]
model.ranges = [[-10,10],[-10,10]]
model.dt = 1.0
model.steps = 10000
model.printer = generic_printer
for i in range(3,11):
    if not os.path.exists(dir + filename + str(i)):
        os.makedirs(dir + filename + str(i))

    model.grade = i
    model.json = "log.json"

    model.to_json(dir + filename + str(i) + '/input.json')

###### expectation ######
    model.printer = expectation_printer
    model.json = "exp_log.json"
    model.to_json(dir + filename + str(i) + '/exp_input.json')

    with open(dir + filename + str(i) + "/PBS" , 'w') as pbsfile :
        pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS" + "\n")

    with open(dir + filename + str(i) + "/PBS_exp", 'w') as pbsfile:
        pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS_exp" + "\n" )
##### establish dvr_smd ####
filename = "dvr_smd/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
model.method = 'dvr_smd'
model.grid = [50,50]
model.ranges = [[-10,10],[-10,10]]
model.dt = 1.0
model.steps = 10000
model.printer = generic_printer
for i in range(3,11):
    if not os.path.exists(dir + filename + str(i)):
        os.makedirs(dir + filename + str(i))

    model.grade = i
    model.json = "log.json"
    model.printer = generic_printer

    model.to_json(dir + filename + str(i) + '/input.json')

###### expectation ######
    model.printer = expectation_printer
    model.json = "exp_log.json"
    model.to_json(dir + filename + str(i) + '/exp_input.json')

    with open(dir + filename + str(i) + "/PBS", 'w') as pbsfile:
        pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS" + "\n")

    with open(dir + filename + str(i) + "/PBS_exp", 'w') as pbsfile:
        pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                         env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
        pbs.time = "8:00:00"
        pbs.tasks_per_node = 4
        pbs.save_output = True
        pbsfile.write(pbs.to_string())
        total_input.write("cd " + cwd + '/' + dir + filename + str(i) + " && " + "qsub " + "PBS_exp" + "\n")

total_input.close()