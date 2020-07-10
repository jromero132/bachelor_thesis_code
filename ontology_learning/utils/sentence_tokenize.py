from nltk import tokenize


def sentence_tokenize(text):
	return tokenize.sent_tokenize(text)
