import os
import typer
from rich.console import Console
console=Console()

executables = [
    # exe-path; exe_name (to filter output in experiments); instance_list filename; encoding_name filename
    ("./bin/dlv2-double --mode=idlv --t","dlv2-double","instances.float.list","encoding.float.asp"),
    ("./bin/dlv2-double-python3/dlv2 --mode=idlv --t","dlv2-external","instances.idlv.quote.list","encoding.idlv.quote.asp"),
    ("./bin/clingo-5.4.0","clingo-5.4.0","instances.gringo.quote.list","encoding.gringo.quote.asp"),
]

benchmarks = [
    "maritime/q1",
    "maritime/q3",
]



def main(output: bool=True, out_dir: str="out_dir_maritime", clean: bool=True, only_clean: bool=False, timeout: int=600, taskset: int=4, result: bool=True, send_mail: str="pacenza@mat.unical.it zangari@mat.unical.it", debug: bool=False):
    if only_clean:
        cmd = "./run.sh -r " + str(out_dir)  
        os.system(cmd)
        console.log("[magenta]All files have been cleaned and the script has been terminated![/magenta]")
        exit(1)

    if clean:
        cmd = "./run.sh -r " + str(out_dir)  
        os.system(cmd)

    optional_arguments = ""
    if timeout != -1:
        optional_arguments = optional_arguments + "--timeout " + str(timeout) + " "
    if taskset != -1:
        optional_arguments = optional_arguments + "--taskset " + str(taskset) + " "
    if output == False:
        optional_arguments = optional_arguments + "--no-output "

    optional_arguments = optional_arguments + " "

    for tuple in executables:
        exe="\"" + tuple[0] + "\""
        exe_name=tuple[1]

        # Default value for instances.list and encoding.asp 
        instance_list="instances.list"
        encoding_name="encoding.asp"

        if len(tuple) > 2:
            instance_list=tuple[2]
            if len(tuple) > 3:
                encoding_name=tuple[3]

        for benchmark in benchmarks:
            cmd = "./run.sh " + str(optional_arguments) + str(exe) + " problems/" + str(benchmark) + " problems/" + str(benchmark) + "/" + str(instance_list) + " " + str(encoding_name) + " " + str(out_dir) + " " + str(benchmark) + " " + str(exe_name)
            console.log("Executing Problem [magenta]%s[/magenta] with solver [red]%s[/red]" % (str(benchmark), str(exe_name)))
            if debug:
                console.log("Command to be executed %s" % str(cmd))
            os.system(cmd)

    if result:
        cmd="./run.sh -s " + str(out_dir)
        if send_mail != "":
            cmd = cmd + " \"" + str(send_mail) +"\""
            console.log(cmd)
        os.system(cmd)



if __name__ == "__main__":
    typer.run(main)
