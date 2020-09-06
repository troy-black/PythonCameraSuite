import subprocess


class Process:
    def __init__(self, cmd, *args):
        self.cmd = cmd
        self.args = args
        self.stdout = None
        self.stderr = None
        self.exception = None
        self.returncode = None

    def run(self):
        try:
            process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            self.stdout, self.stderr = process.communicate()
            self.returncode = process.returncode
        except Exception as exception:
            self.exception = exception
