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

from collections import defaultdict
from itertools import chain, product


lemmatizer = Lemmatizer()
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

		for sentence in collection.sentences:
			node_dic, keyphrases_dic = {}, {}
			for keyphrase in sentence.keyphrases:
				key = keyphrase.clone()
				setattr(key, "lemmatized", lemmatizer.lemmatize(key.text.lower()))
				keyphrases_dic[ key.id ] = key

				node = KnowledgeGraphSimpleNode(key)
				graph.add_node(node)
				if key.attributes: # attributes
					node2 = KnowledgeGraphAttributeNode(node, sorted(key.attributes), key.label)
					graph.add_node(node2)
					graph.add_edge(node2, node, key.label)
					node = node2

				node_dic[ key.id ] = [ node ]


			def is_base_label(label):
				return label in ("Concept", "Reference")

			def is_action_label(label):
				return label == "Action"

			def is_predicate_label(label):
				return label == "Predicate"

			def is_action_relation(label):
				return label in ("subject", "target")

			def is_predicate_relation(label):
				return label in ("domain", "arg")

			def is_context_relation(label):
				return label in ("in-context", "in-place", "in-time")

			def is_taxonomic_relation(label):
				return label in ("is-a", "part-of", "same-as", "has-property")

			def is_causes_or_entails_relation(label):
				return label in ("causes", "entails")


			def groupby(items, func):
				groups = defaultdict(list)
				for item in items:
					groups[ func(item) ].append(item)
				return groups

			def combinations(array):
				return [[ x[ 0 ] for x in array ]]

			def add_multiple_relations(relations):
				v = relations[ 0 ].origin
				v_node = node_dic[ v ]

				nodes = [
					node_dic[ rel.destination ]
					for rel in relations
				]

				result = []
				for w in v_node:
					for combination in product(*nodes):
						node = KnowledgeGraphCompouseNode([ w ] + list(combination), w.type)
						graph.add_edge(node, w, keyphrases_dic[ v ].label)
						for i, node2 in enumerate(combination):
							graph.add_edge(node, node2, relations[ i ].label)

						result.append(node)

				return result

			def add_edges(relations):
				for relation in relations:
					if isinstance(relation, list):
						if len(relation) > 0:
							grouped = groupby(relation, lambda r: r.label)
							label = keyphrases_dic[ relation[ 0 ].origin ].label
							if label == "Action":
								rels = list(chain(*(v for k, v in grouped.items() if not is_action_relation(k))))
								l1, l2 = len(grouped[ "subject" ]), len(grouped[ "target" ])
								res = []
								if l1 > 0 and l2 > 0:
									for r1 in grouped[ "subject" ]:
										for r2 in grouped[ "target" ]:
											res.extend(add_multiple_relations([ r1, r2 ] + rels))

								elif l1 == 0 and l2 > 0:
									for r in grouped[ "target" ]:
										res.extend(add_multiple_relations([ r ] + rels))

								elif l1 > 0 and l2 == 0:
									for r in grouped[ "subject" ]:
										res.extend(add_multiple_relations([ r ] + rels))

								else:
									res.extend(add_multiple_relations(rels))

								node_dic[ relation[ 0 ].origin ] = res

							elif label == "Predicate":
								rels = list(chain(*(v for k, v in grouped.items() if k != "domain")))
								l = len(grouped[ "domain" ])
								res = []

								if l > 0:
									for r in grouped[ "domain" ]:
										res.extend(add_multiple_relations([ r ] + rels))

								else:
									res.extend(add_multiple_relations(rels))

								node_dic[ relation[ 0 ].origin ] = res

							else:
								node_dic[ relation[ 0 ].origin ] = add_multiple_relations(relation)

					else:
						for node1 in node_dic[ relation.origin ]:
							for node2 in node_dic[ relation.destination ]:
								graph.add_edge(node1, node2, relation.label)

								if relation.label == "same-as":
									graph.add_edge(node2, node1, relation.label)

			def get_dag(edges):
				transpose, indegree = defaultdict(list), defaultdict(int)
				for edge in edges:
					indegree[ edge.origin ] += 1
					indegree.setdefault(edge.destination, 0)
					transpose[ edge.destination ].append(edge.origin)

				dag = [ v for v, d in indegree.items() if d == 0 ]
				index = 0
				while index != len(dag):
					v = dag[ index ]
					for w in transpose[ v ]:
						indegree[ w ] -= 1
						if indegree[ w ] == 0:
							dag.append(w)
					index += 1

				if len(dag) != len(transpose):
					raise Exception("Annotated file contains one or more errors")

				return dag

			grouped = groupby(
				sentence.relations,
				lambda r: is_action_relation(r.label) or is_predicate_relation(r.label) or is_context_relation(r.label)
			)
			base_context_relations, relations = grouped[ True ], grouped[ False ]
			dag = get_dag(base_context_relations)
			rels = groupby(base_context_relations, lambda r: r.origin)
			add_edges(rels[ v ] for v in dag)

			grouped = groupby(
				relations,
				lambda r: is_taxonomic_relation(r.label) or is_causes_or_entails_relation(r.label)
			)
			base_relations, relations = grouped[ True ], grouped[ False ]
			add_edges(base_relations)

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