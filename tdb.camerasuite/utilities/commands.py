import subprocess


class Process:
    def __init__(self, cmd: list):
        self.cmd: list = cmd
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
