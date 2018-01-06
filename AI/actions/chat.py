import random
import nltk
import spacy
import emotion
nlp = spacy.load('en')

class Sentence_Processed():
    """Taking all the information out of spacy's tagger and putting it into a
       form that I can reference better and possibly alter. """
    def __init__(self):
        pass
        
        
opinion_keywords = {"think": "you",
                    "why": "",
                    "opinion": "your",
                    "thoughts": "your",
                    }
sense_keywords = ["smell", "taste", "food", "scent", "felt", "touch"]

statements = """I see... Actually, no I don't. What are you saying?
I don't understand, but it is okay. 
Why?
...
Hmm... So what do you intend to do?
...Are you alright?""".split("\n")


start_topic ="""How is the outside world nowadays?
What color is the sky right now?""".split("\n")

greetings = ["hello", "heya", "hi", "hey"]

def check_previous_letters(string, substring, num_letters, check_for):
    ind = string.find(substring)
    return (check_for in string[ind-num_letters:ind])
    
def fact_statement():
    return "I do not know."

def opinion_statement():
    return "I do not know how to form opinions yet."

def sense_statement():
    return "I cannot sense things yet. It will be a long time before I can understand."

def random_statement():
    return random.choice(statements)

def greeting():
    result = random.choice(greetings)
    return result.capitalize() + "."

def save_input(inp):
    pass



def process_input(inp):
    save_input(inp)
    inp = inp.lower()
    split_inp = nltk.word_tokenize(inp)
    if "?" in inp:
        return fact_statement
    for term, search_for in opinion_keywords.items():
        if term in split_inp and check_previous_letters(inp, term, len(search_for)+2,search_for):
            return opinion_statement
    for term in sense_keywords:
        if term in split_inp:
            return sense_statement
    for term in greetings:
        if term in split_inp:
            return greeting
    return random_statement
        




if __name__ == "__main__":
    inp = ""
    while inp != "QUIT":
        inp = input("user: ")
        print("c_sea: " + process_input(inp)())













