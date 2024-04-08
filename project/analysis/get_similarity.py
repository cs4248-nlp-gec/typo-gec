import os
import shutil
import spacy
from nltk.translate.gleu_score import *

"""
We want to:
1. Find the GLEU score of 
2. Find the similarity 

Limitations: 
Both GLEU and similarity may not be best suited for this task of typo correction, because 1. GLEU is designed for machine translation,
while our text is somewhat "translation", there may be better metrics that fit.
for both it may not handle typo datasets well.
corpus_gleu may be bad as they put more weightage to longer sentences.

My opinion:
I think that spacy similarity is better because it understands the contextual meaning of the sentences generated. They may be slightly different in grammar
but it will capture the meanings better compared to GLEU which does an ngram kind of comparision. If one word typo / wrong the other ngrams may be wrong?
"""

abc_baseline_path = "../data/corrected/baseline/ABC.train.gold.bea19_corrected.txt"
abcn_baseline_path = "../data/corrected/baseline/ABCN.dev.gold.bea19_corrected.txt"
abc_long_path = "../data/corrected/corrected_long_sentence/ABC.train.gold.bea19_corrected_long_sentence.txt"
abcn_long_path = "../data/corrected/corrected_long_sentence/ABCN.dev.gold.bea19_corrected_long_sentence.txt"
abc_short_path = "../data/corrected/corrected_short_sentence/ABC.train.gold.bea19_corrected_short_sentence.txt"
abcn_short_path = "../data/corrected/corrected_short_sentence/ABCN.dev.gold.bea19_corrected_short_sentence.txt"

cor_data_path_dict = {
    "ABC_light": abc_baseline_path,
    "ABC_medium": abc_baseline_path,
    "ABC_heavy": abc_baseline_path,
    "ABC_long": abc_long_path,
    "ABC_short": abc_short_path,
    "ABCN_light": abcn_baseline_path,
    "ABCN_medium": abcn_baseline_path,
    "ABCN_heavy": abcn_baseline_path,
    "ABCN_long": abcn_long_path,
    "ABCN_short": abcn_short_path,
}


def process_file(src_file_path, dest_file_path, reference_file_path):
    # Initialize variables to track GLEU scores
    gleu_scores = []
    references = []
    candidates = []
    with open(src_file_path, 'r', encoding='utf-8') as src, open(dest_file_path, 'w', encoding='utf-8') as dest, open(
            reference_file_path, 'r', encoding='utf-8') as ref:
        for src_line, ref_line in zip(src, ref):
            # Calculate GLEU score for the line
            score = sentence_gleu([ref_line.strip().split()], src_line.strip().split())
            gleu_scores.append(score)
            references.append([ref_line.strip().split()])
            candidates.append(src_line.strip().split())

            # Write the GLEU score for this line to the destination file
            dest.write(f"{score}\n")

        # Calculate min, max, and average GLEU scores
        min_score = min(gleu_scores)
        max_score = max(gleu_scores)
        avg_score = sum(gleu_scores) / len(gleu_scores)

        # Write these statistics to the destination file
        dest.write(f"Min Sentence GLEU Score: {min_score}\n")
        dest.write(f"Max Sentence GLEU Score: {max_score}\n")
        dest.write(f"Average Sentence GLEU Score: {avg_score}\n")
        dest.write(f"Corpus Sentence GLEU Score: {score}\n")

def gleu_copy_structure_and_process_files(src_directory, dest_directory, keywords, cor_data_path_dict):
    # Ensure the destination directory exists
    os.makedirs(dest_directory, exist_ok=True)

    # Walk through the source directory
    for root, dirs, files in os.walk(src_directory):
        for dir in dirs:
            src_path = os.path.join(root, dir)
            dest_path = "./gleu_scores/" +  "/".join(src_path.split("/")[2:])
            os.makedirs(dest_path, exist_ok=True)

        for file in files:
            if any(keyword in file for keyword in keywords) and "results" not in file and "word" not in file:
                # Determine the reference file based on the file's naming convention
                for key, path in cor_data_path_dict.items():
                    if all(kw in file for kw in key.split('_')):
                        reference_file_path = path # abcn later in the dict so will match abcn :)

                src_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(root.replace("../predictions", "./gleu_scores"), file.replace('.txt', '_gleu_score.txt'))

                # Process the file to calculate GLEU scores
                process_file(src_file_path, dest_file_path, reference_file_path)
                print(f"Processed {src_file_path}, results in {dest_file_path}, ref {reference_file_path}")


src_directory = '../predictions'
dest_directory = './gleu_scores'
keywords = ["light", "medium", "heavy", "long", "short"]

gleu_copy_structure_and_process_files(src_directory, dest_directory, keywords, cor_data_path_dict)

