from __future__ import annotations
from pydantic import BaseModel, Field
import typing

__all__ = ["Interval"]

class Interval(BaseModel):
    """Defines a token or character span"""
    start: int = Field(description="The token or character index where the interval begins.")
    end: int = Field(description="1 + the index of the last token/character in the span.")

    """
    Methods
    -------
    contains(that)
        Test whether `that` (int or Interval) overlaps with span of this Interval.

    overlaps(that)
        Test whether this Interval contains another.  Equivalent Intervals will overlap.
    """

    # def __init__(self, start, end):
    #     NLPDatum.__init__(self)
    #     assert (start < end), "Interval start must precede end."
    #     self.start = start
    #     self.end = end

    # def to_JSON_dict(self):
    #     return {"start":self.start, "end":self.end}

    @property
    def size(self) -> int:
      """The size of an Interval"""
      return self.end - self.start

    @property
    def __len__(self) -> int:
      """The size of an Interval"""
      return self.size

    def contains(self, other: typing.Union[int, Interval]) -> bool:
        """Test whether `other` (int or Interval) overlaps with span of this Interval."""
        if isinstance(other, int):
          return self.start <= other <= self.end 
        # self.__class__
        elif isinstance(other, Interval):
           return self.start <= other.start and self.end >= other.end
        return False

    def __contains__(self, other: typing.Union[int, Interval]):
       return self.contains(other)

    def overlaps(self, other: typing.Union[int, Interval]) -> bool:
      """Test whether this Interval contains another.  Equivalent Intervals will overlap."""
      if isinstance(other, int):
          return self.start <= other < self.end
      # self.__class__
      elif isinstance(other, Interval):
          return ((other.start <= self.start < other.end) or (self.start <= other.start < self.end))
      return False