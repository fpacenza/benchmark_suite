import os
import typer
from rich.console import Console
console=Console()

executables = [
    # exe-path; exe_name (to filter output in experiments)
#    ("./bin/dlv2-double","dlv2-double","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/idlv_double_wasp.sh","idlv-double+wasp","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/idlv_double_clasp.sh","idlv-double+clasp","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/idlv_double_clasp_precision3.sh","idlv-double-precision3+clasp","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/dlv2-double --mode=idlv","dlv2-double-grounding","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/dlv2-double --mode=idlv --float-precision=0","dlv2-no-double-grounding","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/dlv2-double --float-precision=0","dlv2-no-double","instances.all.list","encoding.dlv2.asp"),

#    ("./bin/clingo-5.4.0","clingo-5-4-0","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/clingo-5.6.2","clingo-5-6-2","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/clingo-5.4.0 --mode=gringo","clingo-5-4-0-grounding","instances.all.list","encoding.dlv2.asp"),

#    ("./bin/dlv-2.1.1-linux-x86_64","dlv-2.1.1-linux-x86_64","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/DLV2.1.0-python3/build/release/dlv2","dlv2.1.0","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/DLV2.1.0-python3/build/release/dlv2 --mode=idlv","dlv2.1.0-grounding","instances.all.list","encoding.dlv2.asp"),

#    ("./bin/idlv_double_clasp540_precision4.sh","idlv-double-precision4+clasp5.4.0","instances.all.list","encoding.dlv2.asp"),
    ("./bin/idlv_double_clasp540_precision5.sh","idlv-double-precision5+clasp5.4.0","instances.all.list","encoding.dlv2.asp"),
#    ("./bin/idlv_double_wasp_precision0.sh","idlv-double-precision0+wasp","instances.all.list","encoding.dlv2.asp"),


]

benchmarks = [
    "SystemSynthesis",
]


def main(output: bool=True, out_dir: str="out_dir_system_synthesis_special2", clean: bool=True, only_clean: bool=False, timeout: int=600, taskset: int=8, result: bool=True, send_mail: str="pacenza@mat.unical.it zangari@mat.unical.it", debug: bool=False):
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
    if output==False:
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
