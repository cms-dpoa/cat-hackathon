#!/bin/bash

# Get the input variable from the command line
input_var=$1
output_var=$2

input=$(cat ${input_var})
output=$(echo "Hello $input!")
echo $output >> ${output_var}