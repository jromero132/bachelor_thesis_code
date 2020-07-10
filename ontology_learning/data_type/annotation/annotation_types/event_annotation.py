from .annotation import Annotation
import re

class EventAnnotation(Annotation):
	def __init__(self, id: str, typ: str, ref: str, args: "Dict{str:str}"):
		super(EventAnnotation, self).__init__(id, typ)
		self.ref = ref
		self.args = args

	@staticmethod
	def try_parse(line: str) -> bool:
		return line.startswith("E")

	@staticmethod
	def parse(line: str) -> "EventAnnotation":
		match = re.fullmatch(r"(?P<id>E\d+)\t(?P<type>\w+):(?P<ref>\w+) (?P<args>.*)", line)
		id, typ, ref = match.group("id"), match.group("typ"), match.group("ref")
		args = [ (label, destination) for label, destination in re.findall(r"(\w+):(\w+)", match.group("args")) ]
		return EventAnnotation(id, typ, ref, args)

	def __repr__(self):
		return f"<Event(id={self.id}, type={self.type}, ref={self.ref}, args={self.args})>"

	def __str__(self):
		return self.__repr__()

	def as_ann(self) -> str:
		return f"{self.id}\t{self.type}:{self.ref} {' '.join(f'{k}:{v}' for k, v in self.args.items())}"