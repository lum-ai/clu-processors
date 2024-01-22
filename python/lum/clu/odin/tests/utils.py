from pydantic import BaseModel
import json
import os
import typing

# Test utilities

class TestCaseMentionsData(BaseModel):
    name: str
    path: str

    @property
    def json_dict(self) -> dict[str, typing.Any]:
        with open(self.path, "r") as infile:
          return json.load(infile)
    
test_cases = [
    TestCaseMentionsData(
        name="old-mentions",
        path=os.path.join(
          os.path.dirname(os.path.realpath(__file__)), 
          "data", 
          "mentions-old.json"
        )
    ),
    TestCaseMentionsData(
        name="overlapping-mentions",
        path=os.path.join(
          os.path.dirname(os.path.realpath(__file__)), 
          "data", 
          "overlapping-mentions.json"
        )
    )
]
