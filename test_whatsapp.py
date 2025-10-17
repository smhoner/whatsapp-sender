import pandas as pd
import urllib.parse
import webbrowser
import re
import time

EXCEL_PATH = "test_numaralar.xlsx"
DEFAULT_COUNTRY = "+90"  # Türkiye varsayılanı

def clean_number(raw):
    if pd.isna(raw):
        return None
    s = str(raw).strip()
    s = re.sub(r"[^\d+]", "", s)
    if s.startswith("+"):
        return s
    if s.startswith("0"):
        return DEFAULT_COUNTRY + s[-10:]
    if len(s) == 10:
        return DEFAULT_COUNTRY + s
    return s

# Excel'i oku
df = pd.read_excel(EXCEL_PATH)

# Telefon sütunundaki tüm numaraları al
phones = [clean_number(x) for x in df["Telefon"].dropna()]

# Gönderilecek mesaj
message = "Merhaba! Bu bir *deneme mesajıdır*. Her şey yolunda mı?"

# Her numara için WhatsApp Web penceresi aç
for phone in phones:
    url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"
    print(f"Açılıyor: {url}")
    webbrowser.open(url)
    # Her kişi arasında 7 saniye bekle (çok hızlı olmasın)
    time.sleep(7)

print("✅ Tüm numaralar işlendi. Tarayıcıda çıkan pencerelerde mesajı Gönder'e tıklayabilirsin.")
