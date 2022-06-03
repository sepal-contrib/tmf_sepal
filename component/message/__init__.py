import os
from pathlib import Path

from sepal_ui.translator import Translator

# create a ms object that will be used to translate all the messages
# the base language is english and every untranslated messages will be fallback to the english key
# complete the json file the add keys in the app
# avoid hard written messages at all cost
cm = Translator(Path(__file__).parent)
