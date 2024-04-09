import os
import matplotlib.pyplot as plt
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

abcn_baseline_path = "../data/corrected/baseline/ABCN.dev.gold.bea19_corrected.txt"
abcn_long_path = "../data/corrected/corrected_long_sentence/ABCN.dev.gold.bea19_corrected_long_sentence.txt"
abcn_short_path = "../data/corrected/corrected_short_sentence/ABCN.dev.gold.bea19_corrected_short_sentence.txt"


def process_file(src_file_path, dest_file_path, reference_file_path):
    gleu_scores = []
    references = []
    candidates = []
    with open(src_file_path, 'r',
              encoding='utf-8') as src, open(dest_file_path,
                                             'w',
                                             encoding='utf-8') as dest, open(
                                                 reference_file_path,
                                                 'r',
                                                 encoding='utf-8') as ref:
        for src_line, ref_line in zip(src, ref):
            score = sentence_gleu([ref_line.strip().split()],
                                  src_line.strip().split())
            gleu_scores.append(score)
            references.append([ref_line.strip().split()])
            candidates.append(src_line.strip().split())
            dest.write(f"GLEU: {score}\n")

        # Calculate min, max, and average GLEU scores
        min_score = min(gleu_scores)
        max_score = max(gleu_scores)
        avg_score = sum(gleu_scores) / len(gleu_scores)
        corpus_score = corpus_gleu(references, candidates)

        # Write these statistics to the destination file
        dest.write(f"Min Sentence GLEU Score: {min_score}\n")
        dest.write(f"Max Sentence GLEU Score: {max_score}\n")
        dest.write(f"Average Sentence GLEU Score: {avg_score}\n")
        dest.write(f"Corpus Sentence GLEU Score: {corpus_score}\n")

    with open("./gleu_scores/total_results.txt",
              "a") as file:  # store total results
        file.write(
            f"{src_file_path}: Min: {min_score}, Max: {max_score}, Avg: {avg_score}, Corpus score: {corpus_score}\n"
        )
    return avg_score, corpus_score


def gleu_copy_structure_and_process_files(src_directory, dest_directory,
                                          keywords):
    os.makedirs(dest_directory, exist_ok=True)
    try:
        os.remove("./gleu_scores/total_results.txt")
    except:
        pass
    directory_scores = {}

    immediate_subdirs = [
        d for d in os.listdir(src_directory)
        if os.path.isdir(os.path.join(src_directory, d))
    ]

    for subdir in immediate_subdirs:
        second_level_dir = os.path.join(src_directory, subdir)
        dest_subdir = os.path.join(dest_directory, subdir)
        os.makedirs(dest_subdir, exist_ok=True)
        scores = []

        files = [
            f for f in os.listdir(second_level_dir)
            if os.path.isfile(os.path.join(second_level_dir, f))
        ]
        for file in files:
            if any(keyword in file for keyword in keywords):
                if "long" in file:
                    reference_file_path = abcn_long_path
                elif "short" in file:
                    reference_file_path = abcn_short_path
                else:
                    reference_file_path = abcn_baseline_path

                src_file_path = os.path.join(second_level_dir, file)
                dest_file_path = os.path.join(
                    dest_subdir, file.replace('.txt', '_gleu_score.txt'))

                avg_score, corpus_score = process_file(src_file_path,
                                                       dest_file_path,
                                                       reference_file_path)
                scores.append(
                    (file, avg_score, corpus_score, reference_file_path))
                print(
                    f"Processed {src_file_path}, results in {dest_file_path}, ref {reference_file_path}"
                )

        summary_path = os.path.join(dest_subdir, "summary_results.txt")
        with open(summary_path, 'w', encoding='utf-8') as summary_file:
            for file, avg_score, corpus_score in scores:
                summary_file.write(
                    f"{file}: Avg: {avg_score}, Corpus Score: {corpus_score}\n"
                )

        directory_scores[dest_subdir] = scores

    return directory_scores


def sorting_key(filename):
    order = ['light', 'medium', 'heavy', 'short', 'long']
    x = 0
    if "+gector" in filename:
        x += 0.5
    for index, category in enumerate(order):
        if category in filename:
            return index + x
    return len(order)


def plot_directory_scores(directory_scores):
    for directory, scores in directory_scores.items():
        sorted_scores = sorted(scores, key=lambda x: sorting_key(x[0]))
        files = [score[0] for score in sorted_scores]
        avg_sentence_scores = [score[1] for score in sorted_scores]
        corpus_scores = [score[2] for score in sorted_scores]

        plt.figure(figsize=(10, 6))
        plt.plot(files,
                 avg_sentence_scores,
                 label='Avg Sentence GLEU',
                 marker='o')
        plt.plot(files, corpus_scores, label='Corpus GLEU', marker='x')

        plt.title(f"Sorted GLEU Scores in {os.path.basename(directory)}")
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Files")
        plt.ylabel("Scores")
        plt.legend()
        plt.tight_layout()
        plot_path = os.path.join(directory, "gleu_scores_plot_sorted.png")
        plt.savefig(plot_path)
        plt.close()


src_directory = '../predictions'
dest_directory = './gleu_scores'
keywords = ["light", "medium", "heavy", "long", "short"]

dir_scores = gleu_copy_structure_and_process_files(src_directory,
                                                   dest_directory, keywords)
plot_directory_scores(dir_scores)
