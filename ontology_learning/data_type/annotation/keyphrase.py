class Keyphrase:
	def __init__(self, id: str, label: str, spans: "List[Tuple(int, int)]", text: str):
		self.id = id
		self.label = label
		self.spans = spans
		self.text = text
		self.attributes: "List[Attribute]" = []

	def __repr__(self):
		return f"Keyphrase(text={self.text}, label={self.label}, id={self.id}, attr={self.attributes})"

	def __str__(self):
		return self.__repr__()

	def as_ann(self, shift: int) -> str:
		return f"{self.id}\t{self.label} {';'.join(f'{start + shift} {end + shift}' for start, end in self.spans)}\t{self.text}"