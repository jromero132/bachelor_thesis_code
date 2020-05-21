# built-in libraries
from typing import OrderedDict

import re

# third party libraries
import xmltodict

# module libraries
from ontology_learning.data_type.medline.medline_article import MedlineArticle
from ontology_learning.data_type.medline.medline_article.medline_article_metadata import MedlineArticleMetadata
from ontology_learning.data_type.medline.medline_corpus import MedlineCorpus


def xml_to_json(xml_text: str) -> OrderedDict:
    """Converts xml text to json.

    Args:
        xml_text (str): xml text to be parsed

    Returns:
        OrderedDict: an ordered dict representing the xml text as json
    """
    return xmltodict.parse(xml_text)

def _html_text_sanitizer(html):
    text = re.sub(r"<.+?>", "", html)
    lines = re.split(r"\r+", text)
    sanitized_lines = (re.sub(r"\s{2,}", " ", line).strip() for line in lines)
    return "\n".join(sanitized_lines)

def json_to_medlinearticle(json_dict: dict) -> MedlineArticle:
    return MedlineArticle(
        text = _html_text_sanitizer(json_dict.get("full-summary", None)),
        meta = MedlineArticleMetadata(
            url = json_dict.get("@url", None),
            language = json_dict.get("@language", None),
            title = json_dict.get("@title", None),
            description = json_dict.get("@meta-desc", None),
            id = json_dict.get("@id", None),
            date_created = json_dict.get("@date-created", None),
            also_called = json_dict.get("also-called", []),
        )
    )

def json_to_medlinecorpus(json_dict: dict) -> MedlineCorpus:
    """

    Args:

    Returns:
    """
    health_topics = json_dict[ "health-topics" ]
    print(health_topics["health-topic"][0].keys())
    return  MedlineCorpus(
                date_generated = health_topics[ "@date-generated" ],
                articles = [
                    json_to_medlinearticle(article)
                    for article in health_topics[ "health-topic" ]
                ]
            )