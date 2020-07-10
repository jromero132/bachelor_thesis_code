from abc import abstractstaticmethod
from bisect import bisect


class Annotation:
	def __init__(self, id_: str, typ: str):
		self.id = id_
		self.type = typ

	@abstractstaticmethod
	def try_parse(line: str) -> bool:
		pass

	@abstractstaticmethod
	def parse(line: str) -> "Annotation":
		pass

	@abstractstaticmethod
	def as_ann(self) -> str:
		pass

	@staticmethod
	def get_relative_annotation(spans: "SortedList[Tuple(int,int)]", sentences_length: "SortedList[int]") -> "Tuple(int, List[Tuple(int, int)])":
	    index: int = bisect(sentences_length, spans[ 0 ][ 0 ]) - 1
	    new_spans: "List[Tuple(int, int)]" = list(
			map(
				lambda span:
					(span[ 0 ] - sentences_length[ index ], span[ 1 ] - sentences_length[ index ]),
					spans
			)
		)
	    return index, new_spans