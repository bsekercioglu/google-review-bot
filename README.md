# Google İşletme Değerlendirme Botu

🤖 **AI DESTEKLİ** - ⚠️ **ÖNEMLİ UYARI: Bu proje SADECE EĞİTİM AMAÇLIDIR!**

## Açıklama

Bu bot, Google işletme sayfalarında otomatik olarak 5 yıldız değerlendirme bırakmak için tasarlanmıştır. **Sadece eğitim ve öğrenme amaçlıdır.**

### 🆕 Yeni Özellikler

Bot artık **Google Gemini AI**, **akıllı proxy yönetimi**, **hesap rotasyonu** ve **işletme rotasyonu** kullanarak gelişmiş özellikler sunar:
- 🤖 AI ile otomatik metin oluşturma
- 📋 10 farklı işletme türü desteği
- 🌍 Türkçe dil desteği
- 🔄 Her değerlendirme için farklı metin
- 📝 Fallback metinler (API olmadan da çalışır)
- 🌐 Otomatik proxy rotation ve yönetimi
- 🔍 Proxy test ve doğrulama
- 📊 Güvenilir proxy listeleri
- 🔐 **Çoklu hesap yönetimi ve rotasyonu**
- 📊 **Hesap durumu takibi**
- ⏳ **Otomatik bekleme süreleri**
- 🚫 **Banlanmış hesap yönetimi**
- 🏢 **İşletme rotasyonu ve yönetimi**
- ⭐ **Akıllı yıldız dağılımı**
- 📍 **Çoklu işletme desteği**

## ⚠️ Yasal Uyarı

- Google'ın hizmet şartlarını ihlal edebilir
- Hesap banlanmasına neden olabilir
- Yasal sorunlara yol açabilir
- **Gerçek işletmelerde kullanmayın!**

## Gereksinimler

- Python 3.8+
- Google Chrome tarayıcısı
- İnternet bağlantısı
- **Google hesabı** (değerlendirme bırakmak için zorunlu)
- **Google Gemini API anahtarı** (AI özelliği için, isteğe bağlı)

## Kurulum

1. **Python paketlerini yükleyin:**
```bash
pip install -r requirements.txt
```

2. **Chrome tarayıcısının yüklü olduğundan emin olun**

3. **AI özelliği için (isteğe bağlı):**
   - [Google AI Studio](https://makersuite.google.com/app/apikey)'dan API anahtarı alın
   - `env.example` dosyasını `.env` olarak kopyalayın ve API anahtarını ekleyin:
   ```bash
   copy env.example .env
   # .env dosyasını düzenleyin ve API anahtarınızı ekleyin
   ```

4. **Bot'u çalıştırın:**
```bash
python google_review_bot.py
```

## Kullanım

1. Bot çalıştırıldığında sizden şu bilgileri isteyecek:
   - **İşletme seçimi** (liste veya tek işletme)
   - Google işletme URL'si (tek işletme seçilirse)
   - **Hesap yönetimi seçeneği** (liste veya tek hesap)
   - **AI kullanımı seçeneği** (yeni!)
   - **Proxy kullanımı seçeneği** (yeni!)
   - İşletme türü (AI seçilirse)
   - Değerlendirme metni (AI seçilmezse)
   - Kaç değerlendirme bırakılacağı

2. **İşletme Seçimi Seçenekleri:**
   - 🏢 **İşletme listesi kullan** (önerilen)
   - 🔗 **Tek işletme URL'si girin**

3. **Hesap Yönetimi Seçenekleri:**
   - 📋 **Hesap listesi kullan** (önerilen)
   - 🔐 **Tek hesap girişi**

3. **AI Özelliği Seçenekleri:**
   - 🤖 **AI ile otomatik metin oluşturma** (önerilen)
   - 📝 **Kendi metninizi girin**

4. **Proxy Seçenekleri:**
   - 🚫 **Proxy kullanma** (varsayılan)
   - 🌐 **Manuel proxy** (.env dosyasından)
   - 🔄 **Otomatik proxy rotation** (önerilen)

5. Bot otomatik olarak:
   - Chrome tarayıcısını açar
   - **İşletme listesinden rastgele işletme seçer** (işletme rotasyonu aktifse)
   - **Hesap listesinden sırayla hesap seçer**
   - **Google hesabına giriş yapar**
   - İşletme sayfasına gider
   - Değerlendirme formunu doldurur
   - **İşletme türüne göre rastgele yıldız verir** (3-5 arası)
   - AI ile oluşturulan veya kullanıcının verdiği metni yazar ve gönderir
   - **Hesap kullanımını kaydeder ve rotasyon yapar**
   - **İşletme kullanımını kaydeder ve rotasyon yapar**

## Özellikler

- **🏢 Çoklu İşletme Yönetimi**: JSON dosyasından işletme listesi
- **🔄 İşletme Rotasyonu**: Rastgele işletme seçimi
- **⭐ Akıllı Yıldız Sistemi**: İşletme türüne göre rastgele yıldız dağılımı
- **📊 İşletme Durumu Takibi**: Aktif, tamamlanmış, hata durumları
- **🔐 Çoklu Hesap Yönetimi**: JSON/CSV dosyalarından hesap listesi
- **🔄 Hesap Rotasyonu**: Otomatik hesap değiştirme
- **📊 Hesap Durumu Takibi**: Aktif, bekleme, banlanmış durumları
- **⏳ Otomatik Bekleme**: Hesap kullanımı arası 24 saat bekleme
- **🚫 Ban Yönetimi**: Banlanmış hesapları otomatik işaretleme
- **🔐 Google Giriş**: Otomatik Google hesap girişi
- **🔐 2FA Desteği**: İki faktörlü doğrulama desteği
- **🤖 AI Destekli**: Google Gemini AI ile rastgele değerlendirme metinleri
- **📋 İşletme Türü Desteği**: 10 farklı işletme kategorisi
- **🌍 Çok Dilli**: Türkçe dil desteği
- **🔄 Fallback Sistemi**: API olmadan da çalışır
- **Anti-detection**: Bot tespitini önlemek için çeşitli teknikler
- **İnsan benzeri davranış**: Rastgele gecikmeler ve yavaş yazma
- **User-Agent rastgeleleştirme**: Her çalıştırmada farklı tarayıcı kimliği
- **Proxy desteği**: IP gizleme için proxy kullanımı
- **Detaylı loglama**: Tüm işlemler log dosyasına kaydedilir

## Güvenlik Önlemleri

- Rastgele gecikmeler (2-5 saniye)
- Değerlendirmeler arası uzun bekleme (30-60 saniye)
- Tarayıcı otomasyon belirtilerini gizleme
- User-Agent rastgeleleştirme

## Dosya Yapısı

```
google-review-bot/
├── google_review_bot.py    # Ana bot dosyası
├── account_manager.py      # Hesap yönetim modülü
├── proxy_manager.py        # Proxy yönetim modülü
├── test_account_manager.py # Hesap yönetimi test dosyası
├── test_proxy_manager.py   # Proxy yönetimi test dosyası
├── test_ai_reviews.py      # AI test dosyası
├── test_bot.py             # Bot test dosyası
├── proxy_lists.md          # Güvenilir proxy listeleri
├── proxy_guide.md          # Proxy yönetimi kılavuzu
├── accounts.json           # Hesap listesi (JSON format)
├── accounts.csv            # Hesap listesi (CSV format)
├── proxies.json            # Proxy listesi (JSON format)
├── requirements.txt         # Python paketleri
├── README.md               # Bu dosya
├── env.example             # Örnek konfigürasyon dosyası
├── .env                    # API anahtarları (kullanıcı oluşturur)
└── bot.log                 # Log dosyası (çalıştırıldığında oluşur)
```

## Sorun Giderme

### Chrome Driver Hatası
```bash
pip install --upgrade webdriver-manager
```

### Selenium Hatası
```bash
pip install --upgrade selenium
```

### Tarayıcı Açılmıyor
- Chrome tarayıcısının yüklü olduğundan emin olun
- Antivirus yazılımını geçici olarak devre dışı bırakın

## Geliştirici Notları

Bu bot şu teknolojileri kullanır:
- **Selenium WebDriver**: Web otomasyon
- **ChromeDriver**: Chrome tarayıcı kontrolü
- **Fake UserAgent**: Tarayıcı kimliği gizleme
- **Python-dotenv**: Çevre değişkenleri yönetimi
- **Google Gemini AI**: Değerlendirme metni oluşturma
- **Google Generative AI**: AI API entegrasyonu

## Test

Hesap yönetimini test etmek için:
```bash
python test_account_manager.py
```

Proxy yönetimini test etmek için:
```bash
python test_proxy_manager.py
```

AI özelliklerini test etmek için:
```bash
python test_ai_reviews.py
```

Bot fonksiyonlarını test etmek için:
```bash
python test_bot.py
```

## Katkıda Bulunma

Bu proje sadece eğitim amaçlıdır. Gerçek kullanım için geliştirilmesi önerilmez.

## Lisans

Bu proje eğitim amaçlıdır ve herhangi bir lisans altında değildir.

## İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---

**Tekrar hatırlatma: Bu bot sadece eğitim amaçlıdır ve gerçek işletmelerde kullanılmamalıdır!**
