import random
import nltk
import re
from os import listdir
#import spacy
import json
#import emotion
#nlp = spacy.load('en')

# Note to future self: things sent in emails and chats aren't always one sentence, so don't go dumping
# whole emails in the poor sentence class without thinking

JSON_string = """
        "conversation_id" : {},
	"sentence_id" : {},
	"speaker_id" : {},
	"speaker_name": {},
	"text" : {},
	"tokens" : {},
	"pbank_tags" : {},
	"upos_tags" : {},
	"dialogue_tag" : {},
	"truthfulness" : {},
	"is_sarcasm" : {},
	"sentiment" : {}"""


class Misc_Features():
    """ Things I want to program for someday but don't have official names/algorithms/actual terms/
    not even sure if sarcasm is doable without knowing the speaker 
    """
    def __init__(self, sarcasm=False, sentiment=0, truthfulness=.5):
        self.is_sarcasm = sarcasm
        self.sentiment = sentiment
        self.truthfulness = truthfulness

class Sentence():
    """Taking all the information out of spacy's tagger and putting it into a
       form that I can reference better and possibly alter, plus a few more things
       I want to consider"""
    def __init__(self, sentence, sentence_id, speaker_id, conversation_id, speaker_name, d_tag):
        # Original String
        self.text = sentence
        self.sentence_id = sentence_id
        self.conversation_id = conversation_id
        # List of tokens - see Token on how to access individual attributes
        self.tokens = nltk.word_tokenize(sentence)

        self.pbank_tags = nltk.pos_tag(self.tokens)
        self.upos_tags = []

        # For future use, recording habits of users
        self.speaker_id = speaker_id
        # !! Record speaker name in its own class when you figure out all the things that might be relvant
        self.speaker_name= "speaker_name"

        # For classifying intention of sentences
        self.dialogue_tag = d_tag

        self.misc_features = Misc_Features()

        # implementation plans:
        # pos tagging
        # dialogue tagging - will take a while
        # chunking / sentence structure
        # long break as I experient generate texts and play with nlg

        # no order atm
        # sentiment
        # ner
        # srl -__-
        
    def tokenize(self, sentence):
        self.tokens = nltk.word_tokenize(self.sentence)

    def to_JSON(self):
        result = JSON_string.format(self.conversation_id, self.sentence_id, 1, "vivian", self.text, self.tokens, \
                                    self.pbank_tags, self.upos_tags, self.dialogue_tag, \
                                    self.misc_features.truthfulness, self.misc_features.is_sarcasm, \
                                    self.misc_features.sentiment)
        return "{\n" + result + "\n}\n"
        

class Token():
    def __init__(self):
        # UNUSED ATM - for just generating tagged conversations, nltk returns tuples already 
        #self.lemma = ''
        # Universal POS tags
        self.pos = ""

        # Penn tags
        self.tag = "" 
        #self.dep = "" #syntattic dependency, look more at this later
        #self.shape = ""
        #self.is_alpha = False
        #self.is_stop = False
        #self.morph_features = []


class Conversation_Manager():
    def __init__(self):
        self.shut_down = False
        
        items = listdir("./conversations")
        self.conversation_id = max([int(re.search("[\d]+", f).group(0)) for f in items]) + 1
        self.sentences = []
        pass

    def receive_input(self, inp, speaker_id, speaker_name, d_tag):
        # Split by . and ? for now
        new_sentence = Sentence(inp, len(self.sentences),speaker_id, self.conversation_id, speaker_name, d_tag)

    def add_sentence(self, s):
        self.sentences.append(s)

    def generate_output(self, inp):
        output = ""
        if inp.strip() == "QUIT":
            self.quit()
            output = lazy_output("farewell")
        else:
            output = lazy_output(inp)
        #self._add_sentences(output, 0, 'SELF')
        return output

    def save(self):
        with open("./conversations/output_{}.txt".format(self.conversation_id), "w") as file:
            file.write(self.to_string())

    def to_string(self):
        result = ""
        for sentence in self.sentences:
            result += sentence.to_JSON() + "\n"
        return result 

    def quit(self):
        self.save()
        self.shut_down = True
        

def check_previous_letters(string, substring, num_letters, check_for):
    ind = string.find(substring)
    return (check_for in string[ind-num_letters:ind])


def lazy_output(inp):
    if inp == "farewell":
        return "Farewell."
    """'lazy' and not in a class so I remember to replace this method ASAP"""
    sense_keywords = ["smell", "taste", "food", "scent", "felt", "touch"]
    opinion_keywords = {"think": "you",
                    "why": "",
                    "opinion": "your",
                    "thoughts": "your",
                    }
    statements = ["I see... Actually, no I don't. What are you saying?",
                  "I don't understand, but it is okay. ",
                  "Why?",
                  "...",
                  "Hmm... So what do you intend to do?",
                  "...Are you alright?"]
    greetings = ["hello", "heya", "hi", "hey"]
    split_inp = nltk.word_tokenize(inp.lower())
    if "?" in inp:
        return "I do not know."
    for term, search_for in opinion_keywords.items():
        if term in split_inp and check_previous_letters(inp, term, len(search_for)+2,search_for):
            return "I do not know how to form opinions yet."
    for term in ["smell", "taste", "food", "scent", "felt", "touch"]:
        if term in split_inp:
            return "I do not have that sense."
    for term in greetings:
        if term in split_inp:
            return random.choice(greetings)
    return random.choice(statements)



if __name__ == "__main__":
    
    inp = ""
    c_manager = Conversation_Manager()
    s_counter = 0
    while not c_manager.shut_down:
        inp = input("user: ")
        s = Sentence(inp, s_counter, 1, c_manager.conversation_id, "vivian", "")
        print(s.to_JSON())
        # Here is normally where I would check tags before sending it in
        c_manager.add_sentence(s)
        response = c_manager.generate_output(inp)
        print("c_sea: {}".format(response))
