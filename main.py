from ontology_learning.utils import mapper
from ontology_learning.utils.persistance import save_medline_article
from pathlib import Path
from ontology_learning.data_type.annotation.collection import Collection

# with open("../codee/data/mplus_topics_2018-01-09.xml", "r", encoding = "utf8") as f:
#     ordereddict = mapper.xml_to_json(f.read())
#     medline_corpus = mapper.json_to_medlinecorpus(ordereddict)
#     spanish_medline_corpus = (
#         article
#         for article in medline_corpus
#         if article.meta.language == "spanish"
#     )
#     for spanish_medline_article in spanish_medline_corpus:
#         save_medline_article(spanish_medline_article, Path('articles'))

# print(Collection.load_corpus(Path("articles")).sentences)
# print(Collection.load_document(Path("articles/aborto.txt")).sentences)

annotated_corpus = Collection.load_corpus(Path("health-topics"))
corpus = Collection.load_corpus(Path("articles"), keyphrases = False)
print(132)