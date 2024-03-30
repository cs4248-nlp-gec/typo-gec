import random
import re
import os
from collections import defaultdict

# modify as necessary
THRESHOLD = 0.5

# If all errors include only substitution, then usually can be corrected.
# including other errors might make it harder
ERRORS = ['Substitution', 'Transposition', 'Addition', 'Subtraction']
WEIGHTS = [0.7, 0.1, 0.1, 0.1]

# for key mapping, there is no mapping for non alpabets, as we assume that only alphabets
# are chosen wrongly (hard to correct typo for non-alphabet typos).
# Mapping only for keys with one key difference in keyboard layout. Can modify as necessary
KEY_MAPPING = {
    'a': ['q', 'w', 's', 'x', 'z'],
    'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'e': ['w', 's', 'd', 'r'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'j', 'k', 'o'],
    'j': ['h', 'u', 'i', 'k', 'n', 'm'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k', 'l'],
    'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'k', 'l', 'p'],
    'p': ['o', 'l'],
    'q': ['w', 'a', 's'],
    'r': ['e', 'd', 'f', 't'],
    's': ['w', 'e', 'd', 'x', 'z', 'a'],
    't': ['r', 'f', 'g', 'y'],
    'u': ['y', 'h', 'j', 'i'],
    'v': ['c', 'f', 'g', 'v', 'b'],
    'w': ['q', 'a', 's', 'e'],
    'x': ['z', 's', 'd', 'c'],
    'y': ['t', 'g', 'h', 'u'],
    'z': ['a', 's', 'x'],
}

# determine how many characters to flip for a word, modify as necessary.


def num_of_chars_to_flip(word):
    return 1


def random_transform(string):
    new_phrase = []
    # arr = string.split()
    # to split the special characters also
    arr = re.split('([^a-zA-Z0-9])', string)
    for word in arr:
        outcome = random.random()
        if outcome <= THRESHOLD:
            new_word = add_typo(word)
            new_phrase.append(new_word)
        else:
            new_phrase.append(word)
    return "".join(new_phrase)


def add_typo(word):
    if len(word) <= 2:
        return word
    flip_count = num_of_chars_to_flip(word)
    indexes = random.sample(range(len(word)), flip_count)
    res = []
    i = 0
    while i < len(word):
        if i not in indexes:
            res.append(word[i])
            i += 1
            continue
        mode = random.choices(ERRORS, WEIGHTS, k=1)[0]
        if mode == ERRORS[1]:
            if i == len(word) - 1 or i + 1 in indexes:
                # if cannot transpose just substitute
                mode = ERRORS[0]
            else:
                val = word[i + 1] + word[i].lower()
                if word[i].isupper():
                    val.capitalize()
                res.append(val)
                i += 1
        elif mode == ERRORS[0] and word[i].lower() in KEY_MAPPING:
            upper = word[i].isupper()
            character = random.choice(KEY_MAPPING[word[i].lower()])
            character = character.upper() if upper else character
            res.append(character)
        elif mode == ERRORS[2] and word[i].lower() in KEY_MAPPING:
            res.append(word[i])
            res.append(random.choice(KEY_MAPPING[word[i].lower()]))
        elif mode == ERRORS[3]:
            pass
        else:
            # catch case if somehow the operation to add errors fail
            res.append(word[i])
        i += 1
    return "".join(res)


phrase = "This is a test-sentence, Mary has a little -lamb"
new_phrase = random_transform(phrase)
print(new_phrase)


def make_typo_file(file, outfile):
    for line in file.readlines():
        if line.startswith(
                "S "):  # change this if u want corrected or original sentence
            outfile.write(f"{line}T {random_transform(line[2:])}\n")


for filename in os.listdir("./out"):
    if filename.endswith(".txt"):
        file_path = os.path.join("./out", filename)
        # change filename to distinguish corrected or original typo
        output_file_path = os.path.join(
            "./corrected_typo",
            filename.replace("_corrected.txt", "_corrected_typo.txt"))

        with open(file_path, "r") as file:
            with open(output_file_path, "w") as out:
                make_typo_file(file, out)
