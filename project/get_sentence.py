import os

# modified from https://www.cl.cam.ac.uk/research/nl/bea2019st/data/corr_from_m2.py


def get_sentence(file):
    originals = []
    sentences = []
    skip = {"noop", "UNK", "Um"}
    lines = file.read().strip().split("\n\n")

    for sent in lines:
        sent = sent.split("\n")
        cor_sent = sent[0].split()[1:]  # Ignore "S "
        originals.append(" ".join(cor_sent))
        edits = sent[1:]
        offset = 0
        for edit in edits:
            edit = edit.split("|||")
            if len(edit) >= 2 and edit[1] in skip:
                continue  # Ignore certain edits
            span = edit[0].split()[1:]  # Ignore "A "
            start = int(span[0])
            end = int(span[1])
            cor = edit[2].split()
            cor_sent[start + offset:end + offset] = cor
            offset = offset - (end - start) + len(cor)

        sentences.append(" ".join(cor_sent))

    return originals, sentences


for filename in os.listdir("og_datasets"):
    if filename.endswith(".m2"):
        file_path = os.path.join("og_datasets", filename)
        output_file_path = os.path.join(
            "./out", filename.replace(".m2", "_corrected.txt"))

        with open(file_path, "r") as file:
            with open(output_file_path, "w") as out:
                for og, ne in zip(*get_sentence(file)):
                    out.write(f"S {og}\nC {ne}\n\n")
