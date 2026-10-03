# -*- coding: utf-8 -*-
import unittest

from persian_tools import (ZWNJ, normalize, tokenize, remove_stopwords,
                           convert_digits, process)


class TestNormalize(unittest.TestCase):
    def test_arabic_letters_and_diacritics(self):
        self.assertEqual(normalize('سلامٌ عليكم'), 'سلام علیکم')

    def test_zwnj_preserved(self):
        self.assertEqual(normalize('کتاب‌هاي زيادي'), 'کتاب‌های زیادی')

    def test_mi_prefix(self):
        self.assertEqual(normalize('او می رود و نمی داند'), 'او می‌رود و نمی‌داند')

    def test_mi_inside_word_untouched(self):
        self.assertEqual(normalize('این کار رسمی شد'), 'این کار رسمی شد')

    def test_plural_suffix(self):
        self.assertEqual(normalize('کتاب ها'), 'کتاب' + ZWNJ + 'ها')

    def test_tatweel_removed(self):
        self.assertEqual(normalize('ســلام'), 'سلام')

    def test_newlines_kept(self):
        self.assertEqual(normalize('خط اول\n\n\n\nخط دوم'), 'خط اول\n\nخط دوم')

    def test_zwnj_edges_removed(self):
        self.assertEqual(normalize(ZWNJ + 'سلام' + ZWNJ + ' ' + ZWNJ + 'دنیا'), 'سلام دنیا')

    def test_uncommon_letters_unchanged(self):
        self.assertEqual(normalize('خانۀ مؤمن'), 'خانۀ مؤمن')

    def test_empty(self):
        self.assertEqual(normalize(''), '')


class TestDigits(unittest.TestCase):
    def test_to_en(self):
        self.assertEqual(convert_digits('۱۲۳ ١٢٣ 123', 'en'), '123 123 123')

    def test_to_fa(self):
        self.assertEqual(convert_digits('۱۲۳ ١٢٣ 123', 'fa'), '۱۲۳ ۱۲۳ ۱۲۳')

    def test_invalid(self):
        with self.assertRaises(ValueError):
            convert_digits('1', 'de')

    def test_process_respects_digits(self):
        self.assertEqual(process('عدد 123')['normalized'], 'عدد 123')
        self.assertEqual(process('عدد 123', digits='fa')['normalized'], 'عدد ۱۲۳')


class TestTokenize(unittest.TestCase):
    def test_persian_punctuation(self):
        self.assertEqual(tokenize('سلام، چطوری؟ خوبم؛ ممنون'),
                         ['سلام', '،', 'چطوری', '؟', 'خوبم', '؛', 'ممنون'])

    def test_decimal_kept(self):
        self.assertEqual(tokenize('عدد 3.14 است.'), ['عدد', '3.14', 'است', '.'])

    def test_zwnj_in_token(self):
        self.assertEqual(tokenize('می‌روم'), ['می‌روم'])

    def test_stopwords(self):
        self.assertEqual(remove_stopwords(tokenize('من به مدرسه رفتم')), ['مدرسه', 'رفتم'])


if __name__ == '__main__':
    unittest.main()
