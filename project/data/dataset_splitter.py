import os
import shutil
from project.add_typo import *

def clear_directories(parent_directories):
    for parent_dir in parent_directories:
        for subdir in os.listdir(parent_dir):
            subdir_path = os.path.join(parent_dir, subdir)
            if os.path.isdir(subdir_path):
                for filename in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
def get_originals_and_corrected():
    og_dir_path = "../old_data/original_typo"
    cor_dir_path = "../old_data/corrected_typo"
    # get OG
    for filename in os.listdir(og_dir_path):
        og_file_path = os.path.join(og_dir_path, filename)
        output_file_path = os.path.join("./original/baseline/",
                                        filename[:-9] + ".txt")

        with open(output_file_path, "w", encoding='utf-8') as out:
            with open(og_file_path, 'r', encoding='utf-8') as in_file:
                for line in in_file:
                    if line.startswith('S '):
                        out.write(line[2:])

    # get corrected
    for filename in os.listdir(cor_dir_path):
        cor_file_path = os.path.join(cor_dir_path, filename)
        output_file_path = os.path.join("./corrected/baseline/",
                                        filename[:-9] + ".txt")

        with open(output_file_path, "w", encoding='utf-8') as out:
            with open(cor_file_path, 'r', encoding='utf-8') as in_file:
                for line in in_file:
                    if line.startswith('C '):
                        out.write(line[2:])


def get_sentence_dataset():
    og_dir_path = "./original/baseline"
    cor_dir_path = "./corrected/baseline"
    SHORT_THRESHOLD = 8  # short sentence has <=8 words
    LONG_THRESHOLD = 50

    # get OG
    for filename in os.listdir(og_dir_path):
        og_file_path = os.path.join(og_dir_path, filename)
        short_file_path = os.path.join("./original/original_short_sentence/",
                                       filename[:-4] + "_short_sentence.txt")
        long_file_path = os.path.join("./original/original_long_sentence/",
                                      filename[:-4] + "_long_sentence.txt")

        with open(short_file_path, "w", encoding='utf-8') as short_out:
            with open(long_file_path, "w", encoding='utf-8') as long_out:
                with open(og_file_path, 'r', encoding='utf-8') as in_file:
                    for line in in_file:
                        words = len(line.split())
                        if words <= SHORT_THRESHOLD:
                            short_out.write(line)
                        elif words >= LONG_THRESHOLD:
                            long_out.write(line)

    # get corrected
    for filename in os.listdir(cor_dir_path):
        og_file_path = os.path.join(cor_dir_path, filename)
        short_file_path = os.path.join("./corrected/corrected_short_sentence/",
                                       filename[:-4] + "_short_sentence.txt")
        long_file_path = os.path.join("./corrected/corrected_long_sentence/",
                                      filename[:-4] + "_long_sentence.txt")

        with open(short_file_path, "w", encoding='utf-8') as short_out:
            with open(long_file_path, "w", encoding='utf-8') as long_out:
                with open(og_file_path, 'r', encoding='utf-8') as in_file:
                    for line in in_file:
                        words = len(line.split())
                        if words <= SHORT_THRESHOLD:
                            short_out.write(line)
                        elif words >= LONG_THRESHOLD:
                            long_out.write(line)


def get_word_dataset():
    og_dir_path = "./original/baseline"
    cor_dir_path = "./corrected/baseline"
    SHORT_THRESHOLD = 5  # all words must be <= 5 characters.
    LONG_THRESHOLD = 10  # There exists words of >= 10 characters.

    # get OG
    for filename in os.listdir(og_dir_path):
        og_file_path = os.path.join(og_dir_path, filename)
        short_file_path = os.path.join("./original/original_short_word/",
                                       filename[:-4] + "_short_word.txt")
        long_file_path = os.path.join("./original/original_long_word/",
                                      filename[:-4] + "_long_word.txt")

        with open(short_file_path, "w", encoding='utf-8') as short_out:
            with open(long_file_path, "w", encoding='utf-8') as long_out:
                with open(og_file_path, 'r', encoding='utf-8') as in_file:
                    for line in in_file:
                        words = line.split()
                        if all(len(w) <= SHORT_THRESHOLD for w in words):
                            short_out.write(line)
                        elif any(len(w) >= LONG_THRESHOLD for w in words):
                            long_out.write(line)

    # get corrected
    for filename in os.listdir(cor_dir_path):
        og_file_path = os.path.join(cor_dir_path, filename)
        short_file_path = os.path.join("./corrected/corrected_short_word/",
                                       filename[:-4] + "_short_word.txt")
        long_file_path = os.path.join("./corrected/corrected_long_word/",
                                      filename[:-4] + "_long_word.txt")

        with open(short_file_path, "w", encoding='utf-8') as short_out:
            with open(long_file_path, "w", encoding='utf-8') as long_out:
                with open(og_file_path, 'r', encoding='utf-8') as in_file:
                    for line in in_file:
                        words = line.split()
                        if all(len(w) <= SHORT_THRESHOLD for w in words):
                            short_out.write(line)
                        elif any(len(w) >= LONG_THRESHOLD for w in words):
                            long_out.write(line)

def get_typo_dataset():
    # For every input dir / output dir / config, we run make_typo_file on the filepath.
    input_dirs = [
        # Baseline, long, and short variations for original
        "./original/baseline", "./original/baseline", "./original/baseline",
        "./original/original_long_sentence", "./original/original_long_word",
        "./original/original_short_sentence", "./original/original_short_word",
        "./original/baseline", "./original/baseline", "./original/baseline", "./original/baseline",
        # Baseline, long, and short variations for corrected
        "./corrected/baseline", "./corrected/baseline", "./corrected/baseline",
        "./corrected/corrected_long_sentence", "./corrected/corrected_long_word",
        "./corrected/corrected_short_sentence", "./corrected/corrected_short_word",
        "./corrected/baseline", "./corrected/baseline", "./corrected/baseline", "./corrected/baseline",
    ]

    output_dirs = [
        # Baseline, long, and short variations for original
        "./original_typo/light", "./original_typo/medium", "./original_typo/heavy",
        "./original_typo/long_sentence", "./original_typo/long_word",
        "./original_typo/short_sentence", "./original_typo/short_word",
        "./original_typo/addition_only", "./original_typo/substitution_only", "./original_typo/subtraction_only",
        "./original_typo/transposition_only",
        # Baseline, long, and short variations for corrected
        "./corrected_typo/light", "./corrected_typo/medium", "./corrected_typo/heavy",
        "./corrected_typo/long_sentence", "./corrected_typo/long_word",
        "./corrected_typo/short_sentence", "./corrected_typo/short_word",
        "./corrected_typo/addition_only", "./corrected_typo/substitution_only", "./corrected_typo/subtraction_only",
        "./corrected_typo/transposition_only",
    ]

    configs = [
        # Baseline, long, and short variations configs
        light_config, med_config, heavy_config,
        med_config, med_config,
        med_config, med_config,
        addition_config, substitution_config, subtraction_config, transposition_config,
    ] * 2 # for both original & corrected

    configs_suffix = [
        "light", "medium", "heavy",
        "medium", "medium",
        "medium", "medium",
        "addition_only", "substitution_only", "subtraction_only", "transposition_only"
    ]

    names = [f"_typo_{suffix}.txt" for suffix in configs_suffix] * 2  # Multiply by 2 for both original and corrected

    for input_dir_path, output_dir_path, config, name in zip(input_dirs, output_dirs, configs, names):
        for filename in os.listdir(input_dir_path):
            if filename.endswith(".txt"):
                input_file_path = os.path.join(input_dir_path, filename)
                out_name = filename.replace(".txt", name)
                output_file_path = os.path.join(output_dir_path, out_name)

                print(f"Processing {input_file_path} to {output_file_path}")
                make_typo_file(filename, input_file_path, output_file_path, config=config)

# clear_directories(['./original_typo', './corrected_typo'])
get_typo_dataset()