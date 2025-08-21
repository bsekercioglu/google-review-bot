# Google Firma Adresleri Rehberi 📍

Bu rehber, Google Maps'teki işletme adreslerinin nasıl bulunacağını ve `businesses.json` dosyasına nasıl ekleneceğini detaylı olarak açıklar.

## 📋 İçindekiler

1. [Google Maps'te İşletme Arama](#google-mapste-işletme-arama)
2. [İşletme URL'sini Alma](#işletme-urlsini-alma)
3. [İşletme Bilgilerini Toplama](#işletme-bilgilerini-toplama)
4. [JSON Dosyasına Ekleme](#json-dosyasına-ekleme)
5. [Otomatik Toplama Araçları](#otomatik-toplama-araçları)
6. [Yasal ve Etik Kurallar](#yasal-ve-etik-kurallar)
7. [Sık Sorulan Sorular](#sık-sorulan-sorular)

---

## 🔍 Google Maps'te İşletme Arama

### 1. Manuel Arama Yöntemi

#### Adım 1: Google Maps'i Açın
- [maps.google.com](https://maps.google.com) adresine gidin
- Veya Google Maps uygulamasını açın

#### Adım 2: İşletme Türünü Belirleyin
```
Örnek arama terimleri:
- "restoran İstanbul"
- "kafe Kadıköy"
- "otel Beşiktaş"
- "diş hekimi Bakırköy"
- "spor salonu Maltepe"
```

#### Adım 3: Filtreleme Yapın
- **Konum**: Belirli bir şehir, ilçe veya mahalle
- **Tür**: Restoran, kafe, otel, mağaza vb.
- **Değerlendirme**: 3+ yıldız, 4+ yıldız vb.
- **Mesafe**: Belirli bir yarıçap içinde

### 2. Gelişmiş Arama Teknikleri

#### Boolean Operatörler
```
"restoran" AND "İstanbul" AND "Türk mutfağı"
"kafe" OR "kahve" AND "Kadıköy"
"otel" NOT "hostel" AND "Beşiktaş"
```

#### Özel Arama Terimleri
```
"en iyi restoranlar İstanbul"
"popüler kafeler Kadıköy"
"lüks oteller Beşiktaş"
"uygun fiyatlı spor salonları"
```

---

## 🔗 İşletme URL'sini Alma

### 1. Web Tarayıcısından Alma

#### Adım 1: İşletmeyi Bulun
- Google Maps'te arama yapın
- İstediğiniz işletmeye tıklayın

#### Adım 2: URL'yi Kopyalayın
- Tarayıcının adres çubuğundaki URL'yi kopyalayın
- URL formatı: `https://www.google.com/maps/place/[İşletme+Adı]/@[Koordinatlar]`

#### Örnek URL:
```
https://www.google.com/maps/place/Kebapçı+Mehmet+Usta/@41.0082,28.9784,17z/data=!3m1!4b1!4m5!3m4!1s0x14caa4c7c5c5c5c5:0x5c5c5c5c5c5c5c5c!8m2!3d41.0082!4d28.9784
```

### 2. Mobil Uygulamadan Alma

#### Android:
1. İşletmeye tıklayın
2. "Paylaş" butonuna tıklayın
3. "Kopyala" seçeneğini seçin

#### iOS:
1. İşletmeye tıklayın
2. "Paylaş" butonuna tıklayın
3. "Kopyala" seçeneğini seçin

### 3. URL Temizleme

#### Gereksiz Parametreleri Kaldırın:
```
❌ Uzun URL:
https://www.google.com/maps/place/Kebapçı+Mehmet+Usta/@41.0082,28.9784,17z/data=!3m1!4b1!4m5!3m4!1s0x14caa4c7c5c5c5c5:0x5c5c5c5c5c5c5c5c!8m2!3d41.0082!4d28.9784

✅ Temizlenmiş URL:
https://www.google.com/maps/place/Kebapçı+Mehmet+Usta/@41.0082,28.9784,17z
```

---

## 📊 İşletme Bilgilerini Toplama

### 1. Temel Bilgiler

Her işletme için toplanması gereken bilgiler:

```json
{
  "id": "biz_001",
  "name": "İşletme Adı",
  "url": "Google Maps URL'si",
  "type": "İşletme türü",
  "category": "Kategori",
  "location": "Konum",
  "max_rating": 5,
  "min_rating": 3,
  "review_count": 0,
  "last_review_date": null,
  "status": "active",
  "notes": "Notlar"
}
```

### 2. İşletme Türleri

Desteklenen işletme türleri:

| Tür | Açıklama | Örnek |
|-----|----------|-------|
| `restaurant` | Restoran | Kebapçı, pizzacı |
| `cafe` | Kafe | Kahve dükkanı |
| `hotel` | Otel | Konaklama tesisi |
| `shop` | Mağaza | Giyim, elektronik |
| `medical` | Sağlık | Doktor, hastane |
| `beauty` | Güzellik | Kuaför, spa |
| `fitness` | Spor | Spor salonu |
| `education` | Eğitim | Kurs, okul |
| `service` | Hizmet | Oto yıkama, tamir |

### 3. Konum Formatı

```
Örnek konumlar:
- "İstanbul, Fatih"
- "İstanbul, Beşiktaş, Levent"
- "Ankara, Çankaya"
- "İzmir, Konak"
```

### 4. Yıldız Aralığı

```json
{
  "max_rating": 5,  // Maksimum verilecek yıldız
  "min_rating": 3   // Minimum verilecek yıldız
}
```

---

## 📝 JSON Dosyasına Ekleme

### 1. Manuel Ekleme

`businesses.json` dosyasını açın ve yeni işletme ekleyin:

```json
{
  "id": "biz_011",
  "name": "Yeni İşletme Adı",
  "url": "https://www.google.com/maps/place/Yeni+İşletme/@41.0082,28.9784,17z",
  "type": "restaurant",
  "category": "Türk Mutfağı",
  "location": "İstanbul, Şişli",
  "max_rating": 5,
  "min_rating": 4,
  "review_count": 0,
  "last_review_date": null,
  "status": "active",
  "notes": "Yeni açılan restoran"
}
```

### 2. Otomatik Ekleme

Python script ile otomatik ekleme:

```python
from business_manager import BusinessManager

# İşletme yöneticisini başlat
bm = BusinessManager()
bm.load_businesses()

# Yeni işletme ekle
new_business = {
    "name": "Yeni İşletme",
    "url": "https://www.google.com/maps/place/Yeni+İşletme/@41.0082,28.9784,17z",
    "type": "restaurant",
    "category": "Türk Mutfağı",
    "location": "İstanbul, Şişli",
    "max_rating": 5,
    "min_rating": 4,
    "notes": "Yeni açılan restoran"
}

bm.add_business(new_business)
```

### 3. Toplu Ekleme

CSV dosyasından toplu ekleme:

```python
import csv
from business_manager import BusinessManager

bm = BusinessManager()
bm.load_businesses()

with open('yeni_isletmeler.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        business = {
            "name": row['name'],
            "url": row['url'],
            "type": row['type'],
            "category": row['category'],
            "location": row['location'],
            "max_rating": int(row['max_rating']),
            "min_rating": int(row['min_rating']),
            "notes": row.get('notes', '')
        }
        bm.add_business(business)
```

---

## 🤖 Otomatik Toplama Araçları

### 1. Google Places API

```python
import googlemaps
from business_manager import BusinessManager

# API anahtarınızı ayarlayın
gmaps = googlemaps.Client(key='YOUR_API_KEY')

def search_businesses(query, location):
    places_result = gmaps.places_nearby(
        location=location,
        radius=5000,
        type='restaurant',
        keyword=query
    )
    
    bm = BusinessManager()
    bm.load_businesses()
    
    for place in places_result['results']:
        business = {
            "name": place['name'],
            "url": f"https://www.google.com/maps/place/{place['place_id']}",
            "type": "restaurant",
            "category": "Restoran",
            "location": location,
            "max_rating": 5,
            "min_rating": 3,
            "notes": f"API ile bulundu: {place.get('rating', 'N/A')}⭐"
        }
        bm.add_business(business)
```

### 2. Web Scraping (Selenium)

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_google_maps(query, location):
    driver = webdriver.Chrome()
    driver.get(f"https://www.google.com/maps/search/{query}+{location}")
    
    # İşletmeleri bul
    businesses = driver.find_elements(By.CSS_SELECTOR, '[data-result-index]')
    
    for business in businesses[:10]:  # İlk 10 işletme
        try:
            name = business.find_element(By.CSS_SELECTOR, 'h3').text
            url = business.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            
            # İşletmeyi ekle
            add_business_to_json(name, url, "restaurant", location)
            
        except Exception as e:
            print(f"Hata: {e}")
    
    driver.quit()
```

### 3. Hazır Araçlar

#### Google My Business API
- Resmi Google API'si
- Ücretli ama güvenilir
- Rate limit'leri var

#### ScrapingBee
- Web scraping servisi
- Proxy desteği
- Kolay kullanım

#### Apify
- Hazır scraper'lar
- Google Maps scraper mevcut
- Ücretli servis

---

## ⚖️ Yasal ve Etik Kurallar

### 1. Yasal Uyarılar

⚠️ **ÖNEMLİ**: Bu araç sadece eğitim amaçlıdır!

- Google'ın kullanım şartlarını ihlal etmeyin
- Rate limiting kurallarına uyun
- Kişisel veri koruma kanunlarına uyun
- Ticari kullanım için izin alın

### 2. Etik Kurallar

✅ **Yapılması Gerekenler:**
- Gerçek müşteri deneyimlerine dayalı yorumlar
- Doğru ve dürüst değerlendirmeler
- İşletme sahiplerinin izni
- Şeffaf ve açık iletişim

❌ **Yapılmaması Gerekenler:**
- Sahte yorumlar
- Yanıltıcı bilgiler
- Spam içerik
- Manipülatif değerlendirmeler

### 3. Rate Limiting

```
Önerilen limitler:
- Dakikada maksimum 10 istek
- Saatte maksimum 100 istek
- Günde maksimum 1000 istek
- İstekler arası 2-5 saniye bekleme
```

---

## ❓ Sık Sorulan Sorular

### Q1: Google Maps'te işletme bulamıyorum, ne yapmalıyım?

**A:** 
- Farklı arama terimleri deneyin
- Konum filtresini genişletin
- İşletme türünü değiştirin
- Google My Business'te kayıtlı olup olmadığını kontrol edin

### Q2: URL'yi kopyaladım ama çalışmıyor?

**A:**
- URL'yi temizleyin (gereksiz parametreleri kaldırın)
- İşletme adındaki özel karakterleri kontrol edin
- URL'nin doğru formatta olduğundan emin olun

### Q3: Kaç işletme ekleyebilirim?

**A:**
- Teknik olarak sınırsız
- Performans için 100-500 arası önerilir
- Her işletme için benzersiz ID kullanın

### Q4: İşletme bilgilerini güncellemek istiyorum?

**A:**
```python
from business_manager import BusinessManager

bm = BusinessManager()
bm.load_businesses()

# İşletmeyi bul ve güncelle
business = bm.get_business_by_id("biz_001")
if business:
    business['name'] = "Yeni İsim"
    business['max_rating'] = 4
    bm.save_businesses()
```

### Q5: İşletme listesini yedeklemek istiyorum?

**A:**
```python
import shutil
from datetime import datetime

# Yedek dosya oluştur
backup_name = f"businesses_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
shutil.copy("businesses.json", backup_name)
```

---

## 📞 Destek

Herhangi bir sorun yaşarsanız:

1. **Log dosyalarını kontrol edin**: `bot.log`
2. **Hata mesajlarını okuyun**: Terminal çıktısı
3. **Dokümantasyonu inceleyin**: Bu rehber
4. **Test dosyalarını çalıştırın**: `test_business_manager.py`

---

## 🔄 Güncellemeler

Bu rehber düzenli olarak güncellenir. Son güncelleme: **15 Ocak 2024**

**Versiyon**: 1.0
**Yazar**: Google Review Bot Team
**Lisans**: Eğitim amaçlı kullanım için
