import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--lang=id-ID') 
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)

url = "https://www.google.com/maps/place/Pantai+Mutun/@-5.5146608,105.2602725,17z/data=!4m18!1m9!3m8!1s0x2e40d863ce0b6695:0xaff8f326c3a8d9e1!2sPantai+Mutun!8m2!3d-5.5143696!4d105.2633118!9m1!1b1!16s%2Fg%2F11b7q6zls0!3m7!1s0x2e40d863ce0b6695:0xaff8f326c3a8d9e1!8m2!3d-5.5143696!4d105.2633118!9m1!1b1!16s%2Fg%2F11b7q6zls0?entry=ttu&g_ep=EgoyMDI2MDMwMi4wIKXMDSoASAFQAw%3D%3D"

driver.get(url)
print("(1-20 detik)")
time.sleep(13)

print("Mencoba klik tombol 'Urutkan'...")
try:
    # Cari tombol "Urutkan ulasan"
    sort_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Urutkan ulasan' or @aria-label='Sort reviews' or contains(@data-value, 'Urutkan')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sort_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", sort_btn)
    print("Tombol 'Urutkan' berhasil diklik! Menunggu menu pop-up muncul...")
    time.sleep(3) 
    newest_opt = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='menuitemradio' and (contains(., 'Terbaru') or contains(., 'Newest'))]")))
    
    # Klik opsi Terbaru
    driver.execute_script("arguments[0].click();", newest_opt)
    print("Berhasil memilih opsi 'Terbaru'!")
    time.sleep(8) 

except Exception as e:
    print(f"❌ Gagal melakukan sorting. Error: {e}")
    print("Bot akan tetap melanjutkan mengekstrak data ulasan seadanya (Paling Relevan).")

print("Scrolling untuk memperbanyak ulasan...")
try:
    scroll_pane = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "m6QErb") and (contains(@aria-label, "Ulasan") or contains(@aria-label, "Ulasan"))]')))
    print("Panel scrollable utama DITEMUKAN!")
except:
    print("Fallback ke container besar...")
    scroll_pane = driver.find_element(By.XPATH, '//div[contains(@class, "m6QErb")]')

last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_pane)

reviews = [] 
current_count = 0
max_attempts = 50
stuck_counter = 0 

while current_count < 350 and max_attempts > 0:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_pane)
    time.sleep(2) 
    
    review_cards = driver.find_elements(By.XPATH, '//div[@data-review-id]')
    unique_ids = set([card.get_attribute("data-review-id") for card in review_cards])
    current_count = len(unique_ids)
    driver.execute_script("""
        // 1. Cari semua kartu ulasan
        var cards = document.querySelectorAll('div[data-review-id]');
        if (cards.length > 0) {
            var lastCard = cards[cards.length - 1];
            
            // 2. Bawa kartu terakhir ke layar 
            lastCard.scrollIntoView(true);
            
            // 3. Cari wadah aslinya secara otomatis dengan merambat ke atas
            var parent = lastCard.parentElement;
            while (parent != null) {
                // Jika elemen parent ini punya scrollbar (tinggi isinya > tinggi layarnya)
                if (parent.scrollHeight > parent.clientHeight) {
                    parent.scrollTop = parent.scrollHeight; // Paksa turun mentok
                    break; // Berhenti mencari setelah ketemu
                }
                parent = parent.parentElement;
            }
        }
    """)
    
    # Beri waktu 5 detik agar animasi loading bulat-bulat Google selesai
    time.sleep(5)
    
    # Hitung ulasan unik yang ada di layar (agar yang kembar tidak dihitung)
    review_cards = driver.find_elements(By.XPATH, '//div[@data-review-id]')
    unique_ids = set([card.get_attribute("data-review-id") for card in review_cards])
    current_count = len(unique_ids)
    
    print(f"Ulasan ter-load: {current_count}")

    if current_count >= 350:
        print("✅ Target 350 ulasan tercapai!")
        break

    # Cek apakah setelah scroll angkanya nambah atau jalan di tempat
    if current_count == last_height:
        stuck_counter += 1
        print(f"   ⚠️ Loading tertahan... (Percobaan {stuck_counter}/4)")
        if stuck_counter >= 4:
            print("❌ Loading benar-benar mentok. Ulasan mungkin sudah habis.")
            break
    else:
        stuck_counter = 0 # Reset kalau berhasil nambah
        
    last_height = current_count
    max_attempts -= 1

for card in review_cards[:350]:
    try:
        try:
            name_elem = card.find_element(By.XPATH, './/button[contains(@aria-label, "Foto")]')
            name = name_elem.get_attribute('aria-label').replace("Foto ", "").strip()
        except:
            try:
                name = card.find_element(By.XPATH, './/div[contains(@class, "d4r55")]').text.strip()
            except:
                name = "Anonymous"

        try:
            rating_elem = card.find_element(By.XPATH, './/span[contains(@aria-label, "bintang") or contains(@aria-label, "star")]')
            rating = rating_elem.get_attribute('aria-label').split()[0]
        except:
            rating = "N/A"

        try:
            date = card.find_element(By.XPATH, './/span[contains(@class, "rsqaWe")]').text.strip()
        except:
            date = "N/A"

        try:
            more = card.find_element(By.XPATH, './/button[contains(@aria-label, "Lainnya") or contains(@aria-label, "More") or contains(@aria-expanded, "false")]')
            driver.execute_script("arguments[0].click();", more)
            time.sleep(1.5)
        except:
            pass

        try:
            text_elem = card.find_elements(By.XPATH, './/span[contains(@class, "wiI7pd") or @dir="ltr"]')
            text = text_elem[0].text.strip() if text_elem else ""
        except:
            text = ""

        reviews.append({
            'name': name,
            'rating': rating,
            'date': date,
            'text': text
        })
    except Exception as e:
        continue

driver.quit()

# Output hasil
df = pd.DataFrame(reviews)
print(f"\nSUKSES! Berhasil ambil {len(df)}.")

print(df.head(15)) # Fallback jika berjalan di terminal biasa

# File siap 
df.to_csv('dataset_ulasan_mutun.csv', index=False, encoding='utf-8')
print("File CSV siap!")