from lum.clu.processors.document import Document as CluDocument
from lum.clu.processors.tests.utils import load_test_docs, check_doc_token_alignment
import pytest
import typing

def test_merge_documents_1():
  """Test case 1 for Document.merge_documents()"""
  docs: list[CluDocument] = list(load_test_docs(["example-1-part-0.json", "example-1-part-1.json", "example-1-part-2.json"]))
  doc = CluDocument.merge_documents(docs)
  check_doc_token_alignment(doc)


def test_merge_documents_2():
  """Test case 2 for Document.merge_documents()"""
  docs: list[CluDocument] = list(load_test_docs([f"example-2-part-{i}.json" for i in range(43)]))
  doc = CluDocument.merge_documents(docs)
  check_doc_token_alignment(doc)
