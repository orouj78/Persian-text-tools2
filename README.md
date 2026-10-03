# Persian Text Tools

ابزار ساده و سبک برای پردازش متن فارسی با پایتون.

A simple and lightweight Persian (Farsi) text processing toolkit written in pure Python (no external dependencies, Python 3.7+).

## Features

- تبدیل حروف عربی به فارسی (ي ← ی، ك ← ک، …) و حذف اعراب و کشیده
- تبدیل اعداد فارسی / عربی / انگلیسی
- نرمال‌سازی فاصله‌ها با **حفظ نیم‌فاصله** و خط‌های جدید
- اصلاح نیم‌فاصله‌های رایج («می رود» ← «می‌رود»، «کتاب ها» ← «کتاب‌ها»)
- توکن‌سازی ساده با پشتیبانی از علائم فارسی (، ؛ ؟ « ») و اعداد اعشاری
- حذف کلمات ایست (Stopwords)

## Installation

فایل‌ها را دانلود کنید و داخل پوشه پروژه اجرا کنید؛ نیازی به نصب چیزی نیست.

## Usage

### استفاده به عنوان ماژول

```python
from persian_tools import normalize, tokenize, process

text = "سلامٌ عليكم! من كتاب‌هاي زيادي دارم. ١٢٣"
print(normalize(text))             # اعداد انگلیسی (پیش‌فرض)
print(normalize(text, digits='fa'))  # اعداد فارسی
print(tokenize(text))

result = process(text, remove_stops=True, digits='en')
print(result)
```

### استفاده از خط فرمان

```bash
# پردازش کامل
python main.py "سلام عليكم! من امروز به مدرسه رفتم."

# فقط نرمال‌سازی (با اعداد فارسی)
python main.py -n --digits fa "متن ۱۲۳ برای نرمال‌سازی"

# فقط توکن‌سازی
python main.py -t "توکن‌سازی این متن"

# حذف کلمات ایست
python main.py -s "من امروز به مدرسه رفتم"

# از فایل یا stdin
python main.py -f input.txt -n
cat input.txt | python main.py -t
```

## Tests

```bash
python -m unittest -v
```

## Notes

- «ۀ» و «ؤ» عمداً تغییر داده نمی‌شوند، چون تبدیل آن‌ها املای کلمه را عوض می‌کند.
- اصلاح نیم‌فاصله فقط برای «می/نمی» و پسوندهای «ها/های/هایی» انجام می‌شود و یک روش ساده مبتنی بر قاعده است، نه تحلیل صرفی کامل.

## License

MIT
