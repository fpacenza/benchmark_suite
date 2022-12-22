import os
import typer
from rich.console import Console
console=Console()

executables = [
    # exe-path; exe_name (to filter output in experiments)
#    ("./bin/dlv2-double --mode=idlv --float-precision=12","grounding","instances.float.list","encoding.float.asp"),
#    ("./bin/dlv2-double --float-precision=12","dlv2-double","instances.float.list","encoding.float.asp"),
#    ("./bin/idlv_double_wasp.sh","idlv-double+wasp","instances.float.list","encoding.float.asp"),
#    ("./bin/idlv_double_clasp.sh","idlv-double+clasp","instances.float.list","encoding.float.asp"),
#    ("./bin/idlv_double_precision_clasp.sh","idlv-double-precision+clasp","instances.float.list","encoding.float.asp"),
    ("./bin/dlv2-double-python3/dlv2","dlv2-external","instances.idlv.list","encoding.idlv.asp"),
#    ("./bin/clingo-5.4.0","clingo-5-4-0","instances.gringo.list","encoding.gringo.asp"),
]

benchmarks = [
    "CityBench/Q1_100",
    "CityBench/Q2_100",
    "CityBench/Q3_100",
    "CityBench/Q5_100",
    "CityBench/Q6_8",
    "CityBench/Q7_8",
    "CityBench/Q8_8",
    "CityBench/Q9_8",
    "CityBench/Q13_100",
]



def main(output: bool=True, out_dir: str="out_dir_citybench2", clean: bool=False, only_clean: bool=False, timeout: int=600, taskset: int=0, result: bool=True, send_mail: str="pacenza@mat.unical.it zangari@mat.unical.it", debug: bool=False):
    if only_clean:
        cmd = "./run.sh --only-clean " + str(out_dir)  
        os.system(cmd)
        console.log("[magenta]All files have been cleaned and the script has been terminated![/magenta]")
        exit(1)

    if clean:
        cmd = "./run.sh --only-clean " + str(out_dir)  
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
        cmd="./run.sh --send " + str(out_dir)
        if send_mail != "":
            cmd = cmd + " \"" + str(send_mail) +"\""
            console.log(cmd)
        os.system(cmd)



if __name__ == "__main__":
    typer.run(main)
