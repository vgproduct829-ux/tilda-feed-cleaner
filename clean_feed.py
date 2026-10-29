import urllib.request
import re

# Ссылка на ваш фид Тильды
SRC = "https://istore34.ru/tstore/yml/a9c0dadf06f66ec5739d3c829e0eb701.yml"
DST = "feed.yml"

req = urllib.request.Request(SRC, headers={"User-Agent": "Mozilla/5.0"})
# Вот здесь мы жестко указываем кодировку UTF-8 при чтении
with urllib.request.urlopen(req, timeout=30) as resp:
    data = resp.read().decode("utf-8")

# Чистка
data = data.replace("#nbsp;", " ")
data = data.replace("&nbsp;", " ")
data = data.replace("&#160;", " ")
data = data.replace("\u00A0", " ")   # настоящий неразрывный пробел
data = re.sub(r" {2,}", " ", data)

# И жестко указываем кодировку при записи
with open(DST, "w", encoding="utf-8") as f:
    f.write(data)

print("Готово")
