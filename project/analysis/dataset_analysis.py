import os
from collections import Counter
import matplotlib.pyplot as plt


def get_stats_for_file(file_path):
    total_sentences = 0
    total_words = 0
    word_lengths = Counter()
    sentence_lengths = Counter()

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('S '):
                sentence = line[2:].strip()
                total_sentences += 1
                words = sentence.split()
                sentence_length = len(words)
                sentence_lengths[sentence_length] += 1

                for word in words:
                    word_length = len(word)
                    word_lengths[word_length] += 1
                    total_words += 1

    stats = {
        'total_sentences': total_sentences,
        'total_words': total_words,
        'word_lengths': word_lengths,
        'sentence_lengths': sentence_lengths,
    }

    return stats


def aggregate_stats(all_stats):
    total_stats = {
        'total_sentences': 0,
        'total_words': 0,
        'word_lengths': Counter(),
        'sentence_lengths': Counter(),
    }

    for stats in all_stats.values():
        total_stats['total_sentences'] += stats['total_sentences']
        total_stats['total_words'] += stats['total_words']
        total_stats['word_lengths'] += stats['word_lengths']
        total_stats['sentence_lengths'] += stats['sentence_lengths']

    return total_stats


# There exists some outliers (super long sentences / words) in our dataset, so the graph is quite skewed.
def plot_distributions(word_lengths, sentence_lengths, filename):
    plt.figure(figsize=(14, 6))
    plt.suptitle(filename)

    plt.subplot(1, 2, 1)
    plt.bar(word_lengths.keys(), word_lengths.values(), color='skyblue')
    plt.xlabel('Word Length')
    plt.ylabel('Frequency')
    plt.title('Word Length vs Frequency')

    plt.subplot(1, 2, 2)
    plt.bar(sentence_lengths.keys(), sentence_lengths.values(), color='lightgreen')
    plt.xlabel('Sentence Length (in words)')
    plt.ylabel('Frequency')
    plt.title('Sentence Length vs Frequency')

    plt.tight_layout()
    plt.savefig(f"./{filename}_plot.png")

def save_file_stats(stats, filename):
    total_sentences = stats['total_sentences']
    total_words = stats['total_words']
    avg_sentence_length = sum(count * length for length, count in stats['sentence_lengths'].items()) / total_sentences if total_sentences > 0 else 0
    total_word_length = sum(count * length for length, count in stats['word_lengths'].items())
    avg_word_length = total_word_length / total_words if total_words > 0 else 0

    with open(filename + "_stats.txt", "w") as f:
        f.write(f"Total Sentences:{total_sentences}\n")
        f.write(f"Average Sentence Length:{avg_sentence_length}\n")
        f.write(f"Total Words:{total_words}\n")
        f.write(f"Average Word Length:{avg_word_length}\n")

def get_stats_and_plot(directory_path):
    all_stats = {} # each files statistics.

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            file_stats = get_stats_for_file(file_path)
            all_stats[filename] = file_stats

    # 1. Start with total
    total_stats = aggregate_stats(all_stats)
    save_file_stats(total_stats, "original_total")
    plot_distributions(total_stats['word_lengths'], total_stats['sentence_lengths'], "original_total")

    # 2. For each file
    for filename, file_stats in all_stats.items():
        save_file_stats(file_stats, filename)
        plot_distributions(file_stats['word_lengths'], file_stats['sentence_lengths'], filename)

data_directory_path = "../old_data/original_typo"
get_stats_and_plot(data_directory_path)