"""The text preprocessing before audio generation.

This is preprocessing for the "Silero" voice engine.
Silero do not read numbers and latin letters, so we need to convert them to russian words.
Silero sometimes crashes on certain unredable symbols, so remove them.

Russian version.
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


def single_latin_to_cyrillic(text):
    text = re.sub("[Aa]", "эй", text)
    text = re.sub("[Bb]", "би", text)
    text = re.sub("[Cc]", "си", text)
    text = re.sub("[Dd]", "ди", text)
    text = re.sub("[Ee]", "и", text)
    text = re.sub("[Ff]", "эф", text)
    text = re.sub("[Gg]", "джи", text)
    text = re.sub("[Hh]", "эйч", text)
    text = re.sub("[Ii]", "ай", text)
    text = re.sub("[Jj]", "джей", text)
    text = re.sub("[Kk]", "кей", text)
    text = re.sub("[Ll]", "эл", text)
    text = re.sub("[Mm]", "эм", text)
    text = re.sub("[Nn]", "эн", text)
    text = re.sub("[Oo]", "оу", text)
    text = re.sub("[Pp]", "пи", text)
    text = re.sub("[Qq]", "кью", text)
    text = re.sub("[Rr]", "ар", text)
    text = re.sub("[Ss]", "эс", text)
    text = re.sub("[Tt]", "ти", text)
    text = re.sub("[Uu]", "ю", text)
    text = re.sub("[Vv]", "ви", text)
    text = re.sub("[Ww]", "даблйу", text)
    text = re.sub("[Xx]", "икс", text)
    text = re.sub("[Yy]", "уаай", text)
    text = re.sub("[Zz]", "зэд", text)
    
    return text


def combined_latin_to_cyrillic(text):
    text = re.sub("PH|Ph|pH|ph", "ф", text)
    text = re.sub("YA|Ya|yA|ya", "я", text)
    text = re.sub("ZH|Zh|zH|zh", "ж", text)
    text = re.sub("SH|Sh|sH|sh", "ш", text)
    text = re.sub("CH|Ch|cH|ch", "ч", text)
    
    text = re.sub("[Aa]", "а", text)
    text = re.sub("[Bb]", "б", text)
    text = re.sub("[Cc]", "к", text)
    text = re.sub("[Dd]", "д", text)
    text = re.sub("[Ee]", "и", text)
    text = re.sub("[Ff]", "ф", text)
    text = re.sub("[Gg]", "дж", text)
    text = re.sub("[Hh]", "х", text)
    text = re.sub("[Ii]", "и", text)
    text = re.sub("[Jj]", "дж", text)
    text = re.sub("[Kk]", "к", text)
    text = re.sub("[Ll]", "л", text)
    text = re.sub("[Mm]", "м", text)
    text = re.sub("[Nn]", "н", text)
    text = re.sub("[Oo]", "о", text)
    text = re.sub("[Pp]", "п", text)
    text = re.sub("[Qq]", "к", text)
    text = re.sub("[Rr]", "р", text)
    text = re.sub("[Ss]", "с", text)
    text = re.sub("[Tt]", "т", text)
    text = re.sub("[Uu]", "ю", text)
    text = re.sub("[Vv]", "в", text)
    text = re.sub("[Ww]", "в", text)
    text = re.sub("[Xx]", "кс", text)
    text = re.sub("[Yy]", "у", text)
    text = re.sub("[Zz]", "з", text)
    
    return text


def latin_to_cyrillic(text):
    for match in re.findall("[a-zA-Z]+", text):
        if len(match) == 1: text = re.sub(match, single_latin_to_cyrillic(match), text, 1)
        else: text = re.sub(match, combined_latin_to_cyrillic(match), text, 1)
    
    return text


def numbers_to_words(text):
    """Find all numeric values and replace them by words."""
    for match in re.findall(r"[+-]?\d*[.,]?\d+", text):
        # "num2words" is a library that converts numbers to words.
        # It doesn"t work with commas.
        repl = num2words(re.sub(",", ".", match), lang="ru")
        # Replace the pattern by the repl: re.sub(pattern, repl, string, count).
        text = re.sub(match, repl, text, 1)
    
    return text


def check_readable_symbols(text):
    if re.search("[а-яА-Я]", text):
        return True
    else:
        return False


def prepare_book(book):
    book = sent_tokenize(book)
    
    return book


def prepare_sentence(sentence):
    sentence = numbers_to_words(sentence)
    sentence = latin_to_cyrillic(sentence)
    
    return sentence
