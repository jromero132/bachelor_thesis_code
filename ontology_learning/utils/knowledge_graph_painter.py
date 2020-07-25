from ontology_learning.data_type.knowledge_graph.knowledge_graph_node import (
	KnowledgeGraphSimpleNode,
	KnowledgeGraphAttributeNode,
	KnowledgeGraphCompouseNode
)
from graphviz import Digraph
# import matplotlib.pyplot as plt
# import networkx as nx


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
		# cf = plt.gcf() # current frame
		# if cf._axstack() is None:
		# 	ax = cf.add_axes((0, 0, 1, 1)) # axis

		# else:
		# 	ax = cf.gca() # axis

		# ax.set_axis_off()
		# cf.canvas.set_window_title(title)

		nodes = KnowledgeGraphPainter.get_nodes(knowledge_graph)
		edges = KnowledgeGraphPainter.get_edges(knowledge_graph)

		# graph = nx.DiGraph()
		graph = Digraph(
			name = 'Knowledge Graph',
			filename = "knowledge_graph.gv",
			format = "png"
		)
		# graph.add_nodes_from(node.id for node in nodes)
		# graph.add_edges_from(KnowledgeGraphPainter.get_edges(knowledge_graph))

		# pos = nx.spring_layout(graph) # pos
		# nx.draw(graph, with_labels = True)
		# nx.draw_networkx_nodes(
		# 	graph,
		# 	pos = pos,
		# 	ax = ax,
		# 	node_size = [ node.node_size for node in nodes ],
		# 	node_color = [ node.color for node in nodes ],
		# 	node_shape = node_shape
		# )

		# nx.draw_networkx_labels(
		# 	graph,
		# 	pos = pos,
		# 	ax = ax,
		# 	labels = { node.id: node.label for node in nodes },
		# 	font_size = node_font_size,
		# 	font_color = node_label_font_color,
		# 	font_family = node_font_family,
		# 	font_weight = node_label_font_weight
		# )

		# if zoomed:
		# 	mng = plt.get_current_fig_manager()
		# 	mng.window.state("zoomed")

		# plt.show()

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
