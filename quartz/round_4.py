import quartz
import jobsys
import math
import os
import copy

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

template_model = quartz.quartz()

template_model.model = quartz.model['double_well']
template_model.initial = quartz.initial([[0.5]], [-2.5], math.pow(math.pi / 2.0, -0.25), phase_factor=[2.0])
template_model.mass = [1836]
template_model.method = 'cwa_smd_opt'
template_model.grid = [50,50]
template_model.ranges = [[-10,10],[-10,10]]
template_model.dt = 10.0
template_model.steps = 1000
template_model.scaling = [4.0, 4.0]
template_model.tol = 0.001
template_model.gradient_tol = 0.0001
template_model.max_iter = 10000
template_model.grade = 4
template_model.printer = generic_printer

dir = "round_3/"


filename = "grade_scaling_tol/"
if not os.path.exists(dir + filename):
    os.makedirs(dir + filename)
for i in range(3,11):
    for j in range(1,11):
        for k in range(7):
            model = copy.deepcopy(template_model)
            if not os.path.exists(dir + filename + str(i)):
                os.makedirs(dir + filename + str(i))

            model.grade = i
            model.scaling = [j / 2.0, j / 2.0]
            model.tol = math.pow(10, -k)
            model.gradient_tol = model.tol * 10.0
            model.json = "log.json"
            model.printer = generic_printer

            model.to_json(dir + filename + str(i) + '/input.json')

        ###### expectation ######
            model.printer = expectation_printer
            model.json = "exp_log.json"
            model.to_json(dir + filename + str(i) + '/exp_input.json')

            with open(dir + filename + str(i) + "_" + str(j) + "_" + str(k) + "/PBS" , 'w') as pbsfile :
                pbs = jobsys.pbs("quartz.exe", "input.json", "wenchang", "SMD",
                                 env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"")
                pbs.time = "120:00:00"
                pbs.tasks_per_node = 4
                pbs.save_output = True
                pbsfile.write(pbs.to_string())
                total_input.write("cd " + cwd + '/' + dir + filename + str(i)  + "_" str(j) + "_" + str(k) + " && " + "qsub " + "PBS" + "\n")

            with open(dir + filename + str(i)  + "_" + str(j) + "_" + str(k) + "/PBS_exp", 'w') as pbsfile:
                pbs = jobsys.pbs("quartz.exe", "exp_input.json", "wenchang", "SMD",
                                 env="alias quartz.exe=\"/public/home/ugrs1_LJ/Walter/Quartz/build/bin/quartz.exe\"\n")
                pbs.time = "120:00:00"
                pbs.tasks_per_node = 4
                pbs.save_output = True
                pbsfile.write(pbs.to_string())
                total_input.write("cd " + cwd + '/' + dir + filename + str(i) + "_" + str(j) + "_" + str(k) + " && " + "qsub " + "PBS_exp" + "\n" )


total_input.close()