# own modules
from ontology_learning.data_type.medline.medline_article.medline_article_metadata import MedlineArticleMetadata
from ontology_learning.utils.sentence_tokenize import sentence_tokenize


class MedlineArticle:
	"""Represents a medline article

	Args:
		text (str): text of the medline article
		meta (MedlineArticleMetadata): metadata of the medline article

	Returns:
		None
	"""
	def __init__(
		self,
		text: str,
		*,
		meta: MedlineArticleMetadata = None
	) -> None:
		self.text = text
		self._sentences = sentence_tokenize(text)
		self.meta = meta

	@property
	def sentences(self):
		for sentence in self._sentences:
			yield sentence