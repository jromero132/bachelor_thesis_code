class MedlineArticleMetadata:
	def __init__(
		self,
		*,
		url = None,
		language = None,
		title = None,
		description = None,
		id = None,
		date_created = None,
		also_called = None,
	):
		self.url = url
		self.language = language
		self.title = title
		self.description = description
		self.id = id
		self.date_created = date_created
		self.also_called = also_called