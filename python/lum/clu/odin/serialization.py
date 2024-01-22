from lum.clu.odin.mention import (Mention, TextBoundMention, RelationMention, EventMention, CrossSentenceMention)
from lum.clu.processors.document import Document
from lum.clu.processors.interval import Interval
import typing
import collections

__all__ = ["OdinJsonSerializer"]



    # ("type" -> longString) ~
    # // used for correspondence with paths map
    # ("id" -> id) ~ // tb.id would just create a different TextBoundMentionOps to provide the id
    # ("text" -> tb.text) ~
    # ("labels" -> tb.labels) ~
    # ("tokenInterval" -> Map("start" -> tb.tokenInterval.start, "end" -> tb.tokenInterval.end)) ~
    # ("characterStartOffset" -> tb.startOffset) ~
    # ("characterEndOffset" -> tb.endOffset) ~
    # ("sentence" -> tb.sentence) ~
    # ("document" -> documentEquivalenceHash.toString) ~
    # ("keep" -> tb.keep) ~
    # ("foundBy" -> tb.foundBy)

# object TextBoundMentionOps {
#   val string = "TextBoundMention"
#   val shortString = "T"
# }

# object EventMentionOps {
#   val string = "EventMention"
#   val shortString = "E"
# }

# object RelationMentionOps {
#   val string = "RelationMention"
#   val shortString = "R"
# }

# object CrossSentenceMentionOps {
#   val string = "CrossSentenceMention"
#   val shortString = "CS"
# }

class OdinJsonSerializer:

  MENTION_TB_TYPE = "TextBoundMention"
  MENTION_R_TYPE = "RelationMention"
  MENTION_E_TYPE = "EventMention"
  MENTION_C_TYPE = "CrossSentenceMention"

  # @staticmethod
  # def to_compact_mentions_json(jdata: dict[str, typing.Any]) -> list[Mention]:
  #   pass

  # don't blow the stack
  @staticmethod
  def from_compact_mentions_json(compact_json: dict[str, typing.Any]) -> list[Mention]:

    # populate mapping of doc id -> Document
    docs_map = dict()
    for doc_id, doc_json in compact_json["documents"].items():
      # store ID if not set
      if "id" not in doc_json:
        doc_json.update({"id": doc_id})
      docs_map[doc_id] = Document(**doc_json)

    mentions_map: dict[str, Mention] = dict()
    mention_ids: typing.Set[str] = {mn.get("id") for mn in compact_json["mentions"]}
    # attack TBMs first
    srt_fn = lambda mid: -1 if mid.startswith("T") else 1
    # make a queue w/ TBMs first
    missing: collections.deque = collections.deque(sorted(list(mention_ids), key=srt_fn))

    while len(missing) > 0:
      m_id = missing.popleft()
      # pop a key and try to create the mention map
      _, mns_map = OdinJsonSerializer._fetch_mention(
        m_id=m_id, 
        compact_json=compact_json, 
        docs_map=docs_map,
        mentions_map=mentions_map
      )
      # store new results
      mentions_map.update(mns_map)
      # filter out newly constructed mentions
      missing = collections.deque([k for k in missing if k not in mentions_map])
    #return list(mentions_map.values())
    # avoids unraveling mentions to include triggers, etc.
    return [m for mid, m in mentions_map.items() if mid in mention_ids]

  @staticmethod
  def _fetch_mention(m_id: str, compact_json: dict[str, typing.Any], docs_map: dict[str, Document], mentions_map: dict[str, Mention]) -> typing.Tuple[Mention, dict[str, Mention]]:
    # base case
    if m_id in mentions_map:
      return mentions_map[m_id], mentions_map
     
    mjson: dict[str, typing.Any] = [mn for mn in compact_json["mentions"] if mn.get("id", None)== m_id][0]
    mtype = mjson["type"]
    # gather general info
    labels = mjson["labels"]
    token_interval = Interval(**mjson["tokenInterval"])
    document = docs_map[mjson["document"]]
    start = mjson["characterStartOffset"]
    end = mjson["characterEndOffset"]
    sentence_index = mjson["sentence"]
    found_by = mjson["foundBy"]
    keep = mjson.get("keep", True)
    # easy case. We have everything we need.
    if mtype == OdinJsonSerializer.MENTION_TB_TYPE:
      m = TextBoundMention(
        labels=labels,
        token_interval=token_interval,
        sentence_index=sentence_index,
        start=start,
        end=end,
        document=document,
        found_by=found_by,
        keep=keep
      )
      mentions_map[m_id] = m
      return (m, mentions_map)
    # everything else *might* have paths
    paths: typing.Optional[Mention.Paths] = OdinJsonSerializer.construct_paths(mjson.get("paths", None))
    # retrieve all args recursively
    arguments: Mention.Arguments = dict()
    for role, mns_json in mjson.get("arguments", {}).items():
        role_mns = arguments.get(role, [])
        for mn_json in mns_json:
          _mid = mn_json["id"]
          if _mid in mentions_map:
            _mn = mentions_map[_mid]
          else:
            # NOTE: in certain cases, the referenced mid might not be found in the compact_json.
            # we'll add it to be safe.
            if all(m["id"] != _mid for m in compact_json["mentions"]):
               compact_json["mentions"] = compact_json["mentions"] + [mn_json]
            _mn, _mns_map = OdinJsonSerializer._fetch_mention(
              m_id=_mid, 
              compact_json=compact_json, 
              docs_map=docs_map, mentions_map=mentions_map
            )
            # update our progress
            mentions_map.update(_mns_map)
          # store this guy
          role_mns.append(_mn)
        # update our args
        arguments[role] = role_mns
          
    if mtype == OdinJsonSerializer.MENTION_E_TYPE:
        # get or load trigger
        trigger_mjson = mjson["trigger"]
        trigger_id = trigger_mjson["id"]
        if trigger_id in mentions_map:
          trigger = mentions_map[trigger_id]
        # avoid a recursive call 
        # for the sake of the stack...
        else:
          trigger = TextBoundMention(
            labels=trigger_mjson["labels"],
            token_interval=Interval(**trigger_mjson["tokenInterval"]),
            sentence_index=trigger_mjson["sentence"],
            start=trigger_mjson["characterStartOffset"],
            end=trigger_mjson["characterEndOffset"],
            document=docs_map[trigger_mjson["document"]],
            found_by=trigger_mjson["foundBy"],
            keep=trigger_mjson.get("keep", False)
          )
        # we have what we need
        m = EventMention(
          labels=labels,
          token_interval=token_interval,
          trigger=trigger,
          sentence_index=sentence_index,
          start=start,
          end=end,
          document=document,
          arguments=arguments,
          paths=paths,
          found_by=found_by,
          keep=keep
        )
        mentions_map[m_id] = m
        return (m, mentions_map)
    if mtype == OdinJsonSerializer.MENTION_R_TYPE:
        # we have what we need
        m = RelationMention(
          labels=labels,
          token_interval=token_interval,
          sentence_index=sentence_index,
          start=start,
          end=end,
          document=document,
          arguments=arguments,
          paths=paths,
          found_by=found_by,
          keep=keep
        )
        mentions_map[m_id] = m
        return (m, mentions_map)
    if mtype == OdinJsonSerializer.MENTION_C_TYPE:
        # anchor
        # this will be one of our args (see https://github.com/clulab/processors/blob/9f89ea7bf6ac551f77dbfdbb8eec9bf216711df4/main/src/main/scala/org/clulab/odin/Mention.scala#L535), so we'll be lazy
        anchor: Mention = mentions_map[mjson["anchor"]["id"]]
        # neighbor
        # this will be one of our args (see https://github.com/clulab/processors/blob/9f89ea7bf6ac551f77dbfdbb8eec9bf216711df4/main/src/main/scala/org/clulab/odin/Mention.scala#L535), so we'll be lazy
        neighbor: Mention = mentions_map[mjson["neighbor"]["id"]]
        # we have what we need
        m = CrossSentenceMention(
          labels=labels,
          token_interval=token_interval,
          anchor=anchor,
          neighbor=neighbor,
          # corresponds to anchor.sentence_inde
          sentence_index=sentence_index,
          start=start,
          end=end,
          document=document,
          arguments=arguments,
          paths=None,
          found_by=found_by,
          keep=keep
        )
        mentions_map[m_id] = m
        return (m, mentions_map)
    else:
       raise Exception(f"Unrecognized mention type {mtype}. Expected one of the following {OdinJsonSerializer.MENTION_TB_TYPE}, {OdinJsonSerializer.MENTION_E_TYPE}, {OdinJsonSerializer.MENTION_R_TYPE}, {OdinJsonSerializer.MENTION_C_TYPE}")
    
  @staticmethod
  def construct_paths(maybe_path_data: typing.Optional[dict[str, typing.Any]]) -> typing.Optional[Mention.Paths]:
     # FIXME: implement me
     return None
     
  @staticmethod
  def _load_mention_from_compact_JSON(mention_id: str, compact_json: dict[str, typing.Any], docs_dict: dict[str, Document], mentions_dict: dict[str, Mention]):
      mjson = compact_json["mentions"][mention_id]
      # recover document
      document = docs_dict[mjson["document"]]
      # TODO: load args

      # collect components
      mtype = mjson["type"]
      labels = mjson["labels"]
      token_interval = Interval(**mjson["tokenInterval"])
      if mtype == OdinJsonSerializer.MENTION_TB_TYPE:
         raise NotImplementedError
      elif mtype == OdinJsonSerializer.MENTION_E_TYPE:
         # get or load trigger
         raise NotImplementedError
      elif mtype == OdinJsonSerializer.MENTION_R_TYPE:
         raise NotImplementedError
      elif mtype == OdinJsonSerializer.MENTION_C_TYPE:
         raise NotImplementedError
         
      kwargs = {
          "label": mjson.get("label", labels[0]),
          "labels": labels,
          "token_interval": Interval.load_from_JSON(mjson["tokenInterval"]),
          "sentence": mjson["sentence"],
          "document": doc,
          "doc_id": doc_id,
          "trigger": mjson.get("trigger", None),
          "arguments": mjson.get("arguments", None),
          "paths": mjson.get("paths", None),
          "keep": mjson.get("keep", True),
          "foundBy": mjson["foundBy"]
      }
      m = Mention(**kwargs)
      # set IDs
      m.id = mjson["id"]
      m._doc_id = doc_id
      # set character offsets
      m.character_start_offset = mjson["characterStartOffset"]
      m.character_end_offset = mjson["characterEndOffset"]
      return m

  # def to_JSON_dict(self):
  #     m = dict()
  #     m["id"] = self.id
  #     m["type"] = self.type
  #     m["label"] = self.label
  #     m["labels"] = self.labels
  #     m["tokenInterval"] = self.tokenInterval.to_JSON_dict()
  #     m["characterStartOffset"] = self.characterStartOffset
  #     m["characterEndOffset"] = self.characterEndOffset
  #     m["sentence"] = self.sentence
  #     m["document"] = self._doc_id
  #     # do we have a trigger?
  #     if self.trigger:
  #          m["trigger"] = self.trigger.to_JSON_dict()
  #     # do we have arguments?
  #     if self.arguments:
  #         m["arguments"] = self._arguments_to_JSON_dict()
  #     # handle paths
  #     if self.paths:
  #         m["paths"] = self.paths
  #     m["keep"] = self.keep
  #     m["foundBy"] = self.foundBy
  #     return m