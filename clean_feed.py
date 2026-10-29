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

# Мы жестко говорим: читай байты как Windows-1251, потому что Тильда для ботов отдает именно её.
text = raw_bytes.decode("windows-1251")

# Проверка на всякий случай: если вдруг это все-таки был UTF-8 (и мы получили кракозябры)
if "Ð" in text and "Ñ" in text:
    try:
        text = text.encode("windows-1251").decode("utf-8")
    except Exception:
        pass

# Чистка
text = text.replace("#nbsp;", " ")
text = text.replace("&nbsp;", " ")
text = text.replace("&#160;", " ")
text = text.replace("\u00A0", " ")
text = text.replace("\xA0", " ")
text = re.sub(r" {2,}", " ", text)

# Сохраняем в нормальном UTF-8
with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

print("Готово! Теперь точно должно быть чисто.")
