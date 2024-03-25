# Reference: https://norvig.com/spell-correct.html
# A naive, edit distance-based model
import nltk
from collections import Counter
class NorvigTypoModel:
    def __init__(self, corpus_path) -> None:
        corpus_text = open(corpus_path).read()
        corpus_tokens = nltk.tokenize.word_tokenize(corpus_text)
        self.words_dict = Counter(corpus_tokens)
        self.words_total = sum(self.words_dict.values())
        self.predict_memo = {}
    # Gets all words of edit distance of 1 
    def get_edit1(self, word):
        letters = "abcdefghijklmnopqrstuvwxyz"
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)] 
        deletes = [L + R[1:] for L, R in splits if R]
        inserts = [L + c + R for L, R in splits for c in letters]
        subs = [L + c + R[1:] for L, R in splits if R for c in letters]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) >= 2]
        return set(deletes + inserts + subs + transposes)
    # Gets all words of edit distance of 2 
    def get_edit2(self, word):
        edit2_words = set()
        for edit1_word in self.get_edit1(word):
            edit2_words = edit2_words.union(self.get_edit1(edit1_word))
        return edit2_words
    # Gets the unigram probability of a word in the corpus
    def get_prob(self, word, smoothing = 0):
        return (self.words_dict[word] + smoothing) / self.words_total * (1 + smoothing)
    # Filter out words that not in the corpus
    def filter_known(self, words):
        return set(filter(lambda w:(w in self.words_dict), words))
    # Get the candidates words. We determine words with the same edit distance away
    # to have the same likelihood of being choosen. 
    def get_candidates(self, word):
        return (self.filter_known([word])\
            or self.filter_known(self.get_edit1(word))\
            or self.filter_known(self.get_edit2(word))\
            or [word])
    # Get the prediction of words
    def predict_word(self, word):
        if word in self.predict_memo:
            return self.predict_memo[word]
        prediction = max(self.get_candidates(word), key=self.get_prob)
        self.predict_memo[word] = prediction
        return prediction
    def predict_sentence(self, sentence):
        words = sentence.split(" ")
        return " ".join([self.predict_word(word) for word in words])

# Some basic tests
if __name__ == "__main__":
    model = NorvigTypoModel("big.txt")
    words_test = ["duckk", "addres", "meo", "too", "Statess", "Chna"]
    for word in words_test:
        print(model.predict_word(word))
    sentence_test = [
        '''It 's difficult anxwer at the qjestion " wyat ate gou going to do in thw future ? " if the only onw wyo has to know it is in twk minds .''',
        '''When I was younger I used to say thst I wamted to be a teacher , a saleswoman and erven a butcher .. I do n't know shy .'''
    ]
    for sentence in sentence_test:
        print(model.predict_sentence(sentence)) 