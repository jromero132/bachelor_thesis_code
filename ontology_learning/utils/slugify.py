import re


def decode(text: str) -> str:
	return text

def slugify(text: str) -> str:
	lowercased_text: str = text.lower()
	decoded_text: str = decode(lowercased_text)
	slugified_text: str = re.sub(r"[\W_]+", "-", decoded_text)
	stripped_text = slugified_text.strip()
	return stripped_text