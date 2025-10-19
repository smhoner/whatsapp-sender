import pandas as pd
import time
import re
import urllib.parse
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

EXCEL_PATH = "test_numaralar.xlsx"

# --- NUMARA TEMİZLEME ---
def clean_number(raw):
    if pd.isna(raw):
        return None
    s = str(raw).strip()
    s = re.sub(r"[^\d]", "", s)  # sadece rakamları tut
    
    if len(s) == 10:  # 532xxxxxxx gibi
        s = "90" + s
    elif len(s) == 11 and s.startswith("0"):  # 0532xxxxxxx
        s = "90" + s[1:]
    elif len(s) == 12 and s.startswith("90"):  # 90532xxxxxxx
        pass
    elif len(s) == 13 and s.startswith("+90"):  # +90532xxxxxxx
        s = s.replace("+", "")
    else:
        return None  # yanlış format
    return s

# --- TARAYICI BAŞLATMA ---
def start_browser():
    print("🧩 Chrome başlatılıyor...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    print("✅ Chrome başarıyla başlatıldı.")
    return driver

# --- MESAJ GÖNDERME ---
def send_whatsapp_messages(driver, df):
    driver.get("https://web.whatsapp.com")
    input("🔑 Lütfen QR kodunu tara ve WhatsApp Web açıldığında Enter'a bas...")

    for _, row in df.iterrows():
        name = str(row.get("Name", "")).strip()
        phone = clean_number(row.get("Phone"))

        if not phone:
            print(f"⚠️ Geçersiz numara atlandı: {row.get('Phone')}")
            continue

        # --- KİŞİSEL MESAJ ---
        message = (
            f"Selam {name}, artık sen de aramıza katılmaya hak kazandın!🥳\n"
            "Link üzerinden WhatsApp grubumuza katılabilirsin.\n"
            "Saat 16.00’da yapılacak duyuruları sakın kaçırma 😉\n\n"
            "👉🏻 https://chat.whatsapp.com/Hs880GuLOg7EnoEUxbKPQf"
        )

        encoded_message = urllib.parse.quote(message)
        link = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"
        print(f"🔗 {link}")

        driver.get(link)
        time.sleep(10)

        try:
            input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            input_box.send_keys(Keys.ENTER)
            print(f"✅ Gönderildi: {name} ({phone})")
        except Exception as e:
            print(f"❌ Gönderilemedi: {name} ({phone}) ({e})")

        time.sleep(5)

# --- ANA PROGRAM ---
if __name__ == "__main__":
    df = pd.read_excel(EXCEL_PATH, dtype=str)
    df = df.fillna("")  # boş hücreleri doldur
    print(f"Toplam {len(df)} kişi bulundu.")

    driver = start_browser()
    send_whatsapp_messages(driver, df)
    print("🎉 Tüm mesajlar başarıyla gönderildi!")
