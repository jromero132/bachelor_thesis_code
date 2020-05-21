from ontology_learning.data_type.medline.medline_article.medline_article_metadata import MedlineArticleMetadata


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
		self.meta = meta