from typing import OrderedDict

import xmltodict


def xml_to_json(xml_text: str) -> OrderedDict:
    """Converts xml text to json.

    Args:
        xml_text (str): xml text to be parsed

    Returns:
        OrderedDict: an ordered dict representing the xml text as json

    Raises:
    """
    return xmltodict.parse(xml_text)