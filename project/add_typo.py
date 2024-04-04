import random
import re
import json

# Can change config parameters here.
light_config = {
    "threshold": 0.3,
    "weights": [0.7, 0.1, 0.1, 0.1],
    "max_flips": 1
}

med_config = {
    "threshold": 0.5,
    "weights": [0.7, 0.1, 0.1, 0.1],  # standard
    "max_flips": 2
}

heavy_config = {
    "threshold": 0.7,
    "weights": [0.7, 0.1, 0.1, 0.1],
    "max_flips": 3
}

# All the other configs follow from med.
substitution_config = {
    "threshold": 0.5,
    "weights": [1, 0, 0, 0],
    "max_flips": 2
}
transposition_config = {
    "threshold": 0.5,
    "weights": [0, 1, 0, 0],
    "max_flips": 2
}
addition_config = {"threshold": 0.5, "weights": [0, 0, 1, 0], "max_flips": 2}
subtraction_config = {
    "threshold": 0.5,
    "weights": [0, 0, 0, 1],
    "max_flips": 2
}

# THRESHOLD = 0.5
# If all errors include only substitution, then usually can be corrected.
# including other errors might make it harder
ERRORS = ['Substitution', 'Transposition', 'Addition', 'Subtraction']
# WEIGHTS = [0.7, 0.1, 0.1, 0.1]

# for key mapping, there is no mapping for non alpabets, as we assume that only alphabets
# are chosen wrongly (hard to correct original_typo for non-alphabet typos).
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

def add_typo(word, config):
    if len(word) <= 2:
        return word
    amount_to_change = random.randint(1, min(
        len(word), config["max_flips"]))  # up to min(len(word), max_flips)
    indexes = random.sample(range(len(word)), amount_to_change)
    res = []
    i = 0
    while i < len(word):
        if i not in indexes:
            res.append(word[i])
            i += 1
            continue
        mode = random.choices(ERRORS, config["weights"], k=1)[0]
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


def random_transform(string, config):
    new_phrase = []
    typos = []
    corrected = [] # keep track of typos.
    # to split the special characters also
    arr = re.split('([^a-zA-Z0-9])', string)
    for word in arr:
        outcome = random.random()
        if outcome <= config["threshold"]:
            new_word = add_typo(word, config)
            new_phrase.append(new_word)
            if word != new_word:
                typos.append(new_word)
                corrected.append(word)
        else:
            new_phrase.append(word)
    return "".join(new_phrase), typos, corrected


def make_typo_file(filename, input_file_path, output_file_path, config=med_config):
    typos, corrected = [], []
    dct = {}
    with open(input_file_path, "r", encoding="utf-8") as file:
        with open(output_file_path, "w", encoding="utf-8") as out:
            for line in file:
                transformed_line, typo_row, corrected_row = random_transform(line, config)
                out.write(transformed_line)
                typos.append(typo_row)
                corrected.append(corrected_row)

    # make the metadata file for original_typo.
    dct[filename] = (typos, corrected)
    json_path = output_file_path.replace(".txt", ".json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(dct, json_file, ensure_ascii=False, indent=4)