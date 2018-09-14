import re


class Cleaner:
    def __init__(self):
        pass

    def clean(self, text):
        text = re.sub('（.*?）', '', text)
        return text
