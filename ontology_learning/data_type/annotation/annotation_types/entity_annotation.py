from .annotation import Annotation
import re


class EntityAnnotation(Annotation):
	def __init__(self, id: str, typ: str, spans: "List[Tuple(int, int)]", text: str):
		super(EntityAnnotation, self).__init__(id, typ)
		self.spans = spans
		self.text = text

	@staticmethod
	def try_parse(line: str) -> bool:
		return line.startswith("T")

	@staticmethod
	def parse(line: str) -> "EntityAnnotation":
		match = re.fullmatch(r"(?P<id>T\d+)\t(?P<type>\w+) (?P<spans>[\d\s;]+)\t(?P<text>.+)", line)
		id, typ, text = match.group("id").capitalize(), match.group("type").capitalize(), match.group("text")
		spans = [ int(span) for span in re.findall(r"\d+", match.group("spans")) ]
		spans = sorted(zip(spans[ 0::2 ], spans[ 1::2 ]))
		return EntityAnnotation(id, typ, spans, text)

	def __repr__(self):
		return f"<Entity(id={self.id}, type={self.type}, spans={self.spans}, text={self.text})>"

	def __str__(self):
		return self.__repr__()

	def as_ann(self) -> str:
		return f"{self.id}\t{self.type} {';'.join(f'{s} {e}' for s, e in self.spans)}\t{self.text}"