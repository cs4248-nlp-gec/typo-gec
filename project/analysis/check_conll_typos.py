import pickle
import string
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate  # might need to `pip install tabulate``

# Usage: add the names of the models to analyze here
# Note: prediction file must be found at exactly {PREDS_DIR}/{model_name}/conll_{model_name}.txt
# ==> might need to temporarily change directory/file names for this (e.g. gector_base folder --> gectorbase)
MODELS = [
    "gectorbase",
    "gectorRoBERTa+gectorbase",
    "gectorBERT+gectorbase",
]
RESULTS_DIR = "./conll_performance"
PREDS_DIR = "../predictions"
SKIP_PROPER_NOUNS = True
SKIP_PUNCS = True

# which CONLL M2 to compare against (combined has 2 annotators)
CONLL_M2_PATH = "../og_datasets/conll14st-test-data/official-2014.combined.m2"
# where to store the results
TYPO_CORRECTIONS_PATH = "./conll_corrections.pickle"

OVERRIDE_PICKLE = True


def generate_typo_corrections(source, dest):
    with open(source, 'r') as f:
        m2_annots = f.readlines()

    typo_corrections_per_sent = []
    curr_sent = None
    curr_sent_corrections = None

    for line in m2_annots:
        if line[0] == 'S':
            if curr_sent is not None:
                typo_corrections_per_sent.append(curr_sent_corrections)
            curr_sent = line[2:].split(" ")
            curr_sent_corrections = []
        elif line[0] == 'A':
            tokens = line.split("|||")
            if tokens[1] != "Mec":
                continue
            correction = tokens[2]
            typo_l, typo_r = map(int, tokens[0].split(" ")[1:])
            if correction == "" or typo_l == typo_r or typo_l == len(
                    curr_sent) - 1:
                continue
            typo = " ".join(curr_sent[typo_l:typo_r])
            if SKIP_PROPER_NOUNS and typo.lower() == correction.lower():
                continue
            if SKIP_PUNCS and (any(c in string.punctuation for c in typo)
                               or any(c in string.punctuation
                                      for c in correction)):
                continue
            curr_sent_corrections.append(
                ((typo, curr_sent.count(typo)), (correction,
                                                 curr_sent.count(correction)),
                 tokens[-1].strip()))
    typo_corrections_per_sent.append(curr_sent_corrections)

    with open(dest, 'wb') as f:
        pickle.dump(typo_corrections_per_sent, f)


def check_typos(pred_file, model):
    with open(pred_file, 'r', encoding='utf8') as f:
        predictions = map(lambda s: s.strip(), f.readlines())

    typos_unfixed = []
    typos_fixed_wrongly = []
    typos_fixed_correctly = []

    for i, (corrections, line) in enumerate(zip(typo_corrections,
                                                predictions)):
        if corrections == ():
            continue
        tokens = line.split(" ")
        for tup in corrections:
            typo, typo_cnt = tup[0]
            corr, corr_cnt = tup[1]
            annotator = tup[2]
            if (tokens.count(typo) < typo_cnt):
                if (tokens.count(corr) > corr_cnt):
                    typos_fixed_correctly.append(
                        (i + 1, typo, corr, annotator))
                else:
                    typos_fixed_wrongly.append((i + 1, typo, corr, annotator))
            else:
                typos_unfixed.append((i + 1, typo, corr, annotator))

    total_fix_attempts = len(typos_fixed_wrongly + typos_fixed_correctly)
    total_typos = total_fix_attempts + len(typos_unfixed)
    table = [
        ["Typos fixed correctly",
         len(typos_fixed_correctly)],
        ["Typos fixed wrongly",
         len(typos_fixed_wrongly)],
        ["Total typo fix attempts", total_fix_attempts],
        [
            "% of fix attempts that were correct",
            f"{round((len(typos_fixed_correctly) / total_fix_attempts) * 100, 2)}%"
        ], ["Total number of typos", total_typos],
        [
            "% of typos attempted to fix",
            f"{round(total_fix_attempts/total_typos*100, 2)}%"
        ]
    ]

    with open(f"{RESULTS_DIR}/{model}_typo_report.txt", 'w',
              encoding='utf-8') as f:
        f.write(f">>> {model} <<<\n\n")
        f.write("Summary: \n")
        f.write(tabulate(table, tablefmt="grid"))
        f.write("\n\nTypos fixed correctly: \n")
        f.writelines(
            map(
                lambda tup:
                f"Line {tup[0]}: \tidentified {tup[1]:<16} : rectified to {tup[2]:<16} : annotator {tup[3]}\n",
                typos_fixed_correctly))
        f.write("\n\nTypos fixed wrongly: \n")
        f.writelines(
            map(
                lambda tup:
                f"Line {tup[0]}: \tidentified {tup[1]:<16} : didn't correct to {tup[2]:<16} : annotator {tup[3]}\n",
                typos_fixed_wrongly))
        f.write("\n\nTypos not fixed/identified: \n")
        f.writelines(
            map(
                lambda tup:
                f"Line {tup[0]}: \tdidn't fix {tup[1]:<16} : expected {tup[2]:<16} : annotator {tup[3]}\n",
                typos_unfixed))

    return (len(typos_fixed_correctly), total_fix_attempts, total_typos)


if __name__ == "__main__":
    if OVERRIDE_PICKLE or not os.path.isfile(TYPO_CORRECTIONS_PATH):
        generate_typo_corrections(CONLL_M2_PATH, TYPO_CORRECTIONS_PATH)

    with open(TYPO_CORRECTIONS_PATH, 'rb') as f:
        typo_corrections = pickle.load(f)

    correct_fixes = []
    total_fixes = []

    for model in MODELS:
        num_correct, num_fixes, _ = check_typos(
            f"{PREDS_DIR}/{model}/conll_{model}.txt", model)
        correct_fixes.append(num_correct)
        total_fixes.append(num_fixes)

    x_coords = np.arange(len(MODELS))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    correct_fix_bars = ax.bar(x_coords - width / 2,
                              correct_fixes,
                              width,
                              label="Typos fixed correctly")
    total_fix_bars = ax.bar(x_coords + width / 2,
                            total_fixes,
                            width,
                            label="Total # typo fix attempts")

    ax.set_title("Typo performance on CoNLL-14 corpus")
    ax.set_ylabel("Occurrences")
    ax.set_xticks(x_coords)
    ax.set_xticklabels(MODELS)
    ax.set_xlabel("Models")
    ax.legend()

    fig.tight_layout()

    plt.axhline(correct_fixes[0], linestyle='--')
    plt.axhline(total_fixes[0], linestyle='--', color="orange")

    plt.savefig(f"{RESULTS_DIR}/compare_plot.png")
    plt.savefig(f"{RESULTS_DIR}/compare_plot.svg")
    plt.savefig(f"{RESULTS_DIR}/compare_plot.pdf")
