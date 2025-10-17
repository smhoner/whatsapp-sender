import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Chrome için gerekli modüller (otomatik driver indirme)
try:
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    Service = None
    ChromeDriverManager = None

# --- AYARLAR ---
EXCEL_PATH = "test_numaralar.xlsx"
DEFAULT_COUNTRY = "+90"
MESSAGE = "Merhaba! Bu mesaj otomatik olarak gönderilmiştir. 😊"

# --- NUMARA TEMİZLEME ---
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

# --- TARAYICI BAŞLATMA ---
def start_browser():
    try:
        print("🧩 Chrome deneniyor...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        print("✅ Chrome başarıyla başlatıldı.")
        return driver
    except Exception as e:
        print(f"⚠️ Chrome başlatılamadı ({e}). Safari'ye geçiliyor...")
        try:
            driver = webdriver.Safari()
            print("✅ Safari başarıyla başlatıldı.")
            return driver
        except Exception as e2:
            raise RuntimeError(f"Hiçbir tarayıcı başlatılamadı: {e2}")

# --- MESAJ GÖNDERME ---
def send_whatsapp_messages(driver, phones):
    driver.get("https://web.whatsapp.com")
    input("🔑 Lütfen QR kodu tara ve WhatsApp Web açıldığında Enter'a bas...")

    for phone in phones:
        link = f"https://web.whatsapp.com/send?phone={phone}&text={MESSAGE}"
        driver.get(link)
        time.sleep(10)  # yüklenmesini bekle

        try:
            # 1️⃣ Mesaj kutusunu bul
            input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            # 2️⃣ ENTER tuşu gönder
            input_box.send_keys(Keys.ENTER)
            print(f"✅ Gönderildi: {phone}")
        except Exception as e:
            print(f"❌ Gönderilemedi: {phone} ({e})")

        time.sleep(5)  # bir sonraki kişiye geçmeden bekle

# --- ANA PROGRAM ---
if __name__ == "__main__":
    df = pd.read_excel(EXCEL_PATH)
    phones = [clean_number(x) for x in df["Telefon"].dropna()]
    print(f"Toplam {len(phones)} numara bulundu.")
    
    driver = start_browser()
    send_whatsapp_messages(driver, phones)
    print("🎉 Tüm mesajlar başarıyla gönderildi!")
