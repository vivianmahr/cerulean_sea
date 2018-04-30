from actions.text_processing.token_taggers import token
import re
from data_access import text_fetcher

class Tokenizer():
	def __init__(self):
		pass
	
	def __call__(self, text, fetcher):
		text = re.sub(r"['][^\s-]* |[\.\?\!]",  lambda x: " " + x.group(0), text)
		result = text.split(" ")
		return [token.Token(item, fetcher) for item in result]