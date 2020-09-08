from ontology_learning.data_type.knowledge_graph.knowledge_graph_node import (
	KnowledgeGraphSimpleNode,
	KnowledgeGraphAttributeNode,
	KnowledgeGraphCompouseNode
)
from graphviz import Digraph


class NodeProperties():
	def __init__(self, id_, label, type_, color, node_size, font_size):
		self.id = id_
		self.label = label
		self.type = type_
		self.color = color
		self.node_size = node_size
		self.font_size = font_size

class EdgeProperties():
	def __init__(self, from_node, to_node, label):
		self.from_node = from_node
		self.to_node = to_node
		self.label = label

class KnowledgeGraphPainter:
	@staticmethod
	def paint(
		knowledge_graph,
		*,
		title = "Grafo de Conocimiento",
		zoomed = True,
		node_font_family = "monospace",
		node_font_size = 9
	):
		nodes = KnowledgeGraphPainter.get_nodes(knowledge_graph)
		edges = KnowledgeGraphPainter.get_edges(knowledge_graph)

		graph = Digraph(
			name = "Knowledge Graph",
			filename = "knowledge_graph",
			format = "png"
		)

		for node in nodes:
			graph.attr("node", style = "filled", color = "black", fillcolor = node.color)
			graph.node(node.label)

		graph.attr("edge", fontsize = "12", fontcolor = "black")
		for edge in edges:
			graph.edge(
				edge.from_node,
				edge.to_node,
				label = f" {edge.label} "
			)

		graph.view()

	@staticmethod
	def get_nodes(knowledge_graph):
		color_dic = {
			"Action": "#ffbdbd",
			"Concept": "#caffbb",
			"Predicate": "#fffba6",
			"Reference": "#c3c3c3"
		}

		return [
			NodeProperties(
				id_ = node.label,
				label = node.label,
				type_ = node.type,
				color = color_dic[ node.type ],
				node_size = 300 * len(node.label),
				font_size = 12
			)
			for node in knowledge_graph.get_nodes()
		]

	@staticmethod
	def get_edges(knowledge_graph):
		return [
			EdgeProperties(
				from_node = node.label,
				to_node = edge.node.label,
				label = edge.label
			)
			for node, edge in knowledge_graph.get_edges()
		]
