import os
import re

import pandas as pd
from base import db, cur

import random

from mstranslator import Translator

key_choices = ["e6e5859bfb4b40baa45e2105dc4880e9",
               "9ed1db3b52234167b9aadf2cbc4c9b78", ]


def _checkTitle(title):
    res = ""
    try:
        translator = Translator(random.choice(key_choices))
        res = translator.detect_lang([title])
        #
        # # translator = Translator(random.choice(key_choices))
        # # res = translate_text(title,'es',)
        # # res = translator.detect_langs([title])
        # res = detect_language(title)
        # print(res)
        # res = TextBlob(title).detect_language()

    except (IndexError, ValueError):
        pass
    return res