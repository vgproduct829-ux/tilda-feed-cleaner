import urllib.request
import re

SRC = "https://istore34.ru/tstore/yml/a9c0dadf06f66ec5739d3c829e0eb701.yml"
DST = "feed.yml"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://istore34.ru/"
}

req = urllib.request.Request(SRC, headers=headers)
with urllib.request.urlopen(req, timeout=30) as resp:
    raw_bytes = resp.read()

# 1. Читаем как UTF-8. Если вдруг там реально Windows-1251, игнорируем ошибки.
try:
    text = raw_bytes.decode("utf-8")
except UnicodeDecodeError:
    text = raw_bytes.decode("windows-1251", errors="replace")

# 2. ЛЕЧИМ КРАКОЗЯБРЫ
# Если мы видим символы 'Ð' и 'Ñ', значит текст был неправильно перекодирован.
# Мы берем эти символы, переводим их в байты (как будто это Windows-1251), и читаем как UTF-8.
if "Ð" in text or "Ñ" in text:
    try:
        text = text.encode("windows-1251", errors="ignore").decode("utf-8", errors="ignore")
    except Exception:
        pass

# 3. Чистим пробелы
text = text.replace("#nbsp;", " ")
text = text.replace("&nbsp;", " ")
text = text.replace("&#160;", " ")
text = text.replace("\u00A0", " ")
text = text.replace("\xA0", " ")

# Схлопываем двойные пробелы
text = re.sub(r" {2,}", " ", text)

# 4. Сохраняем
with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

print("Готово! Ошибка обойдена, текст вылечен.")
