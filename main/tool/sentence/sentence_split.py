import re


class SentenceSplitter:
    def __init__(self):
        pass

    def split(self, text):
        sentences = re.split(r'[。！!?？;；]', text)
        sentences = list(filter(lambda x: True if x else False, sentences))
        return sentences
