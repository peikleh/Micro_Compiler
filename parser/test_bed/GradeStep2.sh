#!/bin/bash

INPUTS=Step2/inputs/*
mkdir Step2/usertest
for i in $INPUTS
	do
		filename=${i%.*}
		name=${filename##*/}
		echo "Testing input file $i"
		output="${name}Test.out"
		outtest="${name}.out"
		./Micro $i > Step2/usertest/$output
		diff -b -s Step2/usertest/$output Step2/outputs/$outtest
	done
