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

# 1. Читаем как UTF-8 (потому что Тильда отдает именно UTF-8)
text = raw_bytes.decode("utf-8", errors="replace")

# 2. МАГИЯ: чиним кракозябры
# Берем испорченный текст, переводим его в байты Windows-1251 и читаем как UTF-8
try:
    text = text.encode("windows-1251").decode("utf-8")
except Exception:
    # Если не получилось (вдруг там уже нормальный текст), оставляем как есть
    pass

# 3. Чистим от неразрывных пробелов
text = text.replace("#nbsp;", " ")
text = text.replace("&nbsp;", " ")
text = text.replace("&#160;", " ")
text = text.replace("\u00A0", " ")
text = text.replace("\xA0", " ")
text = re.sub(r" {2,}", " ", text)

# 4. Сохраняем
with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

print("Готово! Кракозябры уничтожены.")
