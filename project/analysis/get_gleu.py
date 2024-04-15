import os
from collections import defaultdict
import matplotlib
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
models_ignored=["norvig", "bart", "funspell", "gectorBERT", "gectorBERT+gectorbase", "gectorRoBERTa"]

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

        avg_score = sum(gleu_scores) / len(gleu_scores)
    return avg_score


def gleu_copy_structure_and_process_files(src_directory, dest_directory,
                                          keywords):
    os.makedirs(dest_directory, exist_ok=True)
    directory_scores = {}
    topic_scores = defaultdict(list)

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
                reference_file_path = abcn_baseline_path
                if "long" in file:
                    reference_file_path = abcn_long_path
                    topic = "long"
                elif "short" in file:
                    reference_file_path = abcn_short_path
                    topic = "short"
                elif "light" in file:
                    topic = "light"
                elif "heavy" in file:
                    topic = "heavy"
                else:
                    topic = "medium"

                src_file_path = os.path.join(second_level_dir, file)
                dest_file_path = os.path.join(
                    dest_subdir, file.replace('.txt', '_gleu_score.txt'))
                avg_score = process_file(src_file_path,
                                                       dest_file_path,
                                                       reference_file_path)
                name = file[:-4]
                model_name = "".join(name.split("_")[1:])
                if model_name in models_ignored:
                    continue
                scores.append((name, avg_score))
                print(
                    f"Processed {src_file_path}, results in {dest_file_path}, ref {reference_file_path}"
                )
                topic_scores[topic].append(
                    (model_name, avg_score))

        directory_scores[dest_subdir] = scores

    return directory_scores, topic_scores


def sorting_key(filename):
    order = ['light', 'medium', 'heavy', 'short', 'long']
    x = 0
    if "+gector" in filename:
        x += 0.5
    for index, category in enumerate(order):
        if category in filename:
            return index + x
    return len(order)



src_directory = '../predictions'
dest_directory = './gleu_scores'
keywords = ["light", "medium", "heavy", "long", "short"]


def plot_combined_gleu_scores(topic_scores):
    # Aggregate scores for each model across all topics
    model_scores = {}
    for topic, scores in topic_scores.items():
        for model, score in scores:
            if model not in model_scores:
                model_scores[model] = {}
            model_scores[model][topic] = score

    # Prepare data for plotting
    models = sorted(model_scores.keys())
    data_for_plotting = {model: [] for model in models}
    all_scores = []

    for model, scores_by_topic in model_scores.items():
        for topic in ["light", "medium", "heavy", "short", "long"]:
            score = scores_by_topic.get(topic, 0)  # Use 0 if no score for topic
            data_for_plotting[model].append(score)
            all_scores.append(score)

    # Compute the overall average score
    overall_avg_score = sum(all_scores) / len(all_scores)

    # Set up the plotting area
    plt.figure(figsize=(14, 8))
    color_map = {"light": "mediumseagreen", "medium": "orange", "heavy": "red", "short": "mediumturquoise", "long": "rebeccapurple"}
    topics = ["light", "medium", "heavy", "short", "long"]
    n = len(models)
    bar_width = 0.15

    plt.ylim(0.2, 1)

    # Create the bar chart
    for i, topic in enumerate(topics):
        scores = [data_for_plotting[model][i] for model in models]
        plt.bar([x + i * bar_width for x in range(n)], scores, width=bar_width, label=f'{topic.capitalize()} GLEU', color=color_map[topic])

    # Add model names to x-axis
    model_labels = []
    for model in models:
        if "+gector" in model:
            model_labels.append(f"{model.split('+')[0]}\n+gector")
        else:
            model_labels.append(model)
    plt.xticks([x + 2 * bar_width for x in range(n)], model_labels)

    # Draw horizontal line for the overall average
    plt.axhline(y=overall_avg_score, color='blue', linestyle='--', label='Overall Avg GLEU')

    # Add title and labels
    plt.title("GLEU Scores by Model and Topic")
    plt.xlabel("Models")
    plt.ylabel("Average Sentence GLEU Scores")

    # Show legend
    plt.legend()

    # Layout adjustment and display plot
    plt.tight_layout()
    plt.savefig(f"./gleu_scores/total_scores_plot.pdf", format="pdf")
    plt.savefig(f"./gleu_scores/total_scores_plot.png")
    plt.savefig(f"./gleu_scores/total_scores_plot.svg", format="svg")
    plt.close()

matplotlib.rcParams.update({'font.size': 20})
dir_scores, topic_scores = gleu_copy_structure_and_process_files(
    src_directory, dest_directory, keywords)
plot_combined_gleu_scores(topic_scores)
