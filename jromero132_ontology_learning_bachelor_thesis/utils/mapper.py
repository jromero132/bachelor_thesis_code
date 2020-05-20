import xmltodict


class Mapper:
    @staticmethod
    def xml_to_ordereddict(xml_text):
        return xmltodict.parse(xml_text)