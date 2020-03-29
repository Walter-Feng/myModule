import json

model = {
    "harmonic": {
        "exponents": [[2]],
        "coefs": [0.5]
    },
    "cubic_decay": {
      "exponents": [[2],[3]],
      "coefs": [0.5, 1.0/6.0]
    },
    "anharmonic": {
        "exponents": [[2],[3],[4]],
        "coefs": [1,-0.1,0.1]
    },
    "quartic": {
        "exponents": [[4]],
        "coefs": [0.25]
    },
    "double_well": {
        "exponents": [[2],[4]],
        "coefs":[-0.0003, 0.000024]
    }
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
                "printer": self.printer,
            }

    def to_json(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self.to_map(), fp)


