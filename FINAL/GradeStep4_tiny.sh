#!/bin/bash
#Run outputs through Tiny. Prune the expected outputs to remove everything after Statistics.


#Use the inputs to run through compiler with Micro. Recieve outputs.
INPUTS=Step4/inputs/*
mkdir Step4/usertest
mkdir Step4/usertest/inputs
mkdir Step4/usertest/outputs
for i in $INPUTS
	do
		filename=${i%.*}
		name=${filename##*/}
		output="${name}.out"
		./Micro $i > Step4/usertest/inputs/$output
	done

#Get results from tiny.
TINYIN=Step4/usertest/inputs/*
for j in $TINYIN
  do
		filename=${j%.*}
		tinyname=${filename##*/}
    output="${tinyname}.out"
    if [ "$tinyname" == 'step4_testcase' ] ; then
      echo "Please enter parameters for $output"
    fi
    if [ "$tinyname" == 'test_mult' ] ; then
      echo "Please enter parameters for $output"
    fi
    ./tiny $j > Step4/usertest/outputs/$output

  done
# Find expected outputs from given inputs
mkdir Step4/tinyout
EXPECTIN=Step4/outputs/*
for k in $EXPECTIN
  do
		filename=${k%.*}
		name=${filename##*/}
    output="${name}.out"
    if [ "$name" == 'step4_testcase' ] ; then
      echo "Please enter parameters for $output"
    fi
    if [ "$name" == 'test_mult' ] ; then
      echo "Please enter parameters for this $output"
    fi
    ./tiny $k > Step4/tinyout/$output
  done
# Remove all statistics.
FINAL1=Step4/tinyout/*
FINAL2=Step4/usertest/outputs/*
for file in $FINAL1
  do
    while IFS= read -r line
    do
      pat="STATISTICS"
      if [[ $line =~ $pat ]]; then
        break
      fi
      echo "$line" >> tempfile.txt
    done <"$file"
    cat tempfile.txt > $file
    rm tempfile.txt
  cat $file
done

for file in $FINAL2
  do
    while IFS= read -r line
    do
      pat="STATISTICS"
      if [[ $line =~ $pat ]]; then
        break
      fi
      echo "$line" >> tempfile.txt
    done <"$file"
    cat tempfile.txt > $file
    rm tempfile.txt
done

#Run the diff between sets of files. 
for file in $FINAL1
do
  filename=${j%.*}
  tinyname=${filename##*/}
  output="${tinyname}.out"
  diff -b -s Step4/tinyout/$output Step4/usertest/outputs/$output
done

