class MedlineCorpus:
	def __init__(self, date_generated, *, articles = []):
		self._date_generated = date_generated
		self._articles = articles

	# magic methods
	def __len__(self):
		return len(self._articles)

	def __iter__(self):
		return (article for article in self._articles)

	# instance properties
	@property
	def date_generated(self):
		return self._date_generated

	# instance methods
	def add_health_topic(medline_article):
		self._articles.append(medline_article)