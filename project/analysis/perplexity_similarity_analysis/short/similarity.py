import spacy
nlp = spacy.load("en_core_web_sm")


def get_similarity_score(correct_file, output_file):
    total_similarity = 0
    total_lines = 0
    with open(correct_file, 'r') as f_c, open(output_file, 'r') as f_o:
        correct, output = f_c.readlines(), f_o.readlines()
        total_lines += len(correct)
        for i in range(len(correct)):
            d1, d2 = nlp(correct[i]), nlp(output[i])
            total_similarity += d1.similarity(d2)
    return total_similarity/total_lines


# edit the file to compare accordingly
correct_file = "ABCN.dev.gold.bea19_original_short_sentence.txt"
output_file = "ABCN.dev.gold.bea19_original_short_sentence_typo_medium.txt"
similarity_score = get_similarity_score(correct_file, output_file)
print(similarity_score)
## similarity score 0.8703058618889775

