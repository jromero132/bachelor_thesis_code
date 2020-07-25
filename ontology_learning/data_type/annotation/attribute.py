from .keyphrase import Keyphrase

class Attribute:
	def __init__(self, id: str, keyphrase: "Keyphrase", label: str):
		self.id = id
		self.keyphrase = keyphrase
		self.label = label

	def __repr__(self):
		return f"Attribute(label={self.label})"

	def __str__(self):
		return self.__repr__()

	def __lt__(self, attr):
		if isinstance(attr, Attribute):
			return self.label < attr.label

	def as_ann(self) -> str:
		return f"{self.id}\t{self.label} {self.keyphrase.id}"

	def clone(self):
		return Attribute(self.id, self.keyphrase, self.label)