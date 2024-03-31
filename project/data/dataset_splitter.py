import os


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


def get_light_medium_heavy_typo():  # for both original and corrected.
    pass


def get_addition_typo():
    pass


def get_sentence_typo():  #long short, original and corrected.
    pass
