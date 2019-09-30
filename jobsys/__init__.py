class sbatch(object):
    def __init__(self,cmd,file,partition,job_name="SBATCH",flag="",env="",option=""):
        self.nodes = 1
        self.partition = partition
        self.job_name = job_name
        self.tasks_per_node = 1
        self.cpus_per_task = 1
        self.time = "1-00:00:00"
        self.mail = False
        self.mail_type = 'FAIL'
        self.env = env
        self.cmd = cmd
        self.flag = flag
        self.file = file
        self.option = option
        self.save_output = False
        self.post_process = ''
        self.script = ''

    def to_string(self):
        script = "#!/bin/sh" + '\n'
        script += '#SBATCH --job-name=' + self.job_name + '\n'
        script += '#SBATCH --partition=' + self.partition + '\n'
        script += '#SBATCH --nodes=' + str(self.nodes) + '\n'
        script += '#SBATCH --tasks-per-node=' + str(self.tasks_per_node) + '\n'
        script += '#SBATCH --cpus-per-task' + str(self.cpus_per_task) + '\n'
        script += '#SBATCH --time=' + self.time + '\n'
        if self.mail:
            script += '#SBATCH --mail-type=' + self.mail_type + '\n'
        script += '\n'
        script += 'cd $SLURM_SUBMIT_DIR' + '\n'
        script += '\n'
        script += self.env + '\n'
        script += '\n'
        script += self.cmd + ' '
        if self.flag != '':
            script += self.flag + ' '
        script += self.file + ' '
        if self.option != '':
            script += self.option + ' '
        if self.save_output:
            script += '>' + self.file + '.log'
        script += '\n'
        script += '\n'
        script += self.post_process

        self.script = script


class pbs(object):
    def __init__(self,cmd,file,partition,job_name="PBS",flag="",env="",option=""):
        self.nodes = 1
        self.partition = partition
        self.job_name = job_name
        self.tasks_per_node = 1
        self.cpus_per_task = 1
        self.time = "100:00:00"
        self.mail = False
        self.mail_type = 'e'
        self.env = env
        self.cmd = cmd
        self.flag = flag
        self.file = file
        self.option = option
        self.save_output = False
        self.post_process = ''
        self.script = ''

    def to_string(self):
        script = "#!/bin/sh" + '\n'
        script += '#PBS -N ' + self.job_name + '\n'
        script += '#PBS -l nodes=' + str(self.nodes) + ":ppn=" + str(self.tasks_per_node) + '\n'
        script += '#PBS -q ' + str(self.partition) + '\n'
        script += '#PBS -l walltime=' + self.time + '\n'
        if self.mail:
            script += '#PBS -m ' + self.mail_type + '\n'
        script += 'nprocs= `cat $PBS_NODEFILE | wc -l`' + '\n'
        script += '\n'
        script += 'cd $PBS_O_WORKDIR' + '\n'
        script += '\n'
        script += self.env + '\n'
        script += '\n'
        script += self.cmd + ' '
        if self.flag != '':
            script += self.flag + ' '
        script += self.file + ' '
        if self.option != '':
            script += self.option + ' '
        if self.save_output:
            script += '>' + self.file + '.log'
        script += '\n'
        script += '\n'
        script += self.post_process

        self.script = script




