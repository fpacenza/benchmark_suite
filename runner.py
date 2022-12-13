import subprocess
import os
import typer
from rich.console import Console
console=Console()

executables = [
    # exe-path; exe_name (to filter output in experiments)
    ("./bin/clingo","clingo5.6"),
    ("./bin/dlv2-float","dlv2-float"),
]

benchmarks = [
    "SystemSynthesis",
    "solar-30nodes",
]


def main(no_output: bool=False, out_dir: str="out_dir", clean: bool=True, only_clean: bool=False, timeout: int=3, taskset: int=-1, sender: bool=True, debug: bool=False):
    if only_clean:
        cmd = "./run.sh -r " + str(out_dir)  
        os.system(cmd)
        console.log("[magenta]All files cleaned and script terminated![/magenta]")
        exit(1)

    if clean:
        cmd = "./run.sh -r " + str(out_dir)  
        os.system(cmd)

    optional_arguments = ""
    if timeout != -1:
        optional_arguments = optional_arguments + "--timeout " + str(timeout) + " "
    if taskset != -1:
        optional_arguments = optional_arguments + "--taskset " + str(taskset) + " "
    if no_output:
        optional_arguments = optional_arguments + "--no-output "

    optional_arguments = optional_arguments + " "

    for tuple in executables:
        exe=tuple[0]
        exe_name=tuple[1]
        for benchmark in benchmarks:
            cmd = "./run.sh " + str(optional_arguments) + str(exe) + " problems/" + str(benchmark) + " problems/" + str(benchmark) + "/instances_test.list " + str(out_dir) + " " + str(benchmark) + " " + str(exe_name)
            console.log("Executing Problem [magenta]%s[/magenta] with solver [red]%s[/red]" % (str(benchmark), str(exe_name)))
            if debug:
                console.log("Command to be executed %s" % str(cmd))
            os.system(cmd)

    if sender:
        cmd="./run.sh -s " + str(out_dir)
        os.system(cmd)



if __name__ == "__main__":
    typer.run(main)
