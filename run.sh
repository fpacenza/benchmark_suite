#!/bin/bash

# Verifichiamo se l'opzione -c (clean) è stata passata come argomento
if [[ $@ == *"-c"* ]]; then
  shift
  rm -rf *.out *.csv out_dir/.* 1> /dev/null 2>/dev/null
  echo "Rimozione dei file temporanei e dei vecchi esperimenti avvenuta con successo!"
fi

if [[ $@ == *"-r"* ]]; then
  shift
  rm -rf *.out *.csv out_dir/.* 1> /dev/null 2>/dev/null
  echo "Rimozione dei file temporanei e dei vecchi esperimenti avvenuta con successo!"
  echo "USCITA!"
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


# Controlla se sono stati specificati tutti gli argomenti
if [ $# -ne 5 ]; then
  echo "Errore: specificare l'eseguibile, la cartella e il file con le istanze del problema"
  exit 1
fi

# Assegna i valori degli argomenti alle variabili
exe=$1
folder=$2
instances_file=$3
problem_name=$4
exe_name=$5
encoding="encoding.asp"
today=$(date "+%Y-%M-%d_%H.%M.%S")

# Crea il file CSV per salvare i risultati
echo "PROBLEM,INSTANCE,EXECUTABLE,STATUS,TIME,MEMORY,EXIT_CODE" > results_$today.csv

# Crea la cartella per salvare l'output
mkdir -p out_dir


counter=0
# Execute perf command over each instance of the problem 
while read -r instance; do
  filled_counter=$(seq -f "%05g" $counter $counter)
  # Run di executable
  now=$(date "+%Y-%M-%d_%H-%M-%S") 
  out_instance_path="out_dir/."$now"_"$filled_counter"_"$instance"_OUT_"$exe_name
  err_instance_path="out_dir/."$now"_"$filled_counter"_"$instance"_ERR_"$exe_name
  # echo $exe $folder/$encoding $folder/$instance
  time_output=$(/usr/bin/time -v bash -c "$timeout perf stat -o perf.out $exe $folder/$encoding $folder/$instance 1> $out_instance_path 2> $err_instance_path" 2>&1)

  # echo $time_output
  if [ -s perf.out ]; then
    # If the process has not been killed, extract execution time from perf output
    time=$(grep "time elapsed" perf.out | awk '{print $1}' | sed 's/,/./')
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
  echo "$problem_name,$instance,$exe_name,$status,$time,$memory,$exit_code" >> results_$today.csv
  ((counter++))
done < "$instances_file"

# Remove temp files
rm perf.out