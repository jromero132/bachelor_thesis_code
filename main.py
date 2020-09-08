from ontology_learning.data_type.annotation.collection import Collection
from ontology_learning.data_type.knowledge_graph.knowledge_graph import KnowledgeGraph
from ontology_learning.utils import mapper
from ontology_learning.utils.knowledge_graph_painter import KnowledgeGraphPainter
from ontology_learning.utils.persistance import save_medline_article
from pathlib import Path

import sys

xml_file_path = Path("data/mplus_topics_2018-01-09.xml")
articles_folder_path = Path("articles")
annotated_corpus_path = Path("medline")

articles_extension = ".txt"
annotation_extension = ".ann"

# print("reading and parsing xml file...")
# with open(xml_file_path, "r", encoding = "utf8") as f:
#     ordereddict = mapper.xml_to_json(f.read())
#     medline_corpus = mapper.json_to_medlinecorpus(ordereddict)
#     spanish_medline_corpus = (
#         article
#         for article in medline_corpus
#         if article.meta.language == "spanish"
#     )
#     for spanish_medline_article in spanish_medline_corpus:
#         save_medline_article(spanish_medline_article, articles_folder_path)

# print("reading annotated corpus...")
# annotated_corpus = Collection.load_corpus(annotated_corpus_path)
# annotated_corpus.sort()
# print("moving annotated sentences to their respective files...")
# for document_path in articles_folder_path.iterdir():
# 	if document_path.suffix == articles_extension:
# 		document = Collection.load_document(document_path, keyphrases = False)
# 		for sentence in document.sentences:
# 			s = annotated_corpus.get_sentence_annotation(sentence.text)
# 			sentence.keyphrases = s.keyphrases
# 			sentence.relations = s.relations

# 		document.fix_ids()
# 		with open(articles_folder_path / f"{document_path.stem}{annotation_extension}", "w+", encoding = "utf8") as f:
# 			f.write(document.as_ann())

print("loading evaluation corpus...")
folder_path = sys.argv[ 1 ]
annotated_corpus = Collection.load_corpus(Path(folder_path))

print("building knowledge graph...")
knowledge_graph = KnowledgeGraph.build(annotated_corpus)

print("painting graph...")
KnowledgeGraphPainter.paint(knowledge_graph)