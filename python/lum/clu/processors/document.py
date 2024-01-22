from pydantic import BaseModel, Field, ConfigDict
from lum.clu.processors.sentence import Sentence
from lum.clu.processors.utils import Labels
import typing


class Document(BaseModel):

    """
    Storage class for annotated text. Based on [`org.clulab.processors.Document`](https://github.com/clulab/processors/blob/master/main/src/main/scala/org/clulab/processors/Document.scala)
    """

    model_config = ConfigDict(populate_by_name=True)
    
    id: typing.Optional[str] = Field(default=None, description="A unique ID for the `Document`.")

    text: typing.Optional[str] = Field(default=None, description=" The text of the `Document`.")

    sentences: list[Sentence] = Field(description="The sentences comprising the `Document`.")

    # size : int
    #     The number of `sentences`.

    # words : [str]
    #     A list of the `Document`'s tokens.

    # tags : [str]
    #     A list of the `Document`'s tokens represented using part of speech (PoS) tags.

    # lemmas : [str]
    #     A list of the `Document`'s tokens represented using lemmas.

    # _entities : [str]
    #     A list of the `Document`'s tokens represented using IOB-style named entity (NE) labels.

    # nes : dict
    #     A dictionary of NE labels represented in the `Document` -> a list of corresponding text spans.

    # bag_of_labeled_deps : [str]
    #     The labeled dependencies from all sentences in the `Document`.

    # bag_of_unlabeled_deps : [str]
    #     The unlabeled dependencies from all sentences in the `Document`.

    # text : str or None
    #     The original text of the `Document`.

    # Methods
    # -------
    # bag_of_labeled_dependencies_using(form)
    #     Produces a list of syntactic dependencies where each edge is labeled with its grammatical relation.

    # bag_of_unlabeled_dependencies_using(form)
    #     Produces a list of syntactic dependencies where each edge is left unlabeled without its grammatical relation.


    # self.nes = merge_entity_dicts = self._merge_ne_dicts()
    # self.bag_of_labeled_deps = list(chain(*[s.dependencies.labeled for s in self.sentences]))
    # self.bag_of_unlabeled_deps = list(chain(*[s.dependencies.unlabeled for s in self.sentences]))

    # def __hash__(self):
    #     return hash(self.to_JSON())

    # def __unicode__(self):
    #     return self.text

    # def __str__(self):
    #     return "Document w/ {} Sentence{}".format(self.size, "" if self.size == 1 else "s")

    # def __eq__(self, other):
    #     if isinstance(other, self.__class__):
    #         return self.to_JSON() == other.to_JSON()
    #     else:
    #         return False

    # def __ne__(self, other):
    #     return not self.__eq__(other)

    # def bag_of_labeled_dependencies_using(self, form):
    #     return list(chain(*[s.labeled_dependencies_from_tokens(s._get_tokens(form)) for s in self.sentences]))

    # def bag_of_unlabeled_dependencies_using(self, form):
    #     return list(chain(*[s.unlabeled_dependencies_from_tokens(s._get_tokens(form)) for s in self.sentences]))

    # def _merge_ne_dicts(self):
    #     # Get the set of all NE labels found in the Doc's sentences
    #     entity_labels = set(chain(*[s.nes.keys() for s in self.sentences]))
    #     # Do we have any labels?
    #     if entity_labels == None:
    #         return None
    #     # If we have labels, consolidate the NEs under the appropriate label
    #     else:
    #         nes_dict = dict()
    #         for e in entity_labels:
    #             entities = []
    #             for s in self.sentences:
    #                 entities += s.nes[e]
    #             nes_dict[e] = entities
    #         return nes_dict