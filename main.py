# -*- coding: utf-8 -*-
"""
CLI برای ابزارهای متن فارسی
"""

import argparse
import sys

from persian_tools import normalize, tokenize, remove_stopwords, process


def read_input(args, parser):
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                return f.read()
        except (OSError, UnicodeDecodeError) as e:
            parser.error('خواندن فایل ممکن نیست: %s' % e)
    if args.text:
        return args.text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='ابزارهای پردازش متن فارسی - Persian Text Tools'
    )
    parser.add_argument('text', nargs='?', help='متن ورودی (یا از stdin)')
    parser.add_argument('-f', '--file', help='خواندن متن از فایل (UTF-8)')
    parser.add_argument('-n', '--normalize', action='store_true', help='نرمال‌سازی متن')
    parser.add_argument('-t', '--tokenize', action='store_true', help='توکن‌سازی')
    parser.add_argument('-s', '--stopwords', action='store_true', help='حذف کلمات ایست')
    parser.add_argument('-a', '--all', action='store_true', help='پردازش کامل')
    parser.add_argument('--digits', choices=['en', 'fa'], default='en',
                        help='نوع اعداد خروجی (پیش‌فرض: انگلیسی)')

    args = parser.parse_args(argv)

    text = read_input(args, parser)
    if text is None:
        print("لطفاً متن یا فایل وارد کنید.")
        parser.print_help()
        return 1

    if args.all or not (args.normalize or args.tokenize or args.stopwords):
        result = process(text, remove_stops=True, digits=args.digits)
        print("متن نرمال‌سازی شده:")
        print(result['normalized'])
        print("\nتوکن‌ها:")
        print(' | '.join(result['tokens']))
        print("\nبدون کلمات ایست:")
        print(' | '.join(result['tokens_without_stopwords']))
        return 0

    if args.normalize:
        print(normalize(text, digits=args.digits))
    if args.tokenize or args.stopwords:
        tokens = tokenize(text, digits=args.digits)
        if args.tokenize:
            print(' | '.join(tokens))
        if args.stopwords:
            print(' | '.join(remove_stopwords(tokens)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
