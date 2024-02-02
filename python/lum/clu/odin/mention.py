# -*- coding: utf-8 -*-
from __future__ import annotations
from pydantic import BaseModel, Field
from lum.clu.processors.document import Document
from lum.clu.processors.sentence import Sentence
from lum.clu.processors.interval import Interval
from lum.clu.odin.synpath import SynPath
import re
import typing


__all__ = ["Mention", "TextBoundMention", "RelationMention", "EventMention", "CrossSentenceMention"]

# MentionTypes = typing.Union[TextBoundMention, EventMention, RelationMention, CrossSentenceMention]

class Mention(BaseModel):

  Paths: typing.ClassVar[typing.TypeAlias] = dict[str, dict["Mention", SynPath]]

  Arguments: typing.ClassVar[typing.TypeAlias] = dict[str, list["Mention"]]
  # FIXME: add validation that this is non-empty?
  labels: list[str] = Field(description="A sequence of labels for this mention. The first label in the sequence is considered the default.")
  # alias="tokenInterval", 
  # TODO: consider adding https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name
  token_interval: Interval  = Field(description="The interval of token indicess that form this mention.")
  # alias="sentence", 
  sentence_index: int = Field(description="The index of the sentence where this mention occurs.")

  document: Document = Field(description="The document where this mention occurs")

  keep: bool = Field(default=True, description="Should we report this mention at the end?")

  arguments: typing.Optional[Mention.Arguments] = Field(default=None, description="A map from argument name to a sequence of mentions. The value of the map is a sequence because there are events that can have several arguments with the same name. For example, in the biodomain, Binding may have several themes.")

  paths: typing.Optional[Paths] = Field(default=None, description="Graph traversal leading to each argument")
  # alias="foundBy"
  found_by: str = Field(default="unknown", description="The name of the rule that produced this mention")

  def copy(
    self,
    maybe_labels: typing.Optional[list[str]] = None,
    maybe_token_interval: typing.Optional[Interval] = None,
    maybe_sentence_index: typing.Optional[int] = None,
    maybe_document: typing.Optional[Document] = None,
    maybe_keep: typing.Optional[bool] = None,
    maybe_arguments: typing.Optional[Mention.Arguments] = None,
    maybe_paths: typing.Optional[Mention.Paths] = None,
    maybe_found_by: typing.Optional[str] = None,
  ) -> Mention:
    return Mention(
      labels = maybe_labels or self.labels,
      token_interval = maybe_token_interval or self.token_interval,
      sentence_index = maybe_sentence_index or self.sentence_index,
      document = maybe_document or self.document,
      keep = maybe_keep or self.keep,
      arguments = maybe_arguments or self.arguments,
      paths = maybe_paths or self.paths,
      found_by = maybe_found_by or self.found_by
    )

  @property
  def label(self) -> str:
    """the first label for the mention"""
    return self.labels[0]
    
  @property
  def start(self) -> int:
    """index of the first token in the mention"""
    return self.token_interval.start

  @property
  def end(self) -> int:
    """one after the last token in the mention"""
    return self.token_interval.end
  
  @property
  def sentence_obj(self) -> Sentence:
    return self.document.sentences[self.sentence_index]

  @property
  def sentenceObj(self) -> Sentence:
    self.sentence_obj

  @property
  def start_offset(self) -> int:
    """character offset of the mention beginning"""
    return self.sentence_obj.start_offsets[self.start]

  @property
  def startOffset(self) -> int:
    """character offset of the mention beginning"""
    return self.start_offset 

  @property
  def char_start_offset(self) -> int:
    """character offset of the mention beginning"""
    return self.start_offset 
  
  @property
  def end_offset(self) -> int:
    """character offset of the mention end"""
    return self.sentence_obj.end_offsets[self.end - 1]

  @property
  def endOffset(self) -> int:
    """character offset of the mention end"""
    return self.end_offset 

  @property
  def char_end_offset(self) -> int:
    """character offset of the mention end"""
    return self.end_offset 
  
  @property
  def is_valid(self) -> bool:
    """returns true if this is a valid mention"""
    return True

  @property
  def isValid(self) -> bool:
    """returns true if this is a valid mention"""
    return self.is_valid

  def matches(self, label_or_pattern: typing.Union[str, re.Pattern]) -> bool:
    """returns true if `label_or_pattern` matches any of the mention labels"""
    if isinstance(label_or_pattern, str):
      return label_or_pattern in self.labels
    elif isinstance(label_or_pattern, re.Pattern):
      patt = label_or_pattern
      return True if any(re.match(patt, lbl) != None for lbl in self.labels) else False
    return False

  @property
  def raw(self) -> list[str]:
    """returns all raw (original, no processing applied) tokens in mention"""
    return self.sentence_obj.raw[self.start:self.end]

  @property
  def words(self) -> list[str]:
    """returns all tokens in mention"""
    return self.sentence_obj.words[self.start:self.end]

  @property
  def tags(self) -> typing.Optional[list[str]]:
    """returns all tags in mention"""
    if self.sentence_obj.tags:
      return self.sentence_obj.tags[self.start:self.end]
    return None
  
  @property
  def lemmas(self) -> typing.Optional[list[str]]:
    """returns all lemmas in mention"""
    if self.sentence_obj.lemmas:
      return self.sentence_obj.lemmas[self.start:self.end]
    return None
  
  @property
  def entities(self) -> typing.Optional[list[str]]:
    """returns all entities in mention"""
    if self.sentence_obj.entities:
      return self.sentence_obj.entities[self.start:self.end]
    return None
  
  @property
  def norms(self) -> typing.Optional[list[str]]:
    """returns all norms in mention"""
    if self.sentence_obj.norms:
      return self.sentence_obj.norms[self.start:self.end]
    return None
  
  @property
  def chunks(self) -> typing.Optional[list[str]]:
    """returns all chunks in mention"""
    if self.sentence_obj.chunks:
      return self.sentence_obj.chunks[self.start:self.end]
    return None

  @property
  def text(self) -> str:
    """returns a string that contains the mention"""
    _text = self.document.text
    if _text is not None:
      return _text[self.start_offset:self.end_offset]
    # FIXME: this can be improved
    else:
      return " ".join(self.raw[self.start:self.end])

  # /** returns a string that contains the mention */
  # def text: String = document.text match {
  #   case Some(txt) => txt.slice(startOffset, endOffset)
  #   case None =>
  #     // try to reconstruct the sentence using the character offsets
  #     val bits = raw.head +: tokenInterval.tail.map { i =>
  #       val spaces = " " * (sentenceObj.startOffsets(i) - sentenceObj.endOffsets(i - 1))
  #       val rawWord = sentenceObj.raw(i)
  #       spaces + rawWord
  #     }
  #     bits.mkString
  # }
    
  # /** returns all syntactic heads */
  # def synHeads: Seq[Int] = sentenceObj.dependencies match {
  #   case Some(deps) => DependencyUtils.findHeads(tokenInterval, deps)
  #   case None => Nil
  # }

  # /** returns the minimum distance to a root node for dependencies within the token interval */
  # def distToRootOpt: Option[Int] = sentenceObj.dependencies.flatMap { deps =>
  #   // Note that
  #   // Double.MaxValue.toInt == Int.MaxValue
  #   // Double.PositiveInfinity.toInt == Int.MaxValue
  #   DependencyUtils.distToRootOpt(tokenInterval, deps).map(_.toInt)
  # }

  # /** returns the syntactic head of `mention`  */
  # def synHead: Option[Int] = synHeads.lastOption

  # /** returns head token */
  # def synHeadWord: Option[String] = synHead.map(i => sentenceObj.words(i))

  # /** returns head pos tag */
  # def synHeadTag: Option[String] = synHead.flatMap(i => sentenceObj.tags.map(_(i)))

  # /** returns head lemma */
  # def synHeadLemma: Option[String] = synHead.flatMap(i => sentenceObj.lemmas.map(_(i)))

  # /** returns all semantic heads */
  # def semHeads: Seq[Int] = DependencyUtils.findHeadsStrict(tokenInterval, sentenceObj)

  # /** returns the syntactic head of `mention`  */
  # def semHead: Option[Int] = semHeads.lastOption

  # /** returns head token */
  # def semHeadWord: Option[String] = semHead.map(i => sentenceObj.words(i))

  # /** returns head pos tag */
  # def semHeadTag: Option[String] = semHead.flatMap(i => sentenceObj.tags.map(_(i)))

  # /** returns head lemma */
  # def semHeadLemma: Option[String] = semHead.flatMap(i => sentenceObj.lemmas.map(_(i)))


  # override def canEqual(a: Any) = a.isInstanceOf[Mention]

  # override def equals(that: Any): Boolean = that match {
  #   case that: Mention => that.canEqual(this) && this.hashCode == that.hashCode
  #   case _ => false
  # }

  # def compare(that: Mention): Int = {
  #   require(this.document == that.document,
  #     "can't compare mentions if they belong to different documents")
  #   if (this.sentence < that.sentence) -1
  #   else if (this.sentence > that.sentence) 1
  #   else this.tokenInterval compare that.tokenInterval
  # }

  # def precedes(that: Mention): Boolean = this.compare(that) < 0

# class Mention(BaseModel):
    
#     TBM: typing.ClassVar[str] = "TextBoundMention"
#     EM: typing.ClassVar[str] = "EventMention"
#     RM: typing.ClassVar[str] = "RelationMention"

#     """
#     A labeled span of text.  Used to model textual mentions of events, relations, and entities.

#     Parameters
#     ----------
#     token_interval : Interval
#         The span of the Mention represented as an Interval.
#     sentence : int
#         The sentence index that contains the Mention.
#     document : Document
#         The Document in which the Mention was found.
#     foundBy : str
#         The Odin IE rule that produced this Mention.
#     label : str
#         The label most closely associated with this span.  Usually the lowest hyponym of "labels".
#     labels: list
#         The list of labels associated with this span.
#     trigger: dict or None
#         dict of JSON for Mention's trigger (event predicate or word(s) signaling the Mention).
#     arguments: dict or None
#         dict of JSON for Mention's arguments.
#     paths: dict or None
#         dict of JSON encoding the syntactic paths linking a Mention's arguments to its trigger (applies to Mentions produces from `type:"dependency"` rules).
#     doc_id: str or None
#         the id of the document

#     Attributes
#     ----------
#     tokenInterval: processors.ds.Interval
#         An `Interval` encoding the `start` and `end` of the `Mention`.
#     start : int
#         The token index that starts the `Mention`.
#     end : int
#         The token index that marks the end of the Mention (exclusive).
#     sentenceObj : processors.ds.Sentence
#         Pointer to the `Sentence` instance containing the `Mention`.
#     characterStartOffset: int
#         The index of the character that starts the `Mention`.
#     characterEndOffset: int
#         The index of the character that ends the `Mention`.
#     type: Mention.TBM or Mention.EM or Mention.RM
#         The type of the `Mention`.

#     See Also
#     --------

#     [`Odin` manual](https://arxiv.org/abs/1509.07513)

#     Methods
#     -------
#     matches(label_pattern)
#         Test if the provided pattern, `label_pattern`, matches any element in `Mention.labels`.

#     overlaps(other)
#         Test whether other (token index or Mention) overlaps with span of this Mention.

#     copy(**kwargs)
#         Copy constructor for this Mention.

#     words()
#         Words for this Mention's span.

#     tags()
#         Part of speech for this Mention's span.

#     lemmas()
#         Lemmas for this Mention's span.

#     _chunks()
#         chunk labels for this Mention's span.

#     _entities()
#         NE labels for this Mention's span.
#     """

    # def __init__(self,
    #             token_interval,
    #             sentence,
    #             document,
    #             foundBy,
    #             label,
    #             labels=None,
    #             trigger=None,
    #             arguments=None,
    #             paths=None,
    #             keep=True,
    #             doc_id=None):

    #     NLPDatum.__init__(self)
    #     self.label = label
    #     self.labels = labels if labels else [self.label]
    #     self.tokenInterval = token_interval
    #     self.start = self.tokenInterval.start
    #     self.end = self.tokenInterval.end
    #     self.document = document
    #     self._doc_id = doc_id or hash(self.document)
    #     self.sentence = sentence
    #     if trigger:
    #         # NOTE: doc id is not stored for trigger's json,
    #         # as it is assumed to be contained in the same document as its parent
    #         trigger.update({"document": self._doc_id})
    #         self.trigger = Mention.load_from_JSON(trigger, self._to_document_map())
    #     else:
    #         self.trigger = None
    #     # unpack args
    #     self.arguments = {role:[Mention.load_from_JSON(a, self._to_document_map()) for a in args] for (role, args) in arguments.items()} if arguments else None
    #     self.paths = paths
    #     self.keep = keep
    #     self.foundBy = foundBy
    #     # other
    #     self.sentenceObj = self.document.sentences[self.sentence]
    #     self.text = " ".join(self.sentenceObj.words[self.start:self.end])
    #     # recover offsets
    #     self.characterStartOffset = self.sentenceObj.startOffsets[self.tokenInterval.start]
    #     self.characterEndOffset = self.sentenceObj.endOffsets[self.tokenInterval.end - 1]
    #     # for later recovery
    #     self.id = None
    #     self.type = self._set_type()

    # def __str__(self):
    #     return "{}: {}".format(OdinHighlighter.LABEL(self.label), OdinHighlighter.highlight_mention(self))

    # def __eq__(self, other):
    #     if isinstance(other, self.__class__):
    #         return self.__dict__ == other.__dict__
    #     else:
    #         return False

    # def __ne__(self, other):
    #     return not self.__eq__(other)

    # def __hash__(self):
    #     return hash(self.to_JSON())

    # def startOffset(self):
    #     return self.sentenceObj.endOffsets[self.start]

    # def endOffset(self):
    #     return self.sentenceObj.endOffsets[self.end -1]

    # def words(self):
    #     return self.sentenceObj.words[self.start:self.end]

    # def tags(self):
    #     return self.sentenceObj.tags[self.start:self.end]

    # def lemmas(self):
    #     return self.sentenceObj.lemmas[self.start:self.end]

    # def _chunks(self):
    #     return self.sentenceObj._chunks[self.start:self.end]

    # def _entities(self):
    #     return self.sentenceObj._entities[self.start:self.end]

    # def overlaps(self, other):
    #     """
    #     Checks for overlap.
    #     """
    #     if isinstance(other, int):
    #         return self.start <= other < self.end
    #     elif isinstance(other, Mention):
    #         # equiv. sentences + checks on start and end
    #         return (self.sentence.__hash__() == other.sentence.__hash__()) and \
    #         self.tokenInterval.overlaps(other.tokenInterval)
    #     else:
    #         return False



    # def _arguments_to_JSON_dict(self):
    #     return dict((role, [a.to_JSON_dict() for a in args]) for (role, args) in self.arguments.items())

    # def _paths_to_JSON_dict(self):
    #     return {role: paths.to_JSON_dict() for (role, paths) in self.paths}

    # @staticmethod
    # def load_from_JSON(mjson, docs_dict):
    #     # recover document
    #     doc_id = mjson["document"]
    #     doc = docs_dict[doc_id]
    #     labels = mjson["labels"]
    #     kwargs = {
    #         "label": mjson.get("label", labels[0]),
    #         "labels": labels,
    #         "token_interval": Interval.load_from_JSON(mjson["tokenInterval"]),
    #         "sentence": mjson["sentence"],
    #         "document": doc,
    #         "doc_id": doc_id,
    #         "trigger": mjson.get("trigger", None),
    #         "arguments": mjson.get("arguments", None),
    #         "paths": mjson.get("paths", None),
    #         "keep": mjson.get("keep", True),
    #         "foundBy": mjson["foundBy"]
    #     }
    #     m = Mention(**kwargs)
    #     # set IDs
    #     m.id = mjson["id"]
    #     m._doc_id = doc_id
    #     # set character offsets
    #     m.character_start_offset = mjson["characterStartOffset"]
    #     m.character_end_offset = mjson["characterEndOffset"]
    #     return m

    # def _to_document_map(self):
    #     return {self._doc_id: self.document}

    # def _set_type(self):
    #     # event mention
    #     if self.trigger != None:
    #         return Mention.EM
    #     # textbound mention
    #     elif self.trigger == None and self.arguments == None:
    #         return Mention.TBM
    #     else:
    #         return Mention.RM


class TextBoundMention(Mention):

  # override from Mention
  arguments: typing.Optional[Mention.Arguments] = Field(default=None, description="A TextBoundMention has no arguments")
  paths: typing.Optional[Mention.Paths] = Field(default=None, description="A TextBoundMention has no paths")

class RelationMention(Mention):
  # FIXME: ensure arguments dict is non-empt

  # TODO: implement me
  # see https://github.com/clulab/processors/blob/9f89ea7bf6ac551f77dbfdbb8eec9bf216711df4/main/src/main/scala/org/clulab/odin/Mention.scala
  @property
  def is_valid(self) -> bool:
    """returns true if this is a valid mention"""
    # args should all be from same sentence
    raise NotImplementedError
  
  # TODO: implement me
  @property
  def to_event_mention(trigger: TextBoundMention) -> "EventMention":
    """"""
    # check that trigger and self have same sent and doc
    raise NotImplementedError

  # TODO: implement me
  def scatter(arg_name: str, size: int) -> list[RelationMention]:
    raise NotImplementedError
  # arguments
  #   .getOrElse(argName, Nil)
  #   .combinations(size)
  #   .map(args => this + (argName -> args))
  #   .toList

  # TODO: implement me
  # Create a new EventMention by removing a single argument
  def __sub__(other: typing.Any) -> RelationMention:
    raise NotImplementedError
    #copy(arguments = this.arguments - argName)
    # Create a new EventMention by removing a sequence of arguments
    # def --(argNames: Seq[String]): EventMention =
    #   copy(arguments = this.arguments -- argNames)

  # TODO: implement me
  def __add__(other: typing.Any) -> RelationMention:
    """Create a new RelationMention by adding a key, value pair to the arguments map"""
    #def +(arg: (String, Seq[Mention])): RelationMention =
    #copy(arguments = this.arguments + arg)
    raise NotImplementedError
  
class EventMention(Mention):
  trigger: TextBoundMention = Field(description="")
  arguments: Mention.Arguments = Field(default={}, description="A mapping of the EventMention's arguments (role -> list[Mention])")
  paths: typing.Optional[Mention.Paths] = Field(default={}, description="Graph traversal leading to each argument")

  def copy(
    self,
    maybe_trigger: typing.Optional[TextBoundMention] = None,
    maybe_labels: typing.Optional[list[str]] = None,
    maybe_token_interval: typing.Optional[Interval] = None,
    maybe_sentence_index: typing.Optional[int] = None,
    maybe_document: typing.Optional[Document] = None,
    maybe_keep: typing.Optional[bool] = None,
    maybe_arguments: typing.Optional[Mention.Arguments] = None,
    maybe_paths: typing.Optional[Mention.Paths] = None,
    maybe_found_by: typing.Optional[str] = None,
  ) -> EventMention:
    return EventMention(
      trigger = maybe_trigger or self.trigger,
      labels = maybe_labels or self.labels,
      token_interval = maybe_token_interval or self.token_interval,
      sentence_index = maybe_sentence_index or self.sentence_index,
      document = maybe_document or self.document,
      keep = maybe_keep or self.keep,
      arguments = maybe_arguments or self.arguments,
      paths = maybe_paths or self.paths,
      found_by = maybe_found_by or self.found_by
    )

  # TODO: implement me
  # see https://github.com/clulab/processors/blob/9f89ea7bf6ac551f77dbfdbb8eec9bf216711df4/main/src/main/scala/org/clulab/odin/Mention.scala#L323-L330
  @property
  def is_valid(self) -> bool:
    """returns true if this is a valid mention"""
    raise NotImplementedError
  
  # TODO: implement me
  def to_relation_mention(self) -> RelationMention:
    raise NotImplementedError
  
  # TODO: implement me
  def scatter(arg_name: str, size: int) -> list[EventMention]:
    raise NotImplementedError
  # arguments
  #   .getOrElse(argName, Nil)
  #   .combinations(size)
  #   .map(args => this + (argName -> args))
  #   .toList

  # TODO: implement me
  # Create a new EventMention by removing a single argument
  def __sub__(other: typing.Any) -> EventMention:
    raise NotImplementedError
    #copy(arguments = this.arguments - argName)
    # Create a new EventMention by removing a sequence of arguments
    # def --(argNames: Seq[String]): EventMention =
    #   copy(arguments = this.arguments -- argNames)

  # TODO: implement me
  def __add__(other: typing.Any) -> EventMention:
    """Create a new EventMention by adding a key, value pair to the arguments map"""
    #def +(arg: (String, Seq[Mention])): EventMention =
    #copy(arguments = this.arguments + arg)
    raise NotImplementedError
  
class CrossSentenceMention(Mention):
  anchor: Mention = Field(description="The mention serving as the anchor for this cross-sentence mention")
  neighbor: Mention = Field(description="The second mention for this cross-sentence mention")

  # FIXME: add check on arguments  
  #require(arguments.size == 2, "CrossSentenceMention must have exactly two arguments")
  # assert anchor.document == neighbor.document
  # assert anchor.sentence_obj != neighbor.sentence_obj