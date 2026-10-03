# -*- coding: utf-8 -*-
"""
Persian Text Tools
ابزارهای ساده و کاربردی برای پردازش متن فارسی
"""

import re
import unicodedata
from typing import Dict, List, Union

ZWNJ = '\u200c'  # نیم‌فاصله

# ==================== Mapping ها ====================

# حروف عربی -> فارسی
# توجه: «ۀ» و «ؤ» عمداً تبدیل نمی‌شوند چون تغییر املا می‌دهند (خانۀ / مؤمن).
ARABIC_TO_PERSIAN = str.maketrans({
    'ي': 'ی',
    'ى': 'ی',
    'ك': 'ک',
    'ة': 'ه',
    'إ': 'ا',
    'أ': 'ا',
    'ٱ': 'ا',
})

PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
ARABIC_DIGITS = '٠١٢٣٤٥٦٧٨٩'
ENGLISH_DIGITS = '0123456789'

PERSIAN_TO_ENGLISH = str.maketrans(PERSIAN_DIGITS, ENGLISH_DIGITS)
ARABIC_TO_ENGLISH = str.maketrans(ARABIC_DIGITS, ENGLISH_DIGITS)
ENGLISH_TO_PERSIAN = str.maketrans(ENGLISH_DIGITS, PERSIAN_DIGITS)
ARABIC_TO_PERSIAN_DIGITS = str.maketrans(ARABIC_DIGITS, PERSIAN_DIGITS)

STOPWORDS = {
    'و', 'در', 'به', 'از', 'که', 'این', 'را', 'با', 'است', 'برای',
    'آن', 'یک', 'خود', 'تا', 'کرد', 'بر', 'هم', 'نیز', 'گفت', 'شد',
    'دارد', 'ما', 'اما', 'یا', 'شده', 'باید', 'هر', 'آنها', 'بود',
    'او', 'دیگر', 'دو', 'مورد', 'شود', 'کند', 'وجود', 'بین', 'پیش',
    'پس', 'اگر', 'همه', 'یکی', 'هستند', 'من', 'نیست', 'باشد', 'چه',
    'می', 'همین', 'همچنین', 'روی', 'داد', 'بیشتر',
    'بسیار', 'داشت', 'چند', 'سوی', 'تنها', 'هیچ', 'میان', 'شدن',
    'بعد', 'البته', 'مثل', 'حتی', 'بدون', 'قبل', 'زیرا',
    'چرا', 'چون', 'چگونه', 'کجا', 'کی', 'آیا', 'نه', 'بله', 'خیر',
    'مثلا', 'یعنی', 'چنین', 'آنچه'
}

# حروف فارسی/عربی (برای تشخیص مرز کلمه)
_LETTERS = '\u0621-\u063A\u0641-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC'

_DIACRITICS_RE = re.compile('[\u064B-\u065F\u0670\u0640]')  # اعراب + کشیده
_INVISIBLE_RE = re.compile('[\u200d\u200e\u200f\u202a-\u202e\u2066-\u2069\ufeff]')
_MI_RE = re.compile(r'(?<![%s%s])(ن?می) (?=[%s])' % (_LETTERS, ZWNJ, _LETTERS))
_SUFFIX_RE = re.compile(r'(?<=[%s]) (ها|های|هایی)(?![%s%s])' % (_LETTERS, _LETTERS, ZWNJ))
_TOKEN_RE = re.compile(r'\d+(?:[.,٫]\d+)+|(?:[^\W_]|%s)+|\S' % ZWNJ)


def _check_digits(digits: str) -> None:
    if digits not in ('en', 'fa'):
        raise ValueError("digits must be 'en' or 'fa', got %r" % (digits,))


# ==================== توابع اصلی ====================

def arabic_to_persian(text: str) -> str:
    """تبدیل حروف عربی به معادل فارسی"""
    return text.translate(ARABIC_TO_PERSIAN)


def convert_digits(text: str, to: str = 'en') -> str:
    """تبدیل اعداد فارسی/عربی/انگلیسی (to = 'en' یا 'fa')"""
    _check_digits(to)
    if to == 'en':
        return text.translate(PERSIAN_TO_ENGLISH).translate(ARABIC_TO_ENGLISH)
    return text.translate(ENGLISH_TO_PERSIAN).translate(ARABIC_TO_PERSIAN_DIGITS)


def remove_diacritics(text: str) -> str:
    """حذف اعراب و کشیده (ـ)"""
    return _DIACRITICS_RE.sub('', text)


def normalize_spaces(text: str) -> str:
    """
    نرمال‌سازی فاصله‌ها؛ نیم‌فاصله (ZWNJ) حفظ می‌شود و خط‌های جدید
    (حداکثر یک خط خالی) نگه داشته می‌شوند.
    """
    text = text.replace('\xa0', ' ')
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = _INVISIBLE_RE.sub('', text)
    text = re.sub('%s{2,}' % ZWNJ, ZWNJ, text)
    # نیم‌فاصله کنار فاصله/خط جدید بی‌معناست
    text = re.sub(r'%s*(\s)%s*' % (ZWNJ, ZWNJ), r'\1', text)
    text = re.sub(r'[^\S\n]+', ' ', text)
    text = re.sub(r' ?\n ?', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip(' \n' + ZWNJ)


def fix_half_spaces(text: str) -> str:
    """اصلاح نیم‌فاصله‌های رایج: «می رود» ← «می‌رود»، «کتاب ها» ← «کتاب‌ها»"""
    text = _MI_RE.sub(r'\1' + ZWNJ, text)
    text = _SUFFIX_RE.sub(ZWNJ + r'\1', text)
    return text


def normalize(text: str, digits: str = 'en') -> str:
    """نرمال‌سازی کامل متن فارسی"""
    _check_digits(digits)
    if not text:
        return text

    # NFKC: تبدیل شکل‌های نمایشی عربی (مثل ﻛ) به حرف استاندارد
    text = unicodedata.normalize('NFKC', text)
    text = arabic_to_persian(text)
    text = remove_diacritics(text)
    text = convert_digits(text, to=digits)
    text = normalize_spaces(text)
    text = fix_half_spaces(text)
    return text


def tokenize(text: str, digits: str = 'en', already_normalized: bool = False) -> List[str]:
    """
    توکن‌سازی ساده. علائم (از جمله ، ؛ ؟ « » …) توکن جداگانه‌اند،
    اعداد اعشاری مثل 3.14 یک توکن می‌مانند و نیم‌فاصله حفظ می‌شود.
    """
    if not already_normalized:
        text = normalize(text, digits=digits)
    return _TOKEN_RE.findall(text)


def remove_stopwords(tokens: List[str]) -> List[str]:
    """حذف کلمات ایست"""
    return [token for token in tokens if token not in STOPWORDS]


def process(text: str, remove_stops: bool = False, digits: str = 'en') -> Dict[str, Union[str, int, List[str]]]:
    """پردازش کامل متن"""
    normalized = normalize(text, digits=digits)
    tokens = tokenize(normalized, already_normalized=True)

    result = {
        'original': text,
        'normalized': normalized,
        'tokens': tokens,
        'token_count': len(tokens),
    }

    if remove_stops:
        clean_tokens = remove_stopwords(tokens)
        result['tokens_without_stopwords'] = clean_tokens
        result['clean_token_count'] = len(clean_tokens)

    return result


# ==================== نمونه ====================
if __name__ == '__main__':
    sample = "سلامٌ عليكم! من امروز به مدرسه رفتم و كتاب‌هاي زيادي خواندم. ١٢٣"

    print("متن اصلی:")
    print(sample)
    print("\n" + "=" * 50 + "\n")

    result = process(sample, remove_stops=True)

    print("نرمال‌سازی شده:")
    print(result['normalized'])
    print("\nتوکن‌ها:")
    print(result['tokens'])
    print("\nبدون کلمات ایست:")
    print(result['tokens_without_stopwords'])
