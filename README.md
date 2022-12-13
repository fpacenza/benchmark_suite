# ASP Benchmark Suite
A benchmark suite for ASP systems

# How to use
Tests must be executed starting from `runner.py` scripts which **MUST** be edited in order to specify some **default** parameters like:
 * **name of encoding file** (default: `encoding.asp`)
 * **path to problem folder**: (default: `problems`)
 * **list of** `benchmarks` **folders** 

## How to run
    python3 runner.py "./bin/executable" solver_name --out-dir="out_dir" --clean --timeout=3 --taskset=8 --debug