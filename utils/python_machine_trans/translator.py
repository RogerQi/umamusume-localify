import sys
import os
import time
import re

from googletrans import Translator

class UmaMusumeStrTrans:
    """
    Class for processing Japanese original str from the Uma Musume DMM Game
    """
    def __init__(self, target_language):
        """
        target_language: target language to be translated to
        """

        # Add other languages if necessary
        # Code can be looked up by inspecting elements at https://translate.google.com/
        assert target_language in ["en", "zh-CN"]
        self.target_language = target_language
        self.translator = Translator()

        # There are two types of special Char in race_message.json
        #   1. %h_rank_ta1 (% followed by combinations of ASCII letters/numbers/underscore)
        #   2. EOL char: \r \n \r\n \\
        self.regex_exp = r"(%\w*|\\\\n|\\\\r|\\\\|\\r|\\n|\\t|\\r\\n|<.*?>|{\d*})+"
        raise NotImplementedError

    def trans_one(self, raw_str):
        """
        Parameter:
            - raw_str: raw string from dumped original data
                Example: "美しい青空が広がる、%course\nターフも絶好の良バ場になりました！"
        
        Return: translated string in target language, preserving special characters
                such as %course string formatter or \r\n EOL character
        """
        # 1. Split string with special character
        
        # 2. Translate string piece by piece
        self.translator.translate(raw_str, src='ja', dest=self.target_language)
        # 3. Piece back string

    def split_raw_str(self, raw_str):
        pass