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

# ПРИНУДИТЕЛЬНО читаем как Windows-1251 (так как Тильда отдает байты в этой кодировке)
text = raw_bytes.decode("windows-1251", errors="replace")

# Теперь заменяем символы. Обратите внимание: в Windows-1251 неразрывный пробел это \xA0
text = text.replace("#nbsp;", " ")
text = text.replace("&nbsp;", " ")
text = text.replace("&#160;", " ")
text = text.replace("\xA0", " ")  # неразрывный пробел в Windows-1251
text = text.replace("\u00A0", " ") # на всякий случай
text = re.sub(r" {2,}", " ", text)

# Сохраняем уже в правильном UTF-8
with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

print("Готово. Кодировка исправлена на уровне байтов.")
