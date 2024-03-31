import argparse
from math import log10
from collections import defaultdict
from english_words import english_words_lower_set
import copy
from math import ceil, inf
import random
from nltk.tokenize import word_tokenize
import nltk

nltk.download("punkt")
# from nltk.corpus import gutenberg, brown

# General class for n-gram


class N_gram:

    def __init__(self, n=1):
        self.n = n
        self.prob_dict = {}
        self.min_prob = 1.0  # used when we get 0 prob
        self.dictionary = defaultdict(lambda: 1)
        self.longest_word_length = 0
        self.cnt = 0

    # Function to train the model using a given corpus
    def train(self, corpus):
        count_n = {}
        count_n_1 = {}

        for sentence in corpus:
            cur_context = ''
            for i in range(len(sentence)):
                if (cur_context in count_n_1):
                    count_n_1[cur_context] += 1
                else:
                    count_n_1[cur_context] = 1
                if ((sentence[i], cur_context) in count_n):
                    count_n[(sentence[i], cur_context)] += 1
                else:
                    count_n[(sentence[i], cur_context)] = 1
                # print((corpus[i],cur_context))
                self.dictionary[sentence[i]] += 1
                self.cnt += 1
                self.longest_word_length = max(self.longest_word_length,
                                               len(sentence[i]))
                # if(sentence[i] in ['t','h','e','f']): print(sentence[i], sentence)
                cur_context += sentence[i]
                if i >= self.n - 1:
                    removeLen = len(sentence[i - self.n + 1])
                    cur_context = cur_context[removeLen:]

        for key in count_n.keys():
            if key[1] not in self.prob_dict:
                self.prob_dict[key[1]] = dict()
            self.prob_dict[key[1]][key[0]] = round(
                count_n[key] / count_n_1[key[1]], 3)
            if self.prob_dict[key[1]][key[0]] == 0.0:
                self.prob_dict[key[1]][key[0]] = 0.0001
            # if(self.prob_dict[key[1]][key[0]] == 0):
            #     print(count_n[key],count_n_1[key[1]])
            self.min_prob = min(self.min_prob, self.prob_dict[key[1]][key[0]])
        # print(self.min_prob)
        self.min_prob = log10(self.min_prob)

        # print("i:",count_n[("","of")])
        # print(count_n_1["i"])
        # print(self.prob_dict)

    # Get the probablility of a word occuring given a certain context

    def get_prob(self, context, cur_word):
        if context not in self.prob_dict or cur_word not in self.prob_dict[
                context]:
            # print("in:",cur_word)
            return log10(0.001) + self.min_prob
        # print(self.prob_dict[context][cur_word])
        return log10(self.prob_dict[context][cur_word])

    # Get probability with smoothing
    def get_s_prob(self, context, cur_word):
        if context not in self.prob_dict or cur_word not in self.prob_dict[
                context]:
            return log10(0.6 * (self.dictionary[cur_word] / self.cnt))
        return log10(0.6 * self.prob_dict[context][cur_word] - 0.00001 + 0.4 *
                     (self.dictionary[cur_word] / self.cnt))


# Edit Distance


def edit_distance(s1, s2):
    dp = [[0 for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]
    for i in range(1, len(s2) + 1):
        dp[0][i] = i

    for i in range(1, len(s1) + 1):
        dp[i][0] = i

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            dp[i][j] = min(
                min(dp[i - 1][j], dp[i][j - 1]) + 1,
                dp[i - 1][j - 1] + (1 if s1[i - 1] != s2[j - 1] else 0))

    return dp[len(s1)][len(s2)]


# Functions from the nlp tutorial notebook


def edits1(word):
    """All edits that are one edit away from 'word'"""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """All the edits are two edits away from word"""
    return set((e2 for e1 in edits1(word) for e2 in edits1(e1)))


def edits3(word):
    """All the edits are two edits away from word"""
    return set((e2 for e1 in edits2(word) for e2 in edits1(e1)))


def editsk(word, k):
    e = edits1(word)
    prev = e
    for i in range(1, k):
        temp = set(e2 for e1 in prev for e2 in edits1(e1))
        e.update(temp)
        prev = temp
    e.discard(word)
    return e


# Spelling correction class


class Spelling_Corrector(N_gram):

    def __init__(self, n_gram=1):
        super().__init__(n_gram)

    # Generate error word within 2 edit distance of the original word
    def generate_error_word(self, word, edit_distance=2):
        possible_errors = editsk(word, edit_distance)
        # print(possible_errors)
        non_word_errors = []
        real_word_errors = []
        for error in possible_errors:
            if error in self.dictionary:
                real_word_errors.append(error)
            else:
                non_word_errors.append(error)
        # print(real_word_errors)
        c = random.randint(0, 1)
        # c = 1
        if c or len(real_word_errors) == 0:
            return random.choice(non_word_errors)
        return random.choice(real_word_errors)

    # Generate errors in a given set of sentence
    def generate_errors(self, data, edit_distance=2, errors_per_sentence=1):
        print("Generating Errors")
        cnt = 0
        for sentence in data:
            indices = random.choices(range(len(sentence)),
                                     k=errors_per_sentence)
            for i in indices:
                # print("Before: ",sentence[i])
                sentence[i] = self.generate_error_word(sentence[i],
                                                       edit_distance)
                # print("After: ",sentence[i])
            if cnt % 100 == 0:
                print(cnt, "completed")
            cnt += 1

        print("Errors Generated")
        return data

    # Check if there is an error present a given part of the sentence

    def is_error(self, context, word):
        if self.get_prob(context, word) < self.min_prob:
            return True

        return False

    # Find the correction for a word
    def get_corrected_word(self, context, word, removeLen=inf, next_word=""):
        if removeLen == inf:
            removeLen = len(context)
        if context not in self.prob_dict:
            return word

        corrected_word = word
        # print(word)
        next_context = context[removeLen:]
        max_prob = self.get_prob(context, word) + \
            self.get_prob(next_context+word, next_word)
        # if(word == "sure"):
        #     print(max_prob, "c",context,"nc", next_context,"nw", next_word)
        for candidate_word in self.dictionary:
            # if(candidate_word == "of"):
            # print(edit_distance(candidate_word, word) <= 2)
            #     print("maybe:",candidate_word)
            if (edit_distance(candidate_word, word) <= 2):
                # print("possible:", word, candidate_word)
                if self.get_prob(context, candidate_word) + self.get_prob(
                        next_context + candidate_word, next_word) > max_prob:
                    max_prob = self.get_prob(
                        context, candidate_word) + self.get_prob(
                            next_context + candidate_word, next_word)
                    corrected_word = candidate_word
            # print()

        return corrected_word

    # Detect and correct all errors in a set of sentences
    def find_and_correct_errors(self, data_with_errors):
        print("Correction Started")
        corrected_data = data_with_errors
        cnt = 0
        for j in range(len(corrected_data)):
            cur_context = ''
            corrected_cnt = 0
            minp = inf
            mini = -1
            for i in range(len(corrected_data[j])):
                # Just DO NOT set a MAX count on number of words to correct!!
                # if corrected_cnt == max_to_correct:
                #     break
                # if(self.is_error(cur_context, corrected_data[j][i])):
                next_word = ""
                if i + 1 < len(corrected_data[j]):
                    next_word = corrected_data[j][i + 1]
                cur_prob = self.get_prob(cur_context, corrected_data[j][i])
                if (corrected_data[j][i] not in self.dictionary):
                    # print("err:",corrected_data[j][i])
                    removeLen = 0
                    if i >= self.n - 1:
                        removeLen = len(corrected_data[j][i - self.n + 1])

                    # print("word:",cur_context, corrected_data[j][i], removeLen, next_word)
                    bef = corrected_data[j][i]
                    corrected_data[j][i] = self.get_corrected_word(
                        cur_context, corrected_data[j][i], removeLen,
                        next_word)
                    if bef != corrected_data[j][i]:
                        corrected_cnt += 1

                cur_context += corrected_data[j][i]

                if i >= self.n - 1:
                    removeLen = len(corrected_data[j][i - self.n + 1])
                    cur_context = cur_context[removeLen:]

                next_prob = self.get_prob(cur_context, next_word)
                # print("c",cur_context, "w", corrected_data[j][i], "nw", next_word)
                if cur_prob + next_prob < minp:
                    minp = cur_prob + next_prob
                    mini = i

            cur_context = ""
            # print(minp, corrected_data[j][mini])
            # print("core",corrected_cnt)

            for i in range(len(corrected_data[j])):
                # if corrected_cnt == max_to_correct:
                #     break
                # print(cur_context, corrected_data[j][i])
                if (i == mini):
                    # print("err:",corrected_data[j][i])
                    removeLen = 0
                    if i >= self.n - 1:
                        removeLen = len(corrected_data[j][i - self.n + 1])
                    next_word = ""
                    if i + 1 < len(corrected_data[j]):
                        next_word = corrected_data[j][i + 1]
                    # print("word:",cur_context, corrected_data[j][i], removeLen, next_word)
                    corrected_data[j][i] = self.get_corrected_word(
                        cur_context, corrected_data[j][i], removeLen,
                        next_word)
                    corrected_cnt += 1
                cur_context += corrected_data[j][i]
                if i >= self.n - 1:
                    removeLen = len(corrected_data[j][i - self.n + 1])
                    cur_context = cur_context[removeLen:]
            if cnt % 100 == 0:
                print(cnt, "Completed")

            cnt += 1

            # print()
        print("Correction Done")
        return corrected_data


# Train and Test for the model


class Problem:

    def __init__(self, train_file, test_file, solve):
        self.train_file = train_file
        self.test_file = test_file
        self.solve = solve
        self.train_data = []
        self.test_data = []

    def read_data_from_file(self, file_path):
        with open(file_path, 'r') as file:
            data = file.readlines()  # Need to return each line as ONE string!!
        return data

    def load_data(self):
        # Load and preprocess the training and test datasets
        raw_train_data = self.read_data_from_file(self.train_file)
        raw_test_data = self.read_data_from_file(self.test_file)
        self.train_data = self.preprocess(raw_train_data)
        self.test_data = self.preprocess(raw_test_data)
        print("At loading:")
        print(len(self.train_data))
        print(len(self.test_data))

    # change the preprocessing accordingly
    def preprocess(self, data):
        processed_data = []  # a list of lists (sentences of words)

        for line in data:
            tokens = word_tokenize(line)
            if tokens:
                processed_data.append(tokens)
        return processed_data

    def answer(self, output_file):
        self.solve(self.train_data, self.test_data, output_file)
        print("Now:")
        print(len(self.train_data))
        print(len(self.test_data))


def solvep1(train_data, test_data, output_file):
    corrector = Spelling_Corrector(2)
    corrector.train(train_data)

    corrected_data = corrector.find_and_correct_errors(test_data)

    # Assign this back to test_data???? Or maybe just directly save

    with open(output_file, 'w') as file:
        for sentence in corrected_data:
            file.write(' '.join(sentence) + '\n')
    print(f"Output written to {output_file}")


# p1 = Problem('train.txt', 'test.txt', solvep1)
# p1.load_data()
# p1.answer('corrected_output.txt')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Spell corrector for text files.')
    parser.add_argument('train_file',
                        type=str,
                        help='Path to the training datasets file')
    parser.add_argument('test_file',
                        type=str,
                        help='Path to the test datasets file')
    parser.add_argument('output_file',
                        type=str,
                        help='Path for the corrected output file')

    args = parser.parse_args()

    # Instantiate and use your Problem class with the provided arguments
    problem_instance = Problem(args.train_file, args.test_file, solvep1)
    problem_instance.load_data()
    problem_instance.answer(args.output_file)
