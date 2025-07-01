from languages.English.preprocessing import numbers_to_words as en_n2w
from languages.Russian.preprocessing import numbers_to_words as ru_n2w

def test_english_number_conversion():
    assert  en_n2w("Rate was 4.25") == "Rate was four point two five"
    assert  en_n2w("He has 3 apples.") == "He has three apples."

def test_russian_number_conversion():
    assert ru_n2w("Курс был 4,25") == "Курс был четыре целых двадцать пять сотых"
    assert ru_n2w("У него 3 яблока.") == "У него три яблока."