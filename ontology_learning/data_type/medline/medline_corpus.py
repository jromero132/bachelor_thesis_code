# built-in packages
from typing import Generator

# own modules
from ontology_learning.data_type.medline.medline_article import MedlineArticle

class MedlineCorpus:
	"""Represents a corpus using medline articles as documents

	Args:
		date_generated (str): generation date of the corpus
		articles (list): initial list of articles (documents)

	Returns:
		None
	"""
	def __init__(self, date_generated: str, *, articles: list = []) -> None:
		self.date_generated = date_generated
		self._articles = articles

	# magic methods
	def __len__(self) -> int:
		"""Get the amount of articles in the corpus

		Returns:
			int: length of the corpus
		"""
		return len(self._articles)

	def __iter__(self) -> Generator:
		"""Generator with all articles in the corpus

		Returns:
			Generator: all articles in the corpus as a sequence
		"""
		return (article for article in self._articles)

	# instance methods
	def add_health_topic(medline_article: MedlineArticle) -> None:
		"""Add a health topic to the corpus

		Args:
			medline_article (MedlineArticle): health topic to be added

		Returns:
			None
		"""
		self._articles.append(medline_article)