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

			# for rel in sentence.relations:
			# 	k1, k2 = keyphrases_dic[ rel.origin ], keyphrases_dic[ rel.destination ]
			# 	n1, n2 = node_dic[ k1 ], node_dic[ k2 ]
			# 	if is_base_label(k1.label) and is_base_label(k2.label):
			# 		if is_context_relation(rel.label):
			# 			node = KnowledgeGraphCompouseNode([ n1, n2 ], rel.type)
			# 			graph.add_edge(node, n1, k1.label)
			# 			graph.add_edge(node, n2, rel.label)
			# 			node_dic[ k1 ] = node

			# 		else:
			# 			graph.add_edge(node, n1, k1.label)


			# rel_group1, rel_group2, rel_group3 = _group_relations(sentence.relations, keyphrases_dic)

			# def add_relations_by_group(rel_group, main_edge_types = []):
			# 	# rel_group = sorted(rel_group, key = lambda r: r.origin)
			# 	# i = 0
			# 	# while i < len(rel_group):
			# 	# 	cnt = 1
			# 	# 	while i + cnt < len(rel_group) and rel_group[ i ].origin == rel_group[ i + cnt ].origin:
			# 	# 		cnt += 1

			# 	# 	relations = rel_group[ i:i + cnt ]

			# 	# 	node = KnowledgeGraphCompouseNode([ node_dic[ rel_group[ i ].origin ] ] + [
			# 	# 			node_dic[ rel.destination ]
			# 	# 			for rel in relations
			# 	# 		],
			# 	# 		node_dic[ rel_group[ i ].origin ].type
			# 	# 	)

			# 	# 	graph.add_edge(node, node_dic[ rel_group[ i ].origin ], keyphrases_dic[ rel_group[ i ].origin ].label)

			# 	# 	for rel in relations:
			# 	# 		node2 = node_dic[ rel.destination ]
			# 	# 		graph.add_edge(node, node2, rel.label)

			# 	# 	node_dic[ rel_group[ i ].origin ] = node

			# 	# 	i += cnt

			# 	adjacency, transpose, deg = {}, {}, {}
			# 	for relation in rel_group:
			# 		if relation.origin in adjacency:
			# 			adjacency[ relation.origin ].append(relation)

			# 		else:
			# 			adjacency[ relation.origin ] = [ relation ]

			# 		if relation.destination not in adjacency:
			# 			adjacency[ relation.destination ] = []


			# 		if relation.origin not in deg:
			# 			deg[ relation.origin ] = 0

			# 		if relation.destination not in deg:
			# 			deg[ relation.destination ] = 0

			# 		print(relation.label)
			# 		if relation.label in main_edge_types:
			# 			deg[ relation.origin ] += 1


			# 		if relation.destination in transpose:
			# 			transpose[ relation.destination ].append(relation)

			# 		else:
			# 			transpose[ relation.destination ] = [ relation ]

			# 		if relation.origin not in transpose:
			# 			transpose[ relation.origin ] = []

			# 	print(adjacency)
			# 	print(transpose)
			# 	print(deg)

			# 	processed = set()

			# 	# while len(processed) != len(adjacency):
			# 	dag = [ id_ for id_, d in deg.items() if d == 0 and id_ not in processed ]
			# 	while len(dag) > 0:
			# 		id_ = dag[ 0 ]
			# 		dag.pop(0)
			# 		processed.add(id_)

			# 		if len(adjacency[ id_ ]) > 0:
			# 			node = KnowledgeGraphCompouseNode([ node_dic[ id_ ] ] + [
			# 					node_dic[ rel.destination ]
			# 					for rel in adjacency[ id_ ]
			# 				],
			# 				node_dic[ id_ ].type
			# 			)

			# 			graph.add_edge(node, node_dic[ id_ ], keyphrases_dic[ id_ ].label)

			# 			for rel in adjacency[ id_ ]:
			# 				node2 = node_dic[ rel.destination ]
			# 				graph.add_edge(node, node2, rel.label)

			# 			node_dic[ id_ ] = node

			# 		for rel in transpose[ id_ ]:
			# 			if rel.label in main_edge_types:
			# 				deg[ rel.origin ] -= 1
			# 				if deg[ rel.origin ] == 0:
			# 					dag.append(rel.origin)

			# 	# for v in adjacency:
			# 	# 	if v not in processed:
			# 	# 		visited = {}
			# 	# 		queue = [ v ]
			# 	# 		visited[ v ] = (None, 0)
			# 	# 		while len(queue) > 0:
			# 	# 			node = queue[ 0 ]
			# 	# 			queue.pop(0)
			# 	# 			for rel in transpose[ node ]:
			# 	# 				if rel.origin not in visited:
			# 	# 					queue.append(rel.origin)
			# 	# 					visited[ rel.origin ] = (node, visited[ node ][ 1 ] + 1)

			# 	# 		shortest_cycle, start = 10 ** 10, None
			# 	# 		for rel in adjacency[ v ]:
			# 	# 			if rel.destination in visited:
			# 	# 				stat = visited[ rel.destination ]
			# 	# 				if stat[ 1 ] + 1 < shortest_cycle:
			# 	# 					start, shortest_cycle = rel.destination, stat[ 1 ] + 1

			# 	print(processed, len(adjacency))
			# 	# print(node_dic)
			# 	# exit()

			# add_relations_by_group(rel_group1)
			# add_relations_by_group(rel_group2, [ "subject", "target" ])

			# for rel in rel_group3:
			# 	node1 = node_dic[ rel.origin ]
			# 	node2 = node_dic[ rel.destination ]
			# 	graph.add_edge(node1, node2, rel.label)

			# 	if rel.label == "same-as":
			# 		graph.add_edge(node2, node1, rel.label)

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