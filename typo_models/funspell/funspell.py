"""
Funspell is An automatic spell corrector using statistical n-gram models. This is a module which help us to build our custom n-gram model and make use of that language model to perform a context aware automatic spell correction.
"""

import pickle
import os
import re
import string
import collections
import sys 
import random

from nltk.util import ngrams
from pandas import read_csv
import hunspell


def build_ngram_model(file_path, data_file, output_path="./"):
    """A method which estimate the n-grams and persist it to disk
    Keyword parameters:
    data_file:str
    file name which data is stored
    file_path:str
    file path where the data file is present
    output_path : str
    A pkl file will be generated to this given path
    """

    try:
        with open(os.path.join(file_path, data_file), "rb") as file :
            text=str(file.read())
        
    except Exception as e:
        print(e)
        return 
    punctuationNoPeriod = "[" + re.sub("\.","",string.punctuation)+ "]"
    text = re.sub(punctuationNoPeriod, "", text)

    #getting the tokens
    tokenized=text.split()
    ngram_dict={}
    #getting ngrams
    esBigrams=ngrams(tokenized,2)
    esUnigrams=ngrams(tokenized,1)
    esTrigrams=ngrams(tokenized,3)
    es4grams=ngrams(tokenized,4)
    es5grams=ngrams(tokenized,5)
    #getting frequencies of each ngrams
    ngram_freq=dict()
    esBigramFreq=dict(collections.Counter(esBigrams))
    ngram_freq.update(esBigramFreq)
    esUnigramFreq=dict(collections.Counter(esUnigrams))
    ngram_freq.update(esUnigramFreq)
    esTrigramFreq=dict(collections.Counter(esTrigrams))
    ngram_freq.update(esTrigramFreq)
    es4gramFreq=dict(collections.Counter(es4grams))
    ngram_dict.update(es4gramFreq)
    es5gramFreq=dict(collections.Counter(es5grams))
    ngram_freq.update(es5gramFreq)

    with open(os.path.join(output_path,'ngram.pkl'),'wb') as ngram :
        pickle.dump(ngram_freq,ngram)
    
    print("files saved")


if len(sys.argv) > 1 :
    #get path to the file from  sys.argv[1]
    file_path = sys.argv[1]
    # get the file name from sys.argv[2]
    file_name =sys.argv[2]
    #get output_path from sys.argv[3]
    output_path = sys.argv[3]
    build_ngram_model(file_path, file_name, output_path)


class Funspell():
    def __init__(self,file_path='./'):
        """
        file_path : str
        Path to ngram.pkl file build using build_ngram_model function
        """
        self.h = hunspell.HunSpell("en_US.dic", "en_US.aff")
        self.spell = self.h.spell
        self.file_path=file_path
        try:
            print(os.path.join(self.file_path, "ngram.pkl"))
            self.model = open(os.path.join(self.file_path, "ngram.pkl"), "rb")
            self.ngram_model = pickle.load(self.model)
            self.model.close()
        except Exception as e:
            print(e)
            print("please build n-gram first")
            return 


    def update_vocabulary_file(self, file_path="./"):
        """update HunSpell vocabulary using csv
        keyword argument:
        -------
        file_path:str
        a csv file name in the root directory
        """
        

        hunspell_add = self.h.add
        try:
            df = read_csv(file_path)
            words_to_add = list(df.words)

        except Exception as e:
            print("Update Failed, Please check the pathand confirm .csv file present in it")
            return

        words_to_add = map(str.lower, words_to_add)
        for each_taken in words_to_add:
            hunspell_add(each_taken)


    def get_relevant_suggestions(self, words):
        """a function to reduce the number of suggestions using unigrams    
        keyword parameters:
        words:list
        list of suggested words by hunspell 
        return values:
        relevant_suggestions:list
        list of words present in unigram model
        """
        relevant_suggestions = list()
        relevant_suggestions_append = relevant_suggestions.append
        for each_words in ngrams(words, 1):
            try:
                rel_freq = self.ngram_model[each_words]
                if rel_freq > 0:
                    for each in each_words:
                        relevant_suggestions_append(each)
            except KeyError:
                pass
        return relevant_suggestions


    def get_wrong_words(self, query):
        """find mispelled words and returns the list.
        if their is no mispelled words, exit the module
        keyword argument:
        query:str
        the input query as a string 
        return values:
        wrong_words:list
        list of mispelled words found in input text 
        """
        query = re.sub(r"[^\w\s]", "", query)
        query_tokens = query.lower().split()
        wrong_words = list()
        wrong_append = wrong_words.append

        for each in query_tokens:
            try:
                if not self.spell(each):
                    wrong_append(each)
            except Exception as e:
                print(e)

        if len(wrong_words) == 0:
            print("no corrections")
        else:
            return wrong_words


    def get_relevant_ngrams(self, tokenized_sentences, suggested_words, ngram_type):
        """A method to create ngram for given 'n' and filter the relevant ngrams
        keyword arguments:
        tokenized_sentences:list(list)
        list of tokenized sentences
        suggested_words:list
        list of hunspell suggestions for the wrong words 
        ngram_type:int
        value of 'N' to choose the ngram
        return values:
        suggested_gram_dict:dict
        a dictionary with ngrams of each suggested words
        """

        all_ngrams = list()
        all_ngrams_append = all_ngrams.append
        for tok in tokenized_sentences:
            all_ngrams_append(list(ngrams(tok, ngram_type)))
        grams_ = list()
        grams_append = grams_.append
        for each in all_ngrams:
            for each_gram in each:
                grams_append(each_gram)

        suggested_gram_dict = dict()
        for h_suggest in suggested_words:
            suggested_gram_dict[h_suggest] = []
            for each_bigram in grams_:
                if h_suggest in each_bigram:
                    suggested_gram_dict[h_suggest].append(each_bigram)

        return suggested_gram_dict


    def correct_spelling(self, incorrect_word, input_text, value_of_n):
        """this function will find the correct word for the wrong word given and insert it into the query
        parameters
        -------
        incorrect_word:str
        incorrect word in the sentence 
        query:str
        the sentence given by the user 
        value_of_n:int
        value of n to check,2gram through 5gram(default is 2)
        returns
        -------
        ultimate_result:str
        returns the corrected sentence 
        """
        # print("Input text is: ")
        # print(input_text)
        # print(input_text is None)

        try:
            suggested_words = self.h.suggest(incorrect_word)
            if len(suggested_words)<1:
                print("Sorry, No spelling suggestion found,  try updating the Hunspell dictionary")

            suggested_words = self.get_relevant_suggestions(suggested_words)
        except:
            pass

        # when there is no suggested_words, then just do not correct this...
        if len(suggested_words) == 0:
            return input_text

        if len(suggested_words) == 1:
            result = suggested_words[0]
            ultimate_result = input_text.replace(incorrect_word, result)

            return ultimate_result

        elif len(suggested_words) > 1:

            sentence_list = list()
            for word in suggested_words:
                sentence_list.append(input_text.replace(incorrect_word, word))

            tokens_list = list(map(str.split, sentence_list))

            gram_dict = self.get_relevant_ngrams(tokens_list, suggested_words, value_of_n)
            frequency_list = [0] * 20
            for ind, each_hspell in enumerate(suggested_words, 0):
                for _2gram in gram_dict[each_hspell]:
                    try:
                        frequency_list[ind] += self.ngram_model[_2gram]
                    except KeyError:
                        pass

            result_index = frequency_list.index(max(frequency_list))
            result = suggested_words[result_index]
            ultimate_result = input_text.replace(incorrect_word, result)
            
            return ultimate_result


    def correct(self, _text, value_of_n=2):
        """A function to get input and perform spell correction after checking conditions
        keyword parameters:
        _text:str
        input text to the module which should be corrected(should not be empty)
        value_of_n:int
        value of 'n' of ngram(default is 2)
        """

        if len(_text) == 0:
            raise ValueError("given text is empty")

        elif value_of_n < 2 or value_of_n > 5:
            raise ValueError("Allowed value of 'n' are 2,3,4,5")

        after_correction = _text
        
        # print("The original sentence: ")
        # print(after_correction)
        
        wrong = self.get_wrong_words(_text)      

        if wrong is None or len(wrong)<1:
            print("no wrong words found")
            return after_correction

        for each_wrong in wrong:
            # print("The wrong word: ", each_wrong)
            
            # each time, after_correction is updated!
            after_correction = self.correct_spelling(
                each_wrong, after_correction, int(value_of_n)
            )
        return after_correction
