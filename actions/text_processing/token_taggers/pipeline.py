from actions.text_processing.token_taggers import tokenizer, tagger
from data_access import text_fetcher

class Pipeline():
	def __init__(self):
		self.pipeline = [tokenizer.Tokenizer(), tagger.Tagger()]
		self.fetcher = text_fetcher.Text_Fetcher()
		
	def pipe(self, text):
		result = text
		for item in self.pipeline:
			result = item(result, self.fetcher)
		return result
		
		# right now, it's tokens->lemma->tagger->parser(dependency)-> weirder things
		# string.split by exactly " " 
		# prefixes, hyphens, suffixes
p = Pipeline()
l = p.pipe("here I am!")

for i in l:
	print(i)