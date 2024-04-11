import json
import os
import spacy
from collections import defaultdict
import matplotlib.pyplot as plt

"""
We want to:
1. Find the GLEU score of 
2. Find the similarity 

Limitations: 
Both GLEU and similarity may not be best suited for this task of typo correction, because 1. GLEU is designed for machine translation,
while our text is somewhat "translation", there may be better metrics that fit.
for both it may not handle typo datasets well.
corpus_similarity may be bad as they put more weightage to longer sentences.

My opinion:
I think that spacy similarity is better because it understands the contextual meaning of the sentences generated. They may be slightly different in grammar
but it will capture the meanings better compared to GLEU which does an ngram kind of comparision. If one word typo / wrong the other ngrams may be wrong?

Downside of spacy similarity: when it encounter unknown word or typo it may be bad, also cannot just compare the entire corpus similarity cuz the scores are so skewed.
"""

abcn_baseline_path = "../data/corrected/baseline/ABCN.dev.gold.bea19_corrected.txt"
abcn_long_path = "../data/corrected/corrected_long_sentence/ABCN.dev.gold.bea19_corrected_long_sentence.txt"
abcn_short_path = "../data/corrected/corrected_short_sentence/ABCN.dev.gold.bea19_corrected_short_sentence.txt"

nlp = spacy.load("en_core_web_md")

def process_file(src_file_path, dest_file_path, reference_file_path):
    similarity_scores = []
    with open(src_file_path, 'r',
              encoding='utf-8') as src, open(dest_file_path,
                                             'w',
                                             encoding='utf-8') as dest, open(
                                                 reference_file_path,
                                                 'r',
                                                 encoding='utf-8') as ref:
        for src_line, ref_line in zip(src, ref):
            doc1 = nlp(src_line)
            doc2 = nlp(ref_line)
            score = doc1.similarity(doc2)
            similarity_scores.append(score)
            dest.write(f"Similarity: {score}\n")

        avg_score = sum(similarity_scores) / len(similarity_scores)
        dest.write(f"Average Sentence Similarity Score: {avg_score}\n")

    with open("./similarity_scores/total_results.txt",
              "a") as file:  # store total results
        file.write(
            f"{src_file_path}: Avg: {avg_score}\n"
        )
    return avg_score


def similarity_copy_structure_and_process_files(src_directory, dest_directory,
                                          keywords):
    os.makedirs(dest_directory, exist_ok=True)
    try:
        os.remove("./similarity_scores/total_results.txt")
    except:
        pass
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
                    dest_subdir, file.replace('.txt', '_similarity_score.txt'))
                avg_score = process_file(src_file_path, dest_file_path, reference_file_path)
                name = file[:-4]
                scores.append((name, avg_score))
                print(
                    f"Processed {src_file_path}, results in {dest_file_path}, ref {reference_file_path}"
                )
                topic_scores[topic].append(
                    ("".join(name.split("_")[1:]), avg_score))

        summary_path = os.path.join(dest_subdir, "summary_results.txt")
        with open(summary_path, 'w', encoding='utf-8') as summary_file:
            for file, avg_score in scores:
                summary_file.write(
                    f"{file}: Avg: {avg_score}\n"
                )

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


def plot_directory_scores(directory_scores):
    for directory, scores in directory_scores.items():
        sorted_scores = sorted(scores, key=lambda x: sorting_key(x[0]))
        files = [score[0] for score in sorted_scores]
        avg_sentence_scores = [score[1] for score in sorted_scores]

        plt.figure(figsize=(10, 6))
        plt.plot(files,
                 avg_sentence_scores,
                 label='Avg Sentence Similarity',
                 marker='o')

        plt.title(f"Similarity Scores in {os.path.basename(directory)}")
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Models")
        plt.ylabel("Scores")
        plt.legend()
        plt.tight_layout()
        plot_path = os.path.join(directory, "similarity_scores_plot.png")
        plt.savefig(plot_path)
        plt.close()


src_directory = '../predictions'
dest_directory = './similarity_scores'
keywords = ["light", "medium", "heavy", "long", "short"]


def plot_topic_scores(topic_scores):
    for topic, scores in topic_scores.items():
        # Sort scores by model name for consistent plotting
        scores.sort(key=lambda x: x[0])
        models = [score[0] for score in scores]
        avg_sentence_scores = [score[1] for score in scores]

        # Compute the averages for the avg_sentence_scores and corpus_scores
        avg_of_avg_sentence_scores = sum(avg_sentence_scores) / len(
            avg_sentence_scores)

        # Set up the plotting area
        plt.figure(figsize=(10, 6))
        plt.ylim(0.75, 1.05)

        # Create the bar chart
        x_indices = range(len(models))
        plt.bar(x_indices,
                avg_sentence_scores,
                width=0.4,
                label='Avg Sentence Similarity',
                align='center')

        # Add model names to x-axis
        plt.xticks(x_indices, models, rotation=45, ha="right")

        # Draw horizontal lines for the average values
        plt.axhline(y=avg_of_avg_sentence_scores,
                    color='blue',
                    linestyle='--',
                    label='Avg of Avg Sentence Similarity')

        # Add title and labels
        plt.title(f"{topic.capitalize()} Similarity Scores")
        plt.xlabel("Models")
        plt.ylabel("Scores")

        # Show legend
        plt.legend()
        plt.tight_layout()

        plt.savefig(f"./similarity_scores/{topic}_scores_plot.png")
        plt.close()
        print(f"Plot saved for topic: {topic}")

scores_filename = "./dir_topic_scores.json"

if os.path.exists(scores_filename): # use the cached value
    with open(scores_filename, 'r') as file:
        data = json.load(file)
        dir_scores = data['dir_scores']
        topic_scores = data['topic_scores']
else: # we need to get the vals and store them
    dir_scores, topic_scores = similarity_copy_structure_and_process_files(
        src_directory, dest_directory, keywords)

    with open(scores_filename, 'w') as file:
        json.dump({'dir_scores': dir_scores, 'topic_scores': topic_scores}, file)


plot_directory_scores(dir_scores)
plot_topic_scores(topic_scores)