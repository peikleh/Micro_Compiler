#!/bin/bash

INPUTS=Step3/inputs/*
mkdir Step3/usertest
for i in $INPUTS
	do
		filename=${i%.*}
		name=${filename##*/}
		echo "Testing input file $i"
		output="${name}Test.out"
		outtest="${name}.out"
		./Micro $i > Step3/usertest/$output
		diff -b -s Step3/usertest/$output Step3/outputs/$outtest
	done
