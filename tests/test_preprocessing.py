import importlib.util

def load_numbers_to_words(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.numbers_to_words

en_n2w = load_numbers_to_words("languages/English/preprocessing.py", "en_preprocessing")
ru_n2w = load_numbers_to_words("languages/Russian/preprocessing.py", "ru_preprocessing")

def test_english_number_conversion():
    assert  en_n2w("Rate was 4.25") == "Rate was four point two five"
    assert  en_n2w("He has 3 apples.") == "He has three apples."

def test_russian_number_conversion():
    assert ru_n2w("Курс был 4,25") == "Курс был четыре целых двадцать пять сотых"
    assert ru_n2w("У него 3 яблока.") == "У него три яблока."