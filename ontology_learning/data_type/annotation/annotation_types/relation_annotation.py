from .annotation import Annotation
import re

class RelationAnnotation(Annotation):
	def __init__(self, id: str, typ: str, arg1: str, arg2: str):
		super(RelationAnnotation, self).__init__(id, typ)
		self.arg1 = arg1
		self.arg2 = arg2

	@staticmethod
	def try_parse(line: str) -> bool:
		return line.startswith("R")

	@staticmethod
	def parse(line: str) -> "RelationAnnotation":
		match = re.fullmatch(r"(?P<id>R\d+)\t(?P<type>[\w\-]+) Arg1:(?P<arg1>\w+) Arg2:(?P<arg2>\w+)", line)
		id, typ = match.group("id").capitalize(), match.group("type").lower()
		arg1, arg2 = match.group("arg1").capitalize(), match.group("arg2").capitalize()
		return RelationAnnotation(id, typ, arg1, arg2)

	def __repr__(self):
		return f"<Relation(id={self.id}, type={self.type}, arg1={self.arg1}, arg2={self.arg2})>"

	def __str__(self):
		return self.__repr__()

	def as_ann(self) -> str:
		return f"{self.id}\t{self.type} Arg1:{self.arg1} Arg2:{self.arg2}"