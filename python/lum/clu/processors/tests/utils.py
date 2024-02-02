from pathlib import Path
from lum.clu.processors.document import Document as CluDocument
import json
import typing

__all__ = ["load_test_docs"]


def load_test_docs(filenames: list[str] = ["doc-part-1.json", "doc-part-2.json", "doc-part-3.json"]) -> typing.Iterator[CluDocument]:
  for filename in filenames:
    f = Path(__file__).resolve().parent / "data" / filename
    with open(f, "r") as infile:
      data = json.load(infile)
      yield CluDocument(**data)