import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from collections import defaultdict
import difflib

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


# Get tag from TRUE CORRECT sentence
def get_pos_tags(sentence):
    tokens = word_tokenize(sentence)
    tagged_tokens = pos_tag(tokens)
    pos_positions = defaultdict(list)

    for idx, (word, tag) in enumerate(tagged_tokens):
        if tag.startswith('VB'):
            pos_positions['verb'].append(idx)
        elif tag.startswith('NN'):
            pos_positions['noun'].append(idx)
        elif tag == 'IN':
            pos_positions['prep'].append(idx)

        elif tag.startswith("JJ"):
            pos_positions['adj'].append(idx)
        elif tag.startswith("RB"):
            pos_positions['adv'].append(idx)

        elif tag.startswith("PRP"):
            pos_positions['pron'].append(idx)
        elif tag.startswith('CC'):
            pos_positions['conj'].append(idx)
        elif tag.startswith("UH"):
            pos_positions['inter'].append(idx)
    return pos_positions


# M2 file is split by paragraphs
def read_m2_file(m2_file_path):
    with open(m2_file_path, 'r') as f:
        content = f.read().strip()
    paragraphs_raw = content.split('\n\n')
    paragraphs = [item.split('\n') for item in paragraphs_raw]
    return paragraphs


def read_sentence_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def check_equal_length(length_list):
    if len(length_list) <= 1:
        return True
    res = all(elem == length_list[0] for elem in length_list)

    return res


def evaluate_correction_accuracy(total_errors, corrected_errors):
    print("ACCURACY RATE")
    for error_type in total_errors.keys():
        total = total_errors[error_type]
        corrected = corrected_errors[error_type]
        if total > 0:
            accuracy_rate = (corrected / total) * 100
        else:
            accuracy_rate = -100
        print(f"{error_type.upper()}: {accuracy_rate:.2f}%")


def process_files(m2_file, typo_file, true_corrected_file, my_corrected_file):
    m2_content = read_m2_file(m2_file)
    incorrect_content = read_sentence_file(typo_file)
    correct_content = read_sentence_file(true_corrected_file)
    generated_content = read_sentence_file(my_corrected_file)

    # check equal length
    length_list = [
        len(m2_content),
        len(incorrect_content),
        len(correct_content),
        len(generated_content)
    ]
    if not check_equal_length(length_list):
        print("Found disparity between lengths of different files")
    max_length = min(length_list)

    total_errors = defaultdict(int)
    corrected_errors = defaultdict(int)

    for i in range(max_length):
        evaluate_correction_results(total_errors, corrected_errors,
                                    m2_content[i], incorrect_content[i],
                                    correct_content[i], generated_content[i])

    return total_errors, corrected_errors


def evaluate_correction_results(total_errors, corrected_errors, m2_list,
                                original_sentence, true_corrected_sentence,
                                my_corrected_sentence):

    pos_positions = get_pos_tags(true_corrected_sentence)

    true_corrected = true_corrected_sentence.split()
    my_corrected = my_corrected_sentence.split()

    verb_total_error = 0
    verb_error_corrected = 0
    prep_total_error = 0
    prep_error_corrected = 0
    noun_total_error = 0
    noun_error_corrected = 0

    adj_total_error = 0
    adj_error_corrected = 0
    adv_total_error = 0
    adv_error_corrected = 0

    pron_total_error = 0
    pron_error_corrected = 0
    conj_total_error = 0
    conj_error_corrected = 0
    inter_total_error = 0
    inter_error_corrected = 0

    original_correct_offset = 0  # The difference in index (from original to corrected)
    original_generate_offset = 0

    s = difflib.SequenceMatcher(None, original_sentence.split(),
                                my_corrected_sentence.split())
    generate_align = s.get_opcodes()
    generate_align_ptr = 0
    '''
    (1) Get the offset between original and my_corrected sentence, using difflib
    (2) Get the offset between original and true_corrected sentence, using m2 operations
    (3) Compare corresponding positions
    '''
    for correction in m2_list:
        if correction.startswith("S"):
            continue

        original_offset = int(correction.split()[1])

        # get original_generate_offset
        while generate_align_ptr < len(generate_align) and generate_align[
                generate_align_ptr][2] < original_offset:
            tag, i1, i2, j1, j2 = generate_align[generate_align_ptr]

            original_generate_offset += (j2 - j1) - (i2 - i1)
            generate_align_ptr += 1

        # get original_correct_offset (but should do the addition by END of each loop)
        try:
            error_type = correction.split()[2].split("|||")[1]
            if error_type == "noop":  # i.e. no operation
                continue

            correction_type = error_type.split(":")[0]  # e.g. M, R, U
            word_type = error_type.split(":")[1]  # e.g. PREP, SPELL
        except:
            print("Error retrieving correction_type")
            print(correction)
            continue

        correct_offset = original_offset + original_correct_offset
        generate_offset = original_offset + original_generate_offset

        # Check correction status
        try:
            if correct_offset in pos_positions['verb']:
                verb_total_error += 1

                if generate_offset >= len(my_corrected):
                    # Actually this would also count towards failed correction -- sample index: Corrected:  (57, 55) Generated:  (51, 51)
                    pass
                elif true_corrected[correct_offset].lower(
                ) == my_corrected[generate_offset].lower():
                    verb_error_corrected += 1

            if correct_offset in pos_positions['prep']:
                prep_total_error += 1

                if generate_offset >= len(my_corrected):
                    pass
                elif true_corrected[correct_offset].lower(
                ) == my_corrected[generate_offset].lower():
                    prep_error_corrected += 1

            if correct_offset in pos_positions['noun']:
                noun_total_error += 1

                if generate_offset >= len(my_corrected):
                    pass
                elif true_corrected[correct_offset].lower(
                ) == my_corrected[generate_offset].lower():
                    noun_error_corrected += 1

            if correct_offset in pos_positions['adj']:
                adj_total_error += 1

                if generate_offset >= len(my_corrected):
                    pass
                elif true_corrected[correct_offset].lower(
                ) == my_corrected[generate_offset].lower():
                    adj_error_corrected += 1

            if correct_offset in pos_positions['adv']:
                adv_total_error += 1

                if generate_offset >= len(my_corrected):
                    pass
                elif true_corrected[correct_offset].lower(
                ) == my_corrected[generate_offset].lower():
                    adv_error_corrected += 1

            if correct_offset in pos_positions['pron']:
                pron_total_error += 1

                if generate_offset >= len(my_corrected):
                    pass
                elif true_corrected[correct_offset].lower(
                ) == my_corrected[generate_offset].lower():
                    pron_error_corrected += 1

            if correct_offset in pos_positions['conj']:
                conj_total_error += 1

                if generate_offset >= len(my_corrected):
                    pass
                elif true_corrected[correct_offset].lower(
                ) == my_corrected[generate_offset].lower():
                    conj_error_corrected += 1

            if correct_offset in pos_positions['inter']:
                inter_total_error += 1

                if generate_offset >= len(my_corrected):
                    pass
                elif true_corrected[correct_offset].lower(
                ) == my_corrected[generate_offset].lower():
                    inter_error_corrected += 1
        except Exception as e:
            print(e)
            print("Corrected: ", (len(true_corrected), correct_offset))
            print("Generated: ", (len(my_corrected), generate_offset))

            print("Error comparing correction due to offset out of bound")

        # Update original_correct_offset
        if correction_type == "M":
            original_correct_offset += 1

        elif correction_type == "U":
            original_correct_offset -= 1

    # finally, update the dict
    total_errors['verb'] += verb_total_error
    total_errors['prep'] += prep_total_error
    total_errors['noun'] += noun_total_error
    total_errors['adj'] += adj_total_error
    total_errors['adv'] += adv_total_error
    total_errors['pron'] += pron_total_error
    total_errors['conj'] += conj_total_error
    total_errors['inter'] += inter_total_error

    corrected_errors['verb'] += verb_error_corrected
    corrected_errors['prep'] += prep_error_corrected
    corrected_errors['noun'] += noun_error_corrected
    corrected_errors['adj'] += adj_error_corrected
    corrected_errors['adv'] += adv_error_corrected
    corrected_errors['pron'] += pron_error_corrected
    corrected_errors['conj'] += conj_error_corrected
    corrected_errors['inter'] += inter_error_corrected


# Usage:
folder_path = '/content/drive/My Drive/cs2109_dataset/cs4248_assignment2/typo/'

m2_file = folder_path + "true.m2"
typo_file = folder_path + "ABCN.dev.gold.bea19_original_typo.txt"
true_corrected_file = folder_path + "ABCN.dev.gold.bea19_corrected.txt"
my_corrected_file = folder_path + "ABCN_original_typo_norvig.txt"

total_errors, corrected_errors = process_files(m2_file, typo_file,
                                               true_corrected_file,
                                               my_corrected_file)

evaluate_correction_accuracy(total_errors, corrected_errors)
