import re
import unidecode


def decode(text: str) -> str:
	return unidecode.unidecode(text)

def slugify(text: str) -> str:
	decoded_text: str = decode(text)
	lowercased_text: str = decoded_text.lower()
	slugified_text: str = re.sub(r"[\W_]+", "-", lowercased_text)
	stripped_text = slugified_text.strip("-")
	return stripped_text