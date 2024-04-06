# Reference: https://norvig.com/spell-correct.html
# A naive, edit distance-based model
# Note: the words are lowercased before being parsed in the model. This is to ensure more accurate
# unigram probabilities. We then rely on the GEC model to correct the casings.
import nltk
import re
import csv
from collections import Counter


class NorvigTypoModel:

    def __init__(self, corpus_paths=[]) -> None:
        if len(corpus_paths) == 0:
            return
        self.words_dict = Counter()
        self.words_total = 0
        self.predict_memo = {}

    # Fits a model using text corpuses

    def fit(self, corpus_paths=[]):
        self.words_dict = Counter()
        for corpus_path in corpus_paths:
            print(f"Fitting on {corpus_path}.")
            corpus_tokens = self.get_corpus_tokens(corpus_path)
            self.words_dict.update(Counter(corpus_tokens))
        self.words_total = sum(self.words_dict.values())
        self.predict_memo = {}

    # Saves the model in a CSV file, which is essentially saving the unigram counts

    def save_model(self, model_path="model.csv"):
        with open(model_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.words_dict.items():
                writer.writerow([key, value])

    # Loads a model from a CSV file

    def load_model(self, model_path="model.csv"):
        with open(model_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            self.words_dict = Counter()
            for row in reader:
                self.words_dict[row[0]] = int(row[1])
            self.words_total = sum(self.words_dict.values())
            self.predict_memo = {}

    # Gets tokens from corpus

    def get_corpus_tokens(self, corpus_path):
        corpus_text = open(corpus_path).read().lower()
        return nltk.tokenize.word_tokenize(corpus_text)

    # Gets all words of edit distance of 1

    def get_edit1(self, word):
        letters = "abcdefghijklmnopqrstuvwxyz"
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        inserts = [L + c + R for L, R in splits for c in letters]
        subs = [L + c + R[1:] for L, R in splits if R for c in letters]
        transposes = [
            L + R[1] + R[0] + R[2:] for L, R in splits if len(R) >= 2
        ]
        return set(deletes + inserts + subs + transposes)

    # Gets all words of edit distance of 2

    def get_edit2(self, word):
        edit2_words = set()
        for edit1_word in self.get_edit1(word):
            edit2_words = edit2_words.union(self.get_edit1(edit1_word))
        return edit2_words

    # Gets the unigram probability of a word in the corpus

    def get_prob(self, word, smoothing=0):
        return (self.words_dict[word] +
                smoothing) / self.words_total * (1 + smoothing)

    # Filters out words that not in the corpus

    def filter_known(self, words):
        return set(filter(lambda w: (w in self.words_dict), words))

    # Gets the candidates words. We determine words with the same edit distance away
    # to have the same likelihood of being choosen.

    def get_candidates(self, word):
        return (self.filter_known([word])
                or self.filter_known(self.get_edit1(word))
                or self.filter_known(self.get_edit2(word)) or [word])

    # Gets the prediction of words

    def predict_word(self, word):
        # Don't predict on punctuations
        if re.match(r"^[^\w\s]+$", word) != None:
            return word
        word = word.lower()
        if word in self.predict_memo:
            return self.predict_memo[word]
        prediction = max(self.get_candidates(word), key=self.get_prob)
        self.predict_memo[word] = prediction
        return prediction

    # Predicts a sentence. We assume that the sentence has already been tokenised.

    def predict_sentence(self, sentence):
        words = sentence.split(" ")
        return " ".join([self.predict_word(word) for word in words])


# Some basic tests
if __name__ == "__main__":
    # corpus_filenames = ["eng_news_2020_100K-sentences_processed.txt",
    #                     "eng_wikipedia_2016_100K-sentences.processed.txt",
    #                     "eng-europarlv7.100k.txt"]
    # corpus_dirs = [f"../data/{filename}" for filename in corpus_filenames]
    model = NorvigTypoModel()
    model.load_model("model.csv")
    # model.fit(corpus_dirs)
    # model.save_model()
    words_test = ["duckk", "addres", "meo", "too", "Statess", "Chna"]
    for word in words_test:
        print(model.predict_word(word))
    sentence_test = [
        '''It 's difficult anxwer at the qjestion " wyat ate gou going to do in thw future ? " if the only onw wyo has to know it is in twk minds .''',
        '''When I was younger I used to say thst I wamted to be a teacher , a saleswoman and erven a butcher .. I do n't know shy .'''
    ]
    for sentence in sentence_test:
        print(model.predict_sentence(sentence))
