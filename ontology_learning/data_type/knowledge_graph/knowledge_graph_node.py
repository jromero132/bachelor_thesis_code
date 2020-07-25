from ..annotation.attribute import Attribute
from ..annotation.relation import Relation
from .knowledge_graph_edge import KnowledgeGraphEdge

class KnowledgeGraphNode(object):
	def __init__(self, label, type_):
		self.label = label
		self.type = type_
		self.edges = set()
		self.reversed_edges = set()

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
		super(KnowledgeGraphAttributeNode, self).__init__(
			" ".join([ node.label ] + [ a.label for a in attributes ]),
			type_
		)
		self.node = node
		self.attributes = list(attributes)

class KnowledgeGraphCompouseNode(KnowledgeGraphNode):
	def __init__(self, nodes, type_):
		super(KnowledgeGraphCompouseNode, self).__init__(" ".join(node.label for node in nodes), type_)
		self.nodes = list(nodes)