import spacy

nlp = spacy.load("en_core_web_sm")


def get_similarity_score(correct_file, output_file):
    total_similarity = 0
    with open(correct_file, 'r') as f_c, open(output_file, 'r') as f_o:
        correct, output = f_c.readlines(), f_o.readlines()
        for i in range(len(correct)):
            d1, d2 = nlp(correct[i]), nlp(output[i])
            total_similarity += d1.similarity(d2)
    return total_similarity


correct_file = "typo_long_sentence_correct.txt"
output_file = "typo_long_sentence_output.txt"
similarity_score = get_similarity_score(correct_file, output_file)
print(similarity_score)
## similarity score is 88.90632571817265
"""
m2 score
Precision   : 0.6631
Recall      : 0.2568
F_0.5       : 0.5037
"""
