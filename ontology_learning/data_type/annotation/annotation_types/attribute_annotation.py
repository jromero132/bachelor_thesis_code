from .annotation import Annotation
import re

class AttributeAnnotation(Annotation):
	def __init__(self, id: str, typ: str, ref: str):
		super(AttributeAnnotation, self).__init__(id, typ)
		self.ref = ref

	@staticmethod
	def try_parse(line: str) -> bool:
		return line.startswith("A")

	@staticmethod
	def parse(line: str) -> "AttributeAnnotation":
		match = re.fullmatch(r"(?P<id>A\d+)\t(?P<typ>\w+) (?P<ref>\w+)", line)
		id, typ, ref = match.group("id").capitalize(), match.group("typ").capitalize(), match.group("ref").capitalize()
		return AttributeAnnotation(id, typ, ref)

	def __repr__(self):
		return f"<Attribute(id={self.id}, type={self.type}, ref={self.ref})>"

	def __str__(self):
		return self.__repr__()

	def as_ann(self) -> str:
		return f"{self.id}\t{self.type} {self.ref}"