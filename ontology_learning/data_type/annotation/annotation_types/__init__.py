# from pathlib import Path
# import os

# # for fpath in Path(__file__).parent.iterdir():
# # 	print(fpath)
# # 	if fpath.suffix == ".py" and fpath.name != "__init__.py":
# # 		print(str(fpath))
# # 		__import__(f"{fpath.stem}", fromlist=["*"])

# __import__("entity_annotation", fromlist=["*"])
from .annotation import Annotation
from .entity_annotation import EntityAnnotation
from .relation_annotation import RelationAnnotation
from .attribute_annotation import AttributeAnnotation
from .comment_annotation import CommentAnnotation
from .event_annotation import EventAnnotation
from .same_as_annotation import SameAsAnnotation