"""The text preprocessing before audio generation.

This is preprocessing for the "Silero" voice engine.
Silero do not read numbers and latin letters, so we need to convert them to russian words.
Silero sometimes crashes on certain unredable symbols, so remove them.

English version.
"""
import re
import os
from nltk.tokenize import sent_tokenize
from nltk.data import path
from num2words import num2words


__all__ = ["prepare_book", "prepare_sentence", "check_readable_symbols"]

this_dir = os.path.dirname(__file__)                 # src/
nltk_data_path = os.path.join(this_dir, "nltk_data") # src/nltk_data
path.append(nltk_data_path)


def numbers_to_words(text):
    """Find all numeric values and replace them by words."""
    for match in re.findall("[+-]?\d*[.,]?\d+", text):
        # "num2words" is a library that converts numbers to words.
        # It doesn"t work with commas.
        repl = num2words(re.sub(",", ".", match), lang="en")
        # Replace the pattern by the repl: re.sub(pattern, repl, string, count).
        text = re.sub(match, repl, text, 1)
    
    return text


def check_readable_symbols(text):
    if re.search("[a-zA-Z]", text):
        return True
    else:
        return False


def prepare_book(book):
    book = sent_tokenize(book)
    
    return book


def prepare_sentence(sentence):
    sentence = numbers_to_words(sentence)
    
    return sentence
