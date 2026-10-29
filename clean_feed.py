import urllib.request
import re

SRC = "https://istore34.ru/tstore/yml/a9c0dadf06f66ec5739d3c829e0eb701.yml"
DST = "feed.yml"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://istore34.ru/",
    "Accept-Language": "ru-RU,ru;q=0.9"
}

req = urllib.request.Request(SRC, headers=headers)
with urllib.request.urlopen(req, timeout=30) as resp:
    raw_bytes = resp.read()

# --- ЛЕЧЕНИЕ КОДИРОВКИ ---
try:
    # Пробуем прочитать как UTF-8
    text = raw_bytes.decode("utf-8")
    # Если получилось, но похоже на кракозябры (например, есть 'Ð'), пробуем перекодировать
    if "Ð" in text and "Ñ" in text:
        text = text.encode("windows-1251").decode("utf-8")
except UnicodeDecodeError:
    # Если не получилось как UTF-8, значит это точно Windows-1251
    text = raw_bytes.decode("windows-1251")

# Чистка
text = text.replace("#nbsp;", " ")
text = text.replace("&nbsp;", " ")
text = text.replace("&#160;", " ")
text = text.replace("\u00A0", " ")
text = re.sub(r" {2,}", " ", text)

with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

print("Готово. Перекодировка выполнена.")
