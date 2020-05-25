import json
import numpy as np
import re

model = {
    "harmonic": {"polynomial" : {
        "exponents": [[2]],
        "coefs": [0.5]
    }},
    "cubic_decay": {"polynomial" : {
      "exponents": [[2],[3]],
      "coefs": [0.5, 1.0/6.0]
    }},
    "anharmonic": {"polynomial" : {
        "exponents": [[2],[3],[4]],
        "coefs": [1,-0.1,0.1]
    }},
    "quartic": {"polynomial" : {
        "exponents": [[4]],
        "coefs": [0.25]
    }},
    "double_well": { "polynomial" : {
        "exponents": [[2],[4]],
        "coefs":[-0.0003, 0.000024]
    }}
}

def initial(covariance, mean, coef, phase_factor = None) :

    if phase_factor:
        return {
            "coef": coef,
            "covariance": covariance,
            "mean": mean,
            "phase_factor": phase_factor
        }
    return {
        "coef": coef,
        "covariance": covariance,
        "mean": mean
    }

class quartz(object):
    def __init__(self):
        self.model = model['harmonic']
        self.initial = initial([[1]], [1.0], 1.0)
        self.method = "cwa"
        self.mass = [1.0]
        self.grid = [30,30]
        self.ranges = [[-5,5],[-5,5]]
        self.steps = 1000
        self.dt = 0.01
        self.printer = {
            "type": "generic",
            "print_level": 2
        }
        self.grade = 2
        self.scaling = [1.0]
        self.tol = 1
        self.gradient_tol = 0.1
        self.max_iter = 100
        self.print_json = False
        self.json = "log.json"

    def to_map(self):
        if self.print_json:
            return {
                "method": self.method,
                "initial": self.initial,
                "potential": self.model,
                "mass": self.mass,
                "grid": self.grid,
                "range": self.ranges,
                "steps": self.steps,
                "dt": self.dt,
                "grade": self.grade,
                "scaling": self.scaling,
                "tol": self.tol,
                "gradient_tol" : self.gradient_tol,
                "max_iter" : self.max_iter,
                "printer": self.printer,
                "json": self.json
            }
        else:
            return {
                "method": self.method,
                "initial": self.initial,
                "potential": self.model,
                "mass": self.mass,
                "grid": self.grid,
                "range": self.ranges,
                "steps": self.steps,
                "dt": self.dt,
                "grade": self.grade,
                "scaling": self.scaling,
                "tol": self.tol,
                "gradient_tol": self.gradient_tol,
                "max_iter": self.max_iter,
                "printer": self.printer,
            }

    def to_json(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self.to_map(), fp)


class QuartzResult(object):
    def __init__(self, steps, timeline, data, labels, is_normal=False, time=-1):
        self.steps = [steps[0], steps[-1]]
        self.timeline = timeline
        self.data = data
        self.labels = labels
        self.is_normal = is_normal
        self.time = time


def parse_generic_quartz_result(result_str):

    data_block_match = re.compile(r"=+\n(?P<data>[\s\.\d\-]+)=+\n", re.MULTILINE)
    data_block = data_block_match.search(result_str).groupdict()['data']

    label_match = re.compile(r"\|[ ]*(?P<label>[a-zA-z]+)[ ]*")
    labels = [i.groupdict()['label'] for i in label_match.finditer(result_str)]
    del labels[0]
    del labels[0]

    data_block_lines = data_block.split("\n")
    data_block_lines.remove("")

    all_data = np.array(list(map(lambda x: list(map(float, x)), [i.split() for i in data_block_lines]))).transpose()

    steps = all_data[0]
    timeline = all_data[1]
    data = all_data[2:]

    time = -1
    is_normally_terminated = bool(re.search("Quartz terminated normally", result_str))
    if is_normally_terminated:
        time = re.search(r"Total time elapsed:[ ]+(?P<time>\S+)[ ]+s", result_str).groupdict()['time']
    return QuartzResult(steps, timeline, data, labels, is_normal=is_normally_terminated, time=time)

