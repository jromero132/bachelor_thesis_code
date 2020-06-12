# built-in packages
from typing import OrderedDict

import re

# third party packages
import xmltodict

# own modules
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

def _html_text_sanitizer(html: str) -> str:
    """Removes all tags in an html text

    Args:
        html (str): html text to remove tags

    Returns:
        str: html text without tags
    """
    text: str = re.sub(r"<.+?>", "", html)
    lines: list = re.split(r"\r+", text)
    sanitized_lines: list = (
        re.sub(r"\s{2,}", " ", line).strip()
        for line in lines
    )
    return "\n".join(sanitized_lines)

def json_to_medlinearticle(json_dict: dict) -> MedlineArticle:
    """Converts a medline article from json to MedlineArticle

    Args:
        json_dict (OrderedDict): json representing a medline article

    Returns:
        MedlineArticle: medline article object
    """
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
    """Converts all medline articles in json to a MedlineCorpus

    Args:
        json_dict (OrderedDict): json with medline articles

    Returns:
        MedlineCorpus: medline corpus with all articles in json
    """
    health_topics: OrderedDict = json_dict[ "health-topics" ]
    return  MedlineCorpus(
                date_generated = health_topics[ "@date-generated" ],
                articles = [
                    json_to_medlinearticle(article)
                    for article in health_topics[ "health-topic" ]
                ]
            )