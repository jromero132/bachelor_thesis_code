from .annotation_types import (
	Annotation,
	AttributeAnnotation,
	EntityAnnotation,
	EventAnnotation,
	RelationAnnotation,
	SameAsAnnotation
)
from .annotation_file import AnnFile
from .attribute import Attribute
from .keyphrase import Keyphrase
from .relation import Relation
from .sentence import Sentence
from bisect import bisect_left
from itertools import accumulate, chain
from pathlib import Path

import re


class Collection:
	def __init__(self, sentences: list = None) -> None:
		self.sentences = sentences or []

	def __len__(self) -> int:
		return len(self.sentences)

	def __add__(self, c: "'Collection") -> "Collection":
		return Collection(self.sentences + c.sentences)

	@staticmethod
	def load_corpus(
		cpath: Path,
		*,
		legacy: bool = True,
		keyphrases: bool = True,
		relations: bool = True,
		attributes: bool = True,
		extension: (str, tuple, list) = (".txt",)
	) -> "Collection":

		if not isinstance(extension, (tuple, list)):
			extension = (extension,)

		result = Collection()
		offset = [ 0 ] * 3
		for f in cpath.iterdir():
			if f.suffix in extension:
				collection = Collection.load_document(
					f,
					legacy = legacy,
					keyphrases = keyphrases,
					relations = relations,
					attributes = attributes,
				)
				collection.fix_ids()
				new_offset = Collection.increase_ids(collection, *offset)
				offset = [ a + b for a, b in zip(offset, new_offset) ]
				result += collection
		return result

	@staticmethod
	def load_document(
		dpath: Path,
		*,
		legacy: bool = True,
		keyphrases: bool = True,
		relations: bool = True,
		attributes: bool = True,
		sort = False
	) -> "Collection":

		# add sentences from input .txt to Collection
		collection: Collection = Collection(list(Sentence.load_document(dpath)))

		# if keyphrases won't be loaded finish right there
		if not keyphrases:
			return collection

		# else, parse .ann file to start the annotation of sentences
		ann_file_path: "Path" = dpath.parent / (dpath.stem + ".ann")
		ann_file: "AnnFile" = AnnFile.load_document(ann_file_path) if ann_file_path.exists() else AnnFile()

		def add_relation(id: str, source_id: str, destination_id: str, ann_type: str, id_to_keyphrase: "Dict{str:Tuple(keyphrase, int)}"):
			source: "Keyphrase" = id_to_keyphrase[ source_id ]
			destination: "Keyphrase" = id_to_keyphrase[ destination_id ]
			relation: "Relation" = Relation(id, source[ 0 ].id, destination[ 0 ].id, ann_type)
			collection.sentences[ source[ 1 ] ].relations.append(relation)

		# load keyphrases from Entity Annotations
		id_to_keyphrase: "Dict{str:Tuple(keyphrase, int)}" = dict()
		for ann in ann_file.annotations:
			if isinstance(ann, EntityAnnotation):
				sid, spans = Annotation.get_relative_annotation(ann.spans, collection.sentences_boundaries)
				sentence: "Sentence" = collection.sentences[ sid ]
				keyphrase: "Keyphrase" = Keyphrase(ann.id, ann.type, spans, ann.text)
				sentence.keyphrases.append(keyphrase)
				id_to_keyphrase[ ann.id ] = (keyphrase, sid)

		# load standard relations and attributes
		for ann in ann_file.annotations:
			if relations:
				# load relations from Event Annotations (legacy support)
				if legacy and isinstance(ann, EventAnnotation):
					id_to_keyphrase[ ann.id ] = id_to_keyphrase[ ann.ref ]

					for label, destination in ann.args.items():
						label = "".join(i for i in label if not i.isdigit()).lower()
						add_relation(ann.id, ann.ref, destination, label, id_to_keyphrase)

				# load standard relations from Relation Annotations
				elif isinstance(ann, RelationAnnotation):
					add_relation(ann.id, ann.arg1, ann.arg2, ann.type, id_to_keyphrase)

				# load equivalence relations from Same As Annotations
				elif isinstance(ann, SameAsAnnotation):
					source = ann.args[ 0 ]
					for destination in ann.args[ 1: ]:
						add_relation(ann.id, source, destination, ann.type, id_to_keyphrase)

			# load attributes from Attribute Relations
			if attributes and isinstance(ann, AttributeAnnotation):
				keyphrase = id_to_keyphrase[ ann.ref ][ 0 ]
				attribute: "Attribute" = Attribute(ann.id, keyphrase, ann.type)
				keyphrase.attributes.append(attribute)

		if sort:
			collection.sort()

		return collection

	@staticmethod
	def increase_ids(collection, keyphrases_cnt, relations_cnt, attributes_cnt):
		def update_id(obj, *fields):
			for name, value in fields:
				v = getattr(obj, name)
				if re.fullmatch(r"\w\d+", v) is not None:
					_id = int(v[ 1: ])
					setattr(obj, name, f"{v[ 0 ]}{_id + value}")

		keyphrases, relations, attributes = 0, 0, 0
		for sentence in collection.sentences:
			for keyphrase in sentence.keyphrases:
				for attribute in keyphrase.attributes:
					update_id(attribute, ("id", attributes_cnt))
					attributes += 1

				update_id(keyphrase, ("id", keyphrases_cnt))
				keyphrases += 1

			for relation in sentence.relations:
				update_id(relation, ("id", relations), ("origin", keyphrases_cnt), ("destination", keyphrases_cnt))
				relations += 1
		return keyphrases, relations, attributes

	def sort(self):
		for sentence in self.sentences:
			sentence.sort()
		self.sentences.sort(key = lambda s: s.text)

	@property
	def sentences_boundaries(self) -> "List[int]":
		_property_name = "_sentences_boundaries"
		if not hasattr(self, _property_name):
			self.__setattr__(_property_name, list(accumulate(chain([ 0 ], [ len(s) for s in self.sentences ]), lambda l1, l2: l1 + l2 + 1)))
		return self.__getattribute__(_property_name)

	def get_sentence_annotation(self, sentence: str) -> Sentence: #? better to do it with a trie
		index = bisect_left(self.sentences, sentence)
		if index < len(self.sentences) and self.sentences[ index ].text == sentence:
			return self.sentences[ index ]

		else:
			return Sentence(sentence)

	def as_ann(self) -> str:
		ann = "\n\n".join(
			sentence.as_ann(i + 1, self.sentences_boundaries[ i ])
			for i, sentence in enumerate(self.sentences)
		)
		return ann

	def fix_ids(self):
		keyphrases_dict: "Dict{str:str}" = dict()
		attributes_count: int = 0
		relations_count: int = 0

		for sentence in self.sentences:
			for keyphrase in sentence.keyphrases:
				_id: str = keyphrase.id

				if _id in keyphrases_dict:
					keyphrase.id = keyphrases_dict[ _id ]

				else:
					keyphrases_dict[ _id ] = keyphrase.id = f'T{len(keyphrases_dict) + 1}'

				for attribute in keyphrase.attributes:
					attributes_count += 1
					attribute.id = f'A{attributes_count}'

			for relation in sentence.relations:
				relation.origin = keyphrases_dict[ relation.origin ]
				relation.destination = keyphrases_dict[ relation.destination ]

			sentence.sort()

			for relation in sentence.relations:
				if relation.is_same_as_relation:
					continue

				relations_count += 1
				relation.id = f"R{relations_count}"
