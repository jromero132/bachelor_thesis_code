from ontology_learning.utils.hash import get_hash


class KnowledgeGraphEdge(object):
	def __init__(self, node, label):
		self.node = node
		self.label = label

	def __repr__(self):
		return f"KnowledgeGraphEdge(node={self.node}, label={self.label})"

	def __str__(self):
		return self.__repr__()

	def __eq__(self, other):
		return self.node == other.node and self.label == other.label

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return get_hash(self.__repr__())