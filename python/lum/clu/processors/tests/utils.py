from pathlib import Path
from lum.clu.processors.document import Document as CluDocument
import json
import typing

__all__ = ["load_test_docs", "check_doc_token_alignment"]


def load_test_docs(filenames: list[str] = ["doc-part-1.json", "doc-part-2.json", "doc-part-3.json"]) -> typing.Iterator[CluDocument]:
  for filename in filenames:
    f = Path(__file__).resolve().parent / "data" / filename
    with open(f, "r") as infile:
      data = json.load(infile)
      yield CluDocument(**data)

def check_doc_token_alignment(doc: CluDocument):
  for i, s in enumerate(doc.sentences):
    for raw_tok, start, end in zip(s.raw, s.start_offsets, s.end_offsets):
      orig_tok = doc.text[start:end]
      assert orig_tok == raw_tok, f"Expected '{orig_tok}' == '{raw_tok}' for doc[{start}:{end}] and sentence {i} ({' '.join(s.raw)})"