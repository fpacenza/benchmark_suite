#!/bin/bash

today=$(date "+%Y-%M-%d_%H.%M.%S.%N")
out_dir="out_dir"
head_string="PROBLEM,INSTANCE,EXECUTABLE,STATUS,TIME,MEMORY,EXIT_CODE"

# Check if the options are in the argv array
if [[ $@ == *"-s"* ]]; then
  shift
  out_dir=$1
  shift
  if [ ! -d "./$out_dir" ]; then
    echo "Directory $out_dir does not exists!"
  else
    echo "PROBLEM,INSTANCE,EXECUTABLE,STATUS,TIME,MEMORY,EXIT_CODE" > results_$today.csv
    cat $out_dir/*.csv | grep -v $head_string >> results_$today.csv

    if [ -z "$1" ]; then
      echo "All files sent"    
    else
      echo "NUMA04 ASP Benchmarks Complete" | mutt -s "NUMA04 ASP Benchmarks Complete" $1 -a results_$today.csv
      echo "All files sent"
    fi
  fi
  exit 1
fi

if [[ $@ == *"-c"* ]]; then
  shift
  if [ -z "$1" ]; then
    echo "Using default \"out_dir\""
  else
    out_dir=$1
    shift
  fi
  rm -rf *.out *.csv $out_dir 1> /dev/null 2>/dev/null
  echo "Temp files removed correctly!"
fi

if [[ $@ == *"-r"* ]]; then
  shift
  if [ -z "$1" ]; then
    echo "Using default \"out_dir\""
  else
    out_dir=$1
  fi
  rm -rf *.out *.csv $out_dir 1> /dev/null 2>/dev/null
  echo "Temp files removed correctly!"
#  echo "USCITA!"
  exit 1
fi

timeout=""
if [[ $@ == *"--timeout"* ]]; then
  shift
  timer=$1
  shift
  timeout="timeout $timer"
fi

memory_limit=""
if [[ $@ == *"--memory-limit"* ]]; then
  shift
  memory_limit=$1
  shift
fi

taskset=""
if [[ $@ == *"--taskset"* ]]; then
  shift
  taskset="taskset -c $1"
  shift
fi

output_redirect=""
if [[ $@ == *"--no-output"* ]]; then
  shift
  output_redirect="/dev/null"
fi


# Controlla se sono stati specificati tutti gli argomenti
if [ $# -ne 7 ]; then
  echo "Errore: specificare l'eseguibile, la cartella e il file con le istanze del problema"
  exit 1
fi

# Assegna i valori degli argomenti alle variabili
exe=$1
folder=$2
instances_file=$3
encoding=$4
out_dir=$5
problem_name=$6
exe_name=$7


# Crea la cartella per salvare l'output
mkdir -p $out_dir

# Crea il file CSV per salvare i risultati
echo $head_string > $out_dir/results_$today.csv



counter=0
# Execute perf command over each instance of the problem 
while read -r instance; do
  filled_counter=$(seq -f "%05g" $counter $counter)
  # Run di executable
  now=$(date "+%Y-%M-%d_%H-%M-%S-%N") 

  # Split string by space " " and save splitted pieces in array
  my_array=($(echo $instance | cut -d " " -f 1-))

  # For loop Cicloon array to add path before each instance pieces
  final_instance_path=""
  for i in "${my_array[@]}"; do
      final_instance_path=$final_instance_path" $folder/$i"
  done

  instance_name=$(echo $final_instance_path | rev | cut -d "/" -f 1 | rev)
  if [ -z "$output_redirect" ]; then
    out_instance_path="$out_dir/."$now"_"$filled_counter"_"$instance_name"_OUT_"$exe_name
  else
    out_instance_path="$output_redirect"
  fi
  err_instance_path="$out_dir/."$now"_"$filled_counter"_"$instance_name"_ERR_"$exe_name
  perf_out=$out_dir"/perf_"$now"_"$filled_counter"_"$instance_name"_"$exe_name".out"
  #echo "#################" $perf_out "#################"
  #echo "/usr/bin/time -v bash -c \"$timeout $taskset perf stat -o $perf_out $exe $folder/$encoding $final_instance_path 1> $out_instance_path 2> $err_instance_path\" 2>&1"
  time_output=$(/usr/bin/time -v bash -c "$timeout $taskset perf stat -o $perf_out $exe $folder/$encoding $final_instance_path 1> $out_instance_path 2> $err_instance_path" 2>&1)

  # echo $time_output
  if [ -s $perf_out ]; then
    # If the process has not been killed, extract execution time from perf output
    time=$(grep "time elapsed" $perf_out | awk '{print $1}' | sed 's/,/./')
    status="complete"
  else
    # else extract execution time from /usr/bin/time -v
    elapsed_time=$(echo $time_output | grep -oP 'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([0-9]+):([0-9]+)\.([0-9]+)' | awk '{print $8 $9 $10}' | sed 's/,/./')
    # echo $elapsed_time
    # Extract and convert minutes, seconds and milliseconds in milliseconds
    minutes=$(echo $elapsed_time | cut -d: -f1)
    seconds=$(echo $elapsed_time | cut -d: -f2 | cut -d. -f1)
    milliseconds=$(echo $elapsed_time | cut -d: -f2 | cut -d. -f2)

    time=$((60000 * minutes + 1000 * seconds + milliseconds))
    status="killed"
  fi
  # Extract used memory from /usr/bin/time -v command
  memory=$(echo $time_output | grep -oP 'Maximum resident set size \(kbytes\): ([0-9]+)' | awk '{print $6}' | sed 's/,/./')

  # Get the exit code
  exit_code=$(echo $time_output | grep -oP 'Exit status: ([0-9]+)' | awk '{print $3}')

  # Save the dat in a CSV file
  echo "$problem_name,$instance_name,$exe_name,$status,$time,$memory,$exit_code" >> $out_dir/results_$today.csv
  ((counter++))

  sleep 0.1

  # Remove temp files
  rm $perf_out

done < "$instances_file"

