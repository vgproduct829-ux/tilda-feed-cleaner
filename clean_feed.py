import urllib.request
import re
import codecs

# Ссылка на ваш фид Тильды
SRC = "https://istore34.ru/tstore/yml/a9c0dadf06f66ec5739d3c829e0eb701.yml"
DST = "feed.yml"

req = urllib.request.Request(SRC, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    # Читаем сырые байты
    raw_bytes = resp.read()

# Принудительно декодируем как UTF-8 (игнорируя возможные ошибки в начале файла BOM)
text = raw_bytes.decode("utf-8-sig")

# Чистка
text = text.replace("#nbsp;", " ")
text = text.replace("&nbsp;", " ")
text = text.replace("&#160;", " ")
text = text.replace("\u00A0", " ")
text = re.sub(r" {2,}", " ", text)

# Сохраняем в UTF-8 без BOM
with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

print("Готово. Кодировка исправлена.")
