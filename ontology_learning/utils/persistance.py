# built-in packages
from pathlib import Path

# own modules
from ontology_learning.data_type.medline.medline_article.medline_article import MedlineArticle


def save_medline_article(
	medline_article: MedlineArticle,
	folder_path: Path,
	*,
	filename: str = None,
	split_by_sentences = True
) -> None:
	absolute_folder_path: Path = Path(folder_path.absolute())
	absolute_file_path = absolute_folder_path / (filename or f"{medline_article.meta.title_slug}.txt")

	if not absolute_folder_path.exists():
		absolute_folder_path.mkdir()

	with open(absolute_file_path, "w+", encoding = "utf8") as f:
		f.write("\n".join(medline_article.sentences) if split_by_sentences else medline_article.text)