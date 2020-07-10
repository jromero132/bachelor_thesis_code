# from .annotations.comment_annotation import CommentAnnotation
from pathlib import Path

class Sentence:
	def __init__(self, text: str) -> None:
		self.text = text
		self.keyphrases: list = []
		self.relations: list = []

	def sort(self):
		self.keyphrases.sort(key = lambda k: k.spans)
		self.relations.sort(key = lambda r: (r.origin, r.destination))

	def __len__(self) -> int:
		return len(self.text)

	def __repr__(self) -> str:
		return f"Sentence(text={self.text}, keyphrases={self.keyphrases}, relations={self.relations})"

	def __str__(self) -> str:
		return self.__repr__()

	@staticmethod
	def load_document(dpath: Path) -> list:
		return (
			# Sentence(s_stripped)
			Sentence(s)
			for s in dpath.read_text(encoding = "utf8").splitlines()
			# if (s_stripped := s.strip()) != ""
		)

	# @property
	# def annotated(self) -> bool:
	# 	return self.keyphrases or self.relations

	# @property
	# def attributes_len(self) -> int:
	# 	_len: int = 0
	# 	for keyphrase in self.keyphrases:
	# 		_len += len(keyphrase.attributes)
	# 	return _len

	# @property
	# def relations_len(self) -> int:
	# 	return len(self.relations)

	# def as_ann(self, sentence_id: int, keyphrase_span_shift: int) -> str:
	# 	if not hasattr(self, '_as_ann'):
	# 		self._as_ann: str = CommentAnnotation(f'Sentence {sentence_id}: {self.text}').as_ann()

	# 		if self.keyphrases:
	# 			self._as_ann += '\n' + CommentAnnotation('Keyphrases').as_ann() + '\n'
	# 			self._as_ann += '\n'.join(keyphrase.as_ann(keyphrase_span_shift) for keyphrase in self.keyphrases)

	# 		if self.relations:
	# 			self._as_ann += '\n' + CommentAnnotation('Relations').as_ann() + '\n'
	# 			self._as_ann += '\n'.join(relation.as_ann() for i, relation in enumerate(self.relations))

	# 		if any(keyphrase.attributes for keyphrase in self.keyphrases):
	# 			self._as_ann += '\n' + CommentAnnotation('Attributes').as_ann()
	# 			for keyphrase in self.keyphrases:
	# 				for attribute in keyphrase.attributes:
	# 					self._as_ann += '\n' + attribute.as_ann()

	# 	return self._as_ann