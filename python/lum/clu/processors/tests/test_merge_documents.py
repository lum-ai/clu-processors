from lum.clu.processors.document import Document as CluDocument
from lum.clu.processors.tests.utils import load_test_docs
import pytest
import typing

def test_merge_documents():
  """Test case for Document.merge_documents()"""
  docs: list[CluDocument] = list(load_test_docs(["doc-part-1.json", "doc-part-2.json", "doc-part-3.json"]))
  doc = CluDocument.merge_documents(docs)
  for s in doc.sentences:
    for raw_tok, start, end in zip(s.raw, s.start_offsets, s.end_offsets):
      orig_tok = doc.text[start:end]
      assert orig_tok == raw_tok, f"Expected {orig_tok} == {raw_tok}"