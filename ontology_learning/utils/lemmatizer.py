import spacy


class Lemmatizer:
	def __init__(self, *, model = "es_core_news_lg"):
		self.model = model
		self.nlp = spacy.load(self.model)

	def lemmatize(self, text):
		return " ".join(word.lemma_ for word in self.nlp(text))
		# return text