import json
from collections import Counter


def compare_files(predicted_file_path, original_file_path, metadata_path):
    with open(metadata_path, 'r', encoding='utf-8') as meta_file:
        metadata = json.load(meta_file)
    typos, correcteds = next(iter(
        metadata.values()))  # json only has 1 value so we just take that one.
    score = Counter()

    with open(predicted_file_path, 'r', encoding='utf-8') as pred_file, open(
            original_file_path, 'r', encoding='utf-8') as og_file:
        for pred_line, og_line, typo, corrected in zip(pred_file, og_file,
                                                       typos, correcteds):
            print("prediction", pred_line)
            print("original", og_line)
            print("typos", typo)
            print("corrected", corrected)
            print(
                "Score",
                get_score(pred_line.strip(), og_line.strip(), typo, corrected))
            score += get_score(pred_line.strip(), og_line.strip(), typo,
                               corrected)
    TP, TN, FP, FN = score["true_positives"], score["true_negatives"], score[
        "false_positives"], score["false_negatives"]
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1_score = 2 * (precision * recall) / (precision + recall)

    print(dict(score))
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1_score:.4f}")


def get_score(pred_line, og_line, typos, corrected):
    """
        TP: Typo is found and corrected correctly
        FP: Typo is found but made wrong correction
        TN: The words that are not typo and not corrected
        FN: Typo is not found at all when theres a typo
    """

    pred_counter = Counter(tuple(pred_line.split()))
    og_counter = Counter(tuple(og_line.split()))
    typo_counter = Counter(tuple(typos))
    corrected_counter = Counter(tuple(corrected))
    true_positives = sum(
        (pred_counter &
         corrected_counter).values())  # the number of predicted correct words.

    #  number of non-typos, non-correcteds. Intersect of both = all common words - all typos - all correcteds.
    true_negatives = sum(((pred_counter & og_counter) - typo_counter -
                          corrected_counter).values())
    # the number of extra words. Aka, from the typo -> incorrect word.
    # pred_counter - typos - all other words in the correct file will give us the extra words.
    false_positives = sum((pred_counter - typo_counter - og_counter).values())
    false_negatives = sum((pred_counter & typo_counter).values(
    ))  # number of typos that remain uncorrected in predicted text.

    return Counter({
        "true_positives": true_positives,
        "true_negatives": true_negatives,
        "false_positives": false_positives,
        "false_negatives": false_negatives
    })


# # Test:
#
# pred_file_path = "../predictions/gector_base/ABCN.dev.gold.bea19_corrected_typo_light.txt"
# og_file_path = "../data/corrected/baseline/ABCN.dev.gold.bea19_corrected.txt"
# metadata_file_path = "../data/corrected_typo/light/ABCN.dev.gold.bea19_corrected_typo_light.json"
# compare_files(pred_file_path, og_file_path, metadata_file_path)