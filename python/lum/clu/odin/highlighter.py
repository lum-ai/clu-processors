from termcolor import colored

__all__ = ["OdinHighlighter"]

class OdinHighlighter:

    @staticmethod
    def LABEL(token):
        return colored(token, color="red", attrs=["bold"])

    @staticmethod
    def ARG(token):
        return colored(token, on_color="on_green", attrs=["bold"])

    @staticmethod
    def TRIGGER(token):
        return colored(token, on_color="on_blue", attrs=["bold"])

    @staticmethod
    def CONCEAL(token):
        return colored(token, on_color="on_grey", attrs=["concealed"])

    @staticmethod
    def MENTION(token):
        return colored(token, on_color="on_yellow")

    # @staticmethod
    # def highlight_mention(mention):
    #     """
    #     Formats text of mention
    #     """
    #     text_span = mention.sentenceObj.words[:]
    #     # format TBM span like an arg
    #     if mention.type == "TextBoundMention":
    #         for i in range(mention.start, mention.end):
    #             text_span[i] = OdinHighlighter.ARG(text_span[i])
    #     if mention.arguments:
    #         for (role, args) in mention.arguments.items():
    #             for arg in args:
    #                 for i in range(arg.start, arg.end):
    #                     text_span[i] = OdinHighlighter.ARG(text_span[i])
    #     # format trigger distinctly from args
    #     if mention.trigger:
    #         trigger = mention.trigger
    #         for i in range(trigger.start, trigger.end):
    #             text_span[i] = OdinHighlighter.TRIGGER(text_span[i])

    #     # highlight tokens contained in mention span
    #     for i in range(mention.start, mention.end):
    #         text_span[i] = OdinHighlighter.MENTION(text_span[i])
    #     mention_span = OdinHighlighter.MENTION(" ").join(text_span[mention.start:mention.end])
    #     # highlight spaces in mention span
    #     formatted_text = " ".join(text_span[:mention.start]) + " " + mention_span + " " + " ".join(text_span[mention.end:])
    #     return formatted_text.strip()