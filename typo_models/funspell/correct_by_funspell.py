import os
import funspell
from funspell import Funspell

fun_spell  = Funspell()

input_file_path = "ABCN.dev.gold.bea19_original_typo.txt" 
output_file_path = "ABCN_funspell_generated.txt"

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        corrected_line = fun_spell.correct(line.strip(), 3) + '\n'
        output_file.write(corrected_line)

print("Correction process completed. Corrected sentences saved to:", output_file_path)

