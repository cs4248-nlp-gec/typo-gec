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


# edit the file to compare accordingly
# correct_file = "typo_short_sentence_correct.txt"
# output_file = "typo_short_sentence_output.txt"
# similarity_score = get_similarity_score(correct_file, output_file)
# print(similarity_score)




# similarity score analysis (using spacy similarity)
# short:  0.8703058618889775
# long:   0.8417217784384142
# light:  0.9328222384665961
# medium: 0.8466437749029351
# heavy:  0.7056760309225083

# This similarity score is averaged by the number of lines
# Similarity score for spacy calculated by converting word to vec and compare the vector's similarity

# Analysis result
# We can see that from light to medium to heavy, there is a fall in similarity score. This suggests that the closeness of predictions
# to gold standard falls off as the number of typo increases (which fits our hypothesis and shows that gector is not good at correcting 
# erros with typo)
# Short's similarity score does slightly better, but not that much difference. Not too conclusive. (But perplexity between short and long
# are very huge. So Perplexity is better analysis)