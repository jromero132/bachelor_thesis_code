from .annotation_types.annotation import Annotation
import inspect
import bisect


class AnnFile:
	def __init__(self, annotations: "List[Annotation]" = []):
		self.annotations = annotations

	@staticmethod
	def load_document(dpath: "Path") -> "AnnFile":
		return AnnFile([
			AnnFile.parse(line)
			for line in dpath.read_text(encoding = 'utf8').splitlines()
			if line != ''
		])

	@staticmethod
	def parse(line: str) -> "Annotation":
		for parser in Annotation.__subclasses__():
			if parser.try_parse(line):
				return parser.parse(line)
		raise ValueError(f"Unknown annotation: {line}")