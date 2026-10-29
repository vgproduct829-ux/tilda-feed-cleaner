import subprocess
import re

SRC = "https://istore34.ru/tstore/yml/a9c0dadf06f66ec5739d3c829e0eb701.yml"
DST = "feed.yml"

# Используем системную утилиту curl. Она работает на уровне сети и обходит блокировки кодировок.
try:
    # Скачиваем через curl с заголовком User-Agent
    result = subprocess.run(
        ["curl", "-s", "-L", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", SRC],
        capture_output=True
    )
    raw_bytes = result.stdout
except Exception as e:
    print(f"Ошибка скачивания: {e}")
    exit(1)

# Теперь у нас есть чистые байты. Читаем их как UTF-8 (так как Тильда отдает именно UTF-8)
text = raw_bytes.decode("utf-8", errors="replace")

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

print("Готово! Файл скачан через curl и сохранен в чистом UTF-8.")
