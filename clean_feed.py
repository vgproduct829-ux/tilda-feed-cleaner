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

# ФОКУС: Читаем байты как Windows-1251 (потому что Тильда отдает в ней, но пишет в заголовке UTF-8)
# Игнорируем ошибки, чтобы скрипт не падал на спецсимволах
text = raw_bytes.decode("windows-1251", errors="ignore")

# Чистим пробелы
text = text.replace("#nbsp;", " ")
text = text.replace("&nbsp;", " ")
text = text.replace("&#160;", " ")
text = text.replace("\u00A0", " ")
text = text.replace("\xA0", " ")

# Убираем двойные пробелы
text = re.sub(r" {2,}", " ", text)

# Сохраняем в нормальном UTF-8
with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

print("Готово! Файл перекодирован из Windows-1251 в UTF-8.")
