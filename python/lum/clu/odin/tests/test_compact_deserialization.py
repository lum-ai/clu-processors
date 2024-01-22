from lum.clu.odin.serialization import OdinJsonSerializer
from .utils import test_cases
import pytest
import typing

def test_load_compact_json():
  """Test case for OdinJsonSerializer.from_compact_mentions_json()"""
  for tc in test_cases:
    compact_json: dict[str, typing.Any] = tc.json_dict
    expected = len(compact_json.get("mentions", []))
    mentions = OdinJsonSerializer.from_compact_mentions_json(compact_json)
    #print(f"Expected to load {expected} mentions from {tc.name}. Found {len(mentions)}\n")
    assert len(mentions) == expected, f"Expected to load {expected} mentions from {tc.name}, but {len(mentions)} found"