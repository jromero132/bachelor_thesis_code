from ..annotation.attribute import Attribute
from ..annotation.relation import Relation
from .knowledge_graph_edge import KnowledgeGraphEdge
from ontology_learning.utils.hash import get_hash

class KnowledgeGraphNode(object):
	def __init__(self, label, type_):
		self.label = " ".join(sorted(set(label.split(" "))))
		self.type = type_
		self.edges = set()
		self.reversed_edges = set()

	def __repr__(self):
		return f"{type(self).__name__}(label={self.label}, type={self.type})"

	def __str__(self):
		return self.__repr__()

	def __eq__(self, other):
		return self.label == other.label and self.type == other.type

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return get_hash(self.__repr__())

	def add_edge(self, to_node, label = ""):
		self.edges.add(KnowledgeGraphEdge(to_node, label))

	def add_reversed_edge(self, to_node, label = ""):
		self.reversed_edges.add(KnowledgeGraphEdge(to_node, label))

class KnowledgeGraphSimpleNode(KnowledgeGraphNode):
	def __init__(self, keyphrase):
		super(KnowledgeGraphSimpleNode, self).__init__(keyphrase.lemmatized, keyphrase.label)
		self.keyphrase = keyphrase

class KnowledgeGraphAttributeNode(KnowledgeGraphNode):
	def __init__(self, node, attributes, type_):
		def get_attribute_label(label):
			_label = label.lower()
			if _label == "uncertain":
				return "?"
			elif _label == "negated":
				return "¬"
			elif _label == "diminished":
				return "↓"
			elif _label == "emphasized":
				return "↑"
			return label

		super(KnowledgeGraphAttributeNode, self).__init__(
			" ".join([ get_attribute_label(a.label) for a in attributes ] + [ node.label ]),
			type_
		)
		self.node = node
		self.attributes = list(attributes)

class KnowledgeGraphCompouseNode(KnowledgeGraphNode):
	def __init__(self, nodes, type_):
		super(KnowledgeGraphCompouseNode, self).__init__(" ".join(node.label for node in nodes), type_)
		self.nodes = list(nodes)