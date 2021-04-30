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
        # Language code can be looked up at https://translate.google.com/
        assert target_language in ["en", "zh-CN", "test"]
        self.target_language = target_language
        if target_language != "test":
            self.translator = Translator()

        # There are a various types of special characters in JSON
        # check tests/test_translator.py for common examples
        self.regex_exp = r"(?:%\w*|\\\\n|\\\\r|\\\\|\\r|\\n|\\t|\\r\\n|\n|<.*?>|{\d*})+"

    def trans_one(self, raw_str):
        """
        Parameter:
            - raw_str: raw string from dumped original data
                Example: "美しい青空が広がる、%course\nターフも絶好の良バ場になりました！"
        
        Return: translated string in target language, preserving special characters
                such as %course string formatter or \r\n EOL character
        """
        # 1. Split string with special character
        seps, src_strs = self.split_raw_str(raw_str)

        # 1.5. Some sanity checks
        for token in src_strs:
            self.src_str_sanity_check(token)
        assert len(seps) == len(src_strs) - 1

        # 2. Translate string piece by piece
        if self.target_language == "test":
            # This test target language is for local testing only
            # we want to avoid abusing google translate as much as possible...
            dst_strs = ["|TESTTOKEN@|" for i in src_strs]
        else:
            dst_strs = self.translator.translate(raw_str, src='ja', dest=self.target_language)
            dst_strs = [translated_obj.text for translated_obj in dst_strs]

        assert len(src_strs) == len(dst_strs)

        # 3. Piece back string
        ret = ["" for i in range(len(seps) + len(dst_strs))]
        ret[::2] = dst_strs
        ret[1::2] = seps

        return ''.join(ret)

    def split_raw_str(self, raw_str):
        """
        Parameter:
            - raw_str: raw string from dumped original data.
                       See comment under self.trans_one.
        
        Return:
            - separators: list of special char that separated the raw string
            - str_to_translate: list of japanese characters to be translated
        """
        separators = re.findall(self.regex_exp, raw_str)
        str_to_translate = re.split(self.regex_exp, raw_str)
        return separators, str_to_translate
    
    @staticmethod
    def src_str_sanity_check(some_str):
        assert "\\" not in some_str
        assert "\n" not in some_str
        assert "\r" not in some_str
        assert "\t" not in some_str
        assert "%" not in some_str
        assert "{" not in some_str and "}" not in some_str
        assert "<" not in some_str and ">" not in some_str
