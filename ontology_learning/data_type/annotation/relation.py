class Relation:
	def __init__(self, id: str, origin: str, destination: str, label: str):
		self.id = id
		self.origin = origin
		self.destination = destination
		self.label = label

	def __repr__(self):
		return f"Relation(from={self.origin}, to={self.destination}, label={self.label})"

	def __str__(self):
		return self.__repr__()

	@property
	def is_same_as_relation(self) -> bool:
		return self.label == "same-as"

	def as_ann(self) -> str:
		if self.is_same_as_relation:
			return f"{self.id}\t{self.label} {self.origin} {self.destination}"

		else:
			return f"{self.id}\t{self.label} Arg1:{self.origin} Arg2:{self.destination}"