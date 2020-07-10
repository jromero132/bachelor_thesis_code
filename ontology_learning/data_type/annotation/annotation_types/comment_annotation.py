from .annotation import Annotation
import re

class CommentAnnotation(Annotation):
	def __init__(self, comment: str, *, id: str = "#"):
		super(CommentAnnotation, self).__init__(id, "Comment")
		self.comment = comment

	@staticmethod
	def try_parse(line: str) -> bool:
		return line.startswith("#")

	@staticmethod
	def parse(line: str) -> "CommentAnnotation":
		match = re.fullmatch(r"(?P<id>#\d*)(?P<comment>.*)", line)
		id, comment = match.group("id"), match.group("comment").strip()
		return CommentAnnotation(comment, id = id)

	def __repr__(self):
		return f"<Comment(id={self.id}, comment={self.comment})>"

	def __str__(self):
		return self.__repr__()

	def as_ann(self) -> str:
		return f"{self.id} {self.comment}"