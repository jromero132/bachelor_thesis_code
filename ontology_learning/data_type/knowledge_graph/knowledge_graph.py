from .knowledge_graph_node import (
	KnowledgeGraphNode,
	KnowledgeGraphSimpleNode,
	KnowledgeGraphAttributeNode,
	KnowledgeGraphCompouseNode
)
from .knowledge_graph_edge import KnowledgeGraphEdge

from ..annotation.attribute import Attribute
from ..annotation.keyphrase import Keyphrase
from ..annotation.relation import Relation
from ontology_learning.utils.lemmatizer import Lemmatizer


class KnowledgeGraph(object):
	def __init__(self):
		self.nodes = {}

	def add_node(self, node):
		if node.label not in self.nodes:
			self.nodes[ node.label ] = node

	def add_edge(self, from_node, to_node, label):
		if from_node.label not in self.nodes:
			self.add_node(from_node)

		if to_node.label not in self.nodes:
			self.add_node(to_node)

		self.nodes[ from_node.label ].add_edge(to_node, label)
		self.nodes[ to_node.label ].add_reversed_edge(from_node, label)

	def get_node_from_keyphrase(self, keyphrase):
		return self.nodes.get(keyphrase.lemmatized, None)

	def get_nodes(self):
		return iter(self.nodes.values())

	def get_edges(self):
		for node in self.nodes.values():
			for edge in node.edges:
				yield node, edge

	@staticmethod
	def build(collection):
		graph = KnowledgeGraph()
		lemmatizer = Lemmatizer()

		for sentence in collection.sentences:
			node_dic, keyphrases_dic = {}, {}
			for keyphrase in sentence.keyphrases:
				key = keyphrase.clone()
				setattr(key, "lemmatized", lemmatizer.lemmatize(key.text))
				keyphrases_dic[ key.id ] = key

				node = KnowledgeGraphSimpleNode(key)
				graph.add_node(node)
				if key.attributes:
					node2 = KnowledgeGraphAttributeNode(node, sorted(key.attributes), key.label)
					graph.add_node(node2)
					graph.add_edge(node2, node, key.label)
					node = node2

				node_dic[ key.id ] = node

			rel_group1, rel_group2, rel_group3 = _group_relations(sentence.relations, keyphrases_dic)

			def add_relations_by_group(rel_group):
				rel_group = sorted(rel_group, key = lambda r: r.origin)
				i = 0
				while i < len(rel_group):
					cnt = 1
					while i + cnt < len(rel_group) and rel_group[ i ].origin == rel_group[ i + cnt ].origin:
						cnt += 1

					relations = rel_group[ i:i + cnt ]

					node = KnowledgeGraphCompouseNode([ node_dic[ rel_group[ i ].origin ] ] + [
							node_dic[ rel.destination ]
							for rel in relations
						],
						node_dic[ rel_group[ i ].origin ].type
					)

					graph.add_edge(node, node_dic[ rel_group[ i ].origin ], keyphrases_dic[ rel_group[ i ].origin ].label)

					for rel in relations:
						node2 = node_dic[ rel.destination ]
						graph.add_edge(node, node2, rel.label)

					node_dic[ rel_group[ i ].origin ] = node

					i += cnt

			add_relations_by_group(rel_group1)
			add_relations_by_group(rel_group2)

			for rel in rel_group3:
				node1 = node_dic[ rel.origin ]
				node2 = node_dic[ rel.destination ]
				graph.add_edge(node1, node2, rel.label)

				if rel.label == "same-as":
					graph.add_edge(node2, node1, rel.label)

		return graph

relations_groups = (
	lambda r, keys: r.label in ("arg", "domain")
				or (r.label in ("in-context", "in-place", "in-time") and keys[ r.origin ].label == "Predicate"),
	lambda r, keys: r.label in ("in-context", "in-place", "in-time", "subject", "target"),
	lambda r, keys: r.label in ("is-a", "part-of", "same-as", "has-property", "causes", "entails")
)
def _group_relations(relations, keyphrases):
	result = [ [] for _ in range(len(relations_groups)) ]
	for relation in relations:
		index = next(i for i, func in enumerate(relations_groups) if func(relation, keyphrases))

		if index is None:
			raise Exception(f"relation type `{type(relation)}` with `{relation}` is not recognized")

		result[ index ].append(relation)

	return result