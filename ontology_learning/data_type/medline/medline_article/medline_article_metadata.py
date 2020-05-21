class MedlineArticleMetadata:
	"""Metadata of medline articles used in MedlineArticle class.

	Args:
		url (str): url of the medline article
		language (str): language of the medline article
		title (str): title of the medline article
		description (str): description of the medline article
		id (str): id of the medline article
		date_created (str): creation date of the medline article
		also_called (list): other names of the medline article

	Returns:
		None
	"""
	def __init__(
		self,
		*,
		url: str = None,
		language: str = None,
		title: str = None,
		description: str = None,
		id: str = None,
		date_created: str = None,
		also_called: list = None,
	):
		self.url = url
		self.language = language
		self.title = title
		self.description = description
		self.id = id
		self.date_created = date_created
		self.also_called = also_called