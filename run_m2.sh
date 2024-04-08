#!/bin/bash

# A bash script for running the M2 scorer on multiple files. Modify when needed.

typomodel="gector+norvig"
typotype=("long_sentence" "short_sentence")
modeltype=("norvig" "norvig+gector")

for typo in ${typotype[@]}; do
    m2file="./project/m2_annotations/ABCN.dev.gold.bea19_original_typo_$typo.txt"
    for model in ${modeltype[@]}; do
        echo -e "Running M2 on typo type ${typo} and model ${model}"
        filename="./project/predictions/$typomodel/ABCN_original_typo_${typo}_$model"
        ./m2scorer/m2scorer "$filename.txt" $m2file > "${filename}_results.txt" 
    done
done