import subprocess
import os
import typer
from rich.console import Console
console=Console()

benchmarks = [
    "SystemSynthesis",
    "solar-30nodes",
]

def main(exe: str, exe_name: str, out_dir: str="out_dir", clean: bool=True, timeout: int=-1, taskset: int=-1, sender: bool=True, debug: bool=False):

    if clean:
        cmd = "./run.sh -r " + str(out_dir)  
        os.system(cmd)

    optional_arguments = ""
    if timeout != -1:
        optional_arguments = optional_arguments + "--timeout " + str(timeout) + " "
    if taskset != -1:
        optional_arguments = optional_arguments + "--taskset " + str(taskset) + " "

    optional_arguments = optional_arguments + " "
    for benchmark in benchmarks:
        cmd = "./run.sh " + str(optional_arguments) + str(exe) + " problems/" + str(benchmark) + " problems/" + str(benchmark) + "/instances_test.list " + str(out_dir) + " " + str(benchmark) + " " + str(exe_name)
        console.log("Executing Problem %s" % str(benchmark))
        if debug:
            console.log("Command to be executed %s" % str(cmd))
        os.system(cmd)

    if sender:
        cmd="./run.sh -s " + str(out_dir)
        os.system(cmd)



if __name__ == "__main__":
    typer.run(main)
