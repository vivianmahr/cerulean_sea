import re
import numpy as np
from data_access import text_fetcher

POS_LIST = ["", 'ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
MAX_WORD_LENGTH = 40

class Token():    
    nn_length = 666
    def __init__(self, word, fetcher, previous_pos=""):
        self.raw_text = word
        if len(word) > 40:
            raise Error("Max word length is 40 characers.")
        self._processed_text = word.strip().lower()

        self.shape = self._get_shape()
        self.is_alphanumeric = self._is_alphanumeric()

        self.is_stop = fetcher.is_in(self._processed_text, "stop")
        self._previous_pos = previous_pos
        self.pos = ""
        self.lemma = ""
    
    def _get_shape(self):
        word = self.raw_text
        word = re.sub(r"[A-Z]", "X", self.raw_text)
        word = re.sub(r"[a-z]", "x", word)
        word = re.sub(r"[\d]", "d", word)
        return word

    def _is_alphanumeric(self):
        return bool(re.match(r"^([A-Za-z\d]*)$", self.raw_text))

    def _pos_to_int(self, pos):
        return POS_LIST.index(pos)

    def _bin_to_list(self, bitstring, length):
        result = [int(i) for i in bitstring[2:]]
        while len(result) < length:
            result.insert(0, 0)
        return result
		
    def __str__(self):
        return "{}: {}".format(self.raw_text, self.pos)	
    def __repr__(self):
        return "{}: {}".format(self.raw_text, self.pos)

    def _chr_to_list(self, char):
        return self._bin_to_list(bin(ord(char)), 8)

    def to_nn_input(self):
        """ Max word length is 40 chrs by default, that should cover most words in the English language."""
        
        arr_word  = list(np.zeros(MAX_WORD_LENGTH * 8,  dtype="int"))
        arr_shape = list(np.zeros(MAX_WORD_LENGTH * 8,  dtype="int"))
        position = 0
        for i in range(len(self.raw_text)):
            byte_text = self._chr_to_list(self.raw_text[i])
            byte_shape = self._chr_to_list(self.shape[i])
            for n in range(8):
                arr_word[position] = byte_text[n]
                arr_shape[position] = byte_shape[n]
                position += 1
        len_array = self._bin_to_list(bin(len(self._processed_text)), 6)
        pos_array = list(np.zeros(len(POS_LIST), dtype="int"))
        pos_array[POS_LIST.index(self._previous_pos)] = 1

        arr_features = pos_array + len_array + [int(self.is_alphanumeric), int(self.is_stop)]
        result = arr_word + arr_shape + arr_features
        return np.reshape(result, (len(result), 1))   
