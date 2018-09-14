from . import tokenize


class OpenIE:
    def __init__(self):
        self.tokenizer = tokenize.get_class('corenlp')()

    def extract(self):
        pass
