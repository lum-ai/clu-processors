from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from lum.clu.processors.directed_graph import DirectedGraph
from lum.clu.processors.utils import Labels
import typing

__all__ = ["Sentence"]

class Sentence(BaseModel):

    UNKNOWN: typing.ClassVar[str] = Labels.UNKNOWN
    # the O in IOB notation
    O: typing.ClassVar[str] = Labels.O

    """
    Storage class for an annotated sentence. Based on [`org.clulab.processors.Sentence`](https://github.com/clulab/processors/blob/master/main/src/main/scala/org/clulab/processors/Sentence.scala)
    """
    text: typing.Optional[str] = Field(default=None, description=" The text of the `Sentence`.")

    raw: list[str] = Field(description="Raw tokens in this sentence; these are expected to match the original text")
    
    words: list[str] = Field(description="A list of the `Sentence`'s tokens.")

    start_offsets: list[int] = Field(alias="startOffsets", description="The character offsets starting each token (inclusive).")

    end_offsets: list[int] = Field(alias="endOffsets", description="The character offsets marking the end of each token (exclusive).")

    tags: typing.Optional[list[str]] = Field(default=None, description="A list of the `Sentence`'s tokens represented using part of speech (PoS) tags.")

    lemmas: typing.Optional[list[str]] = Field(default=None, description="A list of the `Sentence`'s tokens represented using lemmas.")

    norms: typing.Optional[list[str]] = Field(default=None, description="Normalized values of named/numeric entities, such as dates.")

    chunks: typing.Optional[list[str]] = Field(default=None, description="A list of the `Sentence`'s tokens represented using IOB-style phrase labels (ex. `B-NP`, `I-NP`, `B-VP`, etc.).")

    entities: typing.Optional[list[str]] = Field(default=None, description="A list of the `Sentence`'s tokens represented using IOB-style named entity (NE) labels.")

    graphs: dict[str, DirectedGraph] = Field(description="A dictionary (str -> `lum.clu.processors.doc.DirectedGraph`) mapping the graph type/name to a `lum.clu.processors.doc.DirectedGraph`.")

    @model_validator(mode="before")
    @classmethod
    def raw_or_words(cls, data: typing.Any) -> typing.Any:
        """if `raw` is not present, use `words` in its place."""
        if isinstance(data, dict):
            words = data.get("words", None)
            raw = data.get("raw", None)
            if raw is None:
                data["raw"] = words
        return data
    
    # length : int
    #     The number of tokens in the `Sentence`

    # basic_dependencies : lum.clu.processors.doc.DirectedGraph
    #     A `lum.clu.processors.doc.DirectedGraph` using basic Stanford dependencies.

    # collapsed_dependencies : lum.clu.processors.doc.DirectedGraph
    #     A `lum.clu.processors.doc.DirectedGraph` using collapsed Stanford dependencies.

    # dependencies : lum.clu.processors.doc.DirectedGraph
    #     A pointer to the prefered syntactic dependency graph type for this `Sentence`.

    # _entities : [str]
    #     The IOB-style Named Entity (NE) labels corresponding to each token.

    # _chunks : [str]
    #     The IOB-style chunk labels corresponding to each token.

    # nes : dict
    #     A dictionary of NE labels represented in the `Document` -> a list of corresponding text spans (ex. {"PERSON": [phrase 1, ..., phrase n]}). Built from `Sentence._entities`

    # phrases : dict
    #     A dictionary of chunk labels represented in the `Document` -> a list of corresponding text spans (ex. {"NP": [phrase 1, ..., phrase n]}). Built from `Sentence._chunks`


    # Methods
    # -------
    # bag_of_labeled_dependencies_using(form)
    #     Produces a list of syntactic dependencies where each edge is labeled with its grammatical relation.

    # bag_of_unlabeled_dependencies_using(form)
    #     Produces a list of syntactic dependencies where each edge is left unlabeled without its grammatical relation.

    @property
    def length(self) -> int:
      return len(self.raw)


        # self.basic_dependencies = self.graphs.get(DirectedGraph.STANFORD_BASIC_DEPENDENCIES, None)
        # self.collapsed_dependencies = self.graphs.get(DirectedGraph.STANFORD_COLLAPSED_DEPENDENCIES, None)
        # self.dependencies = self.collapsed_dependencies if self.collapsed_dependencies != None else self.basic_dependencies
        # # IOB tokens -> {label: [phrase 1, ..., phrase n]}
        # self.nes = self._handle_iob(self._entities)
        # self.phrases = self._handle_iob(self._chunks)

    # def __eq__(self, other):
    #     if isinstance(other, self.__class__):
    #         return self.to_JSON() == other.to_JSON()
    #     else:
    #         return False

    # def __ne__(self, other):
    #     return not self.__eq__(other)

    # def __hash__(self):
    #     return hash(self.to_JSON(pretty=False))

    # def deduplication_hash(self):
    #     """
    #     Generates a deduplication hash for the sentence
    #     """
    #     return hashlib.sha256(self.to_JSON(pretty=False).encode()).hexdigest()

    # def _get_tokens(self, form):
    #     f = form.lower()
    #     if f == "words":
    #         tokens = self.words
    #     elif f == "tags":
    #         tokens = self.tags
    #     elif f == "lemmas":
    #         tokens = self.lemmas
    #     elif f == "entities":
    #         tokens = self.nes
    #     elif f == "index":
    #         tokens = list(range(self.length))
    #     # unrecognized form
    #     else:
    #         raise Exception("""form must be 'words', 'tags', 'lemmas', or 'index'""")
    #     return tokens

    # def _set_toks(self, toks):
    #     return toks if toks else [Sentence.UNKNOWN]*self.length

    # def _handle_iob(self, iob):
    #     """
    #     Consolidates consecutive tokens in IOB notation under the appropriate label.
    #     Regexs control for bionlp annotator, which uses IOB notation.
    #     """
    #     entity_dict = defaultdict(list)
    #     # initialize to empty label
    #     current = Sentence.O
    #     start = None
    #     end = None
    #     for i, tok in enumerate(iob):
    #         # we don't have an I or O
    #         if tok == Sentence.O:
    #             # did we have an entity with the last token?
    #             current = re.sub('(B-|I-)','', str(current))
    #             if current == Sentence.O:
    #                 continue
    #             else:
    #                 # the last sequence has ended
    #                 end = i
    #                 # store the entity
    #                 named_entity = ' '.join(self.words[start:end])
    #                 entity_dict[current].append(named_entity)
    #                 # reset our book-keeping vars
    #                 current = Sentence.O
    #                 start = None
    #                 end = None
    #         # we have a tag!
    #         else:
    #             # our old sequence continues
    #             current = re.sub('(B-|I-)','', str(current))
    #             tok = re.sub('(B-|I-)','', str(tok))
    #             if tok == current:
    #                 end = i
    #             # our old sequence has ended
    #             else:
    #                 # do we have a previous NE?
    #                 if current != Sentence.O:
    #                     end = i
    #                     named_entity = ' '.join(self.words[start:end])
    #                     entity_dict[current].append(named_entity)
    #                 # update our book-keeping vars
    #                 current = tok
    #                 start = i
    #                 end = None
    #     # this might be empty
    #     return entity_dict


    # def bag_of_labeled_dependencies_using(self, form):
    #     """
    #     Produces a list of syntactic dependencies
    #     where each edge is labeled with its grammatical relation.
    #     """
    #     tokens = self._get_tokens(form)
    #     return self.labeled_dependencies_from_tokens(tokens) if tokens else None

    # def bag_of_unlabeled_dependencies_using(self, form):
    #     """
    #     Produces a list of syntactic dependencies
    #     where each edge is left unlabeled without its grammatical relation.
    #     """
    #     tokens = self._get_tokens(form)
    #     return self.unlabeled_dependencies_from_tokens(tokens) if tokens else None

    # def labeled_dependencies_from_tokens(self, tokens):
    #     """
    #     Generates a list of labeled dependencies for a sentence
    #     using the provided tokens
    #     """
    #     deps = self.dependencies
    #     labeled = []
    #     return [(tokens[out], rel, tokens[dest]) \
    #             for out in deps.outgoing \
    #             for (dest, rel) in deps.outgoing[out]]

    # def unlabeled_dependencies_from_tokens(self, tokens):
    #     """
    #     Generate a list of unlabeled dependencies for a sentence
    #     using the provided tokens
    #     """
    #     return [(head, dep) for (head, rel, dep) in self.labeled_dependencies_from_tokens(tokens)]

    # def semantic_head(self, graph_name="stanford-collapsed", valid_tags={r"^N", "VBG"}, valid_indices=None):
    #     return HeadFinder.semantic_head(self, graph_name, valid_tags, valid_indices)