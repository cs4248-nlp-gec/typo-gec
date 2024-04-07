#!/bin/bash

# A bash script for running the M2 scorer on multiple files. Modify when needed.

typomodel="gector+norvig"
typotype=("light" "medium" "heavy")
modeltype=("norvig" "norvig+gector")

for typo in ${typotype[@]}; do
    m2file="./project/m2_annotations/ABCN.dev.gold.bea19_original_typo_$typo.txt"
    for model in ${modeltype[@]}; do
        echo -e "Running M2 on typo type ${typo} and model ${model}"
        filename="./project/predictions/$typomodel/ABCN_original_typo_${typo}_$model.txt"
        ./m2scorer/m2scorer $filename $m2file
    done
done