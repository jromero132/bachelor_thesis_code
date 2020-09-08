from .annotation import Annotation
import re

class SameAsAnnotation(Annotation):
	def __init__(self, id: str, typ: str, args: "List[str]"):
		super(SameAsAnnotation, self).__init__(id, typ)
		self.args = args

	@staticmethod
	def try_parse(line: str) -> bool:
		return line.startswith("*")

	@staticmethod
	def parse(line: str) -> "SameAsAnnotation":
		match = re.fullmatch(r"(?P<id>\*)\t(?P<type>[\w\-]+) (?P<args>[\w\s]+)", line)
		id, typ, args = match.group("id"), match.group("type"), re.split(" ", match.group("args"))
		return SameAsAnnotation(id, typ, args)

	def __repr__(self):
		return f"<Relation(id={self.id}, type={self.type}, args={self.args})>"

	def __str__(self):
		return self.__repr__()

	def as_ann(self) -> str:
		return f"{self.id}\t{self.type} {' '.join(self.args)}"