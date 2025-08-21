# Gemini API Anahtarı Alma Rehberi 🔑

Bu rehber, Google Gemini AI API anahtarının nasıl alınacağını adım adım açıklar. Bu API anahtarı, Google Review Bot'un AI destekli değerlendirme metinleri oluşturması için gereklidir.

## 📋 İçindekiler

1. [Gereksinimler](#gereksinimler)
2. [Google AI Studio'ya Erişim](#google-ai-studioya-erisim)
3. [API Anahtarı Oluşturma](#api-anahtari-olusturma)
4. [API Anahtarını Kullanma](#api-anahtarini-kullanma)
5. [Güvenlik Önlemleri](#guvenlik-onlemleri)
6. [Kullanım Limitleri](#kullanim-limitleri)
7. [Sorun Giderme](#sorun-giderme)
8. [SSS (Sık Sorulan Sorular)](#sss)

## 🎯 Gereksinimler

### Temel Gereksinimler:
- ✅ Google hesabı (Gmail)
- ✅ İnternet bağlantısı
- ✅ Web tarayıcısı (Chrome, Firefox, Safari, Edge)
- ✅ 18 yaş üzeri olmak (API kullanım şartları)

### Desteklenen Ülkeler:
- 🌍 Türkiye dahil çoğu ülke
- ⚠️ Bazı ülkelerde kısıtlamalar olabilir

## 🚀 Google AI Studio'ya Erişim

### Adım 1: Google AI Studio'yu Açın
1. Web tarayıcınızda şu adrese gidin: [https://aistudio.google.com/](https://aistudio.google.com/)
2. "Get API key" veya "API anahtarı al" butonuna tıklayın

### Adım 2: Google Hesabınızla Giriş Yapın
1. Google hesabınızla giriş yapın
2. Eğer birden fazla hesabınız varsa, API anahtarı almak istediğiniz hesabı seçin
3. "Devam et" butonuna tıklayın

### Adım 3: Kullanım Şartlarını Kabul Edin
1. Gemini API kullanım şartlarını okuyun
2. "Kabul ediyorum" veya "I agree" butonuna tıklayın

## 🔑 API Anahtarı Oluşturma

### Adım 1: API Anahtarı Oluştur
1. Google AI Studio ana sayfasında "Create API key" veya "API anahtarı oluştur" butonuna tıklayın
2. "Create API key in new project" seçeneğini seçin
3. Proje adını girin (örn: "Google Review Bot")
4. "Create" butonuna tıklayın

### Adım 2: API Anahtarını Kopyalayın
1. Oluşturulan API anahtarını kopyalayın
2. **⚠️ ÖNEMLİ**: Bu anahtarı güvenli bir yere kaydedin
3. API anahtarı şu formatta olacak: `AIzaSyC...` (uzun bir string)

### Adım 3: API Anahtarını Test Edin
1. Google AI Studio'da "Test" sekmesine gidin
2. API anahtarınızı girin
3. Basit bir test mesajı gönderin
4. Yanıt alıyorsanız API anahtarınız çalışıyor demektir

## 🔧 API Anahtarını Kullanma

### Adım 1: .env Dosyası Oluşturun
1. Proje klasörünüzde `.env` dosyası oluşturun
2. Dosyaya şu satırı ekleyin:
```env
GEMINI_API_KEY=AIzaSyC...your_api_key_here...
```

### Adım 2: .env Dosyasını Güvenli Hale Getirin
1. `.gitignore` dosyasına `.env` satırını ekleyin
2. Bu sayede API anahtarınız GitHub'a yüklenmez

### Adım 3: Bot'u Test Edin
1. Terminal'de şu komutu çalıştırın:
```bash
python google_review_bot.py
```
2. Bot AI değerlendirme metinleri oluşturabiliyorsa başarılı demektir

## 🔒 Güvenlik Önlemleri

### API Anahtarı Güvenliği:
- ❌ API anahtarınızı asla kod içinde paylaşmayın
- ❌ GitHub'a yüklemeyin
- ❌ E-posta ile göndermeyin
- ✅ Sadece `.env` dosyasında saklayın
- ✅ `.env` dosyasını `.gitignore`'a ekleyin

### Kullanım Güvenliği:
- 🔄 API anahtarınızı düzenli olarak yenileyin
- 📊 Kullanım istatistiklerini takip edin
- ⚠️ Anormal kullanım durumunda Google'ı bilgilendirin

### Örnek .gitignore İçeriği:
```gitignore
# Environment variables
.env
.env.local
.env.production

# API Keys
*.key
api_keys.txt

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
```

## 📊 Kullanım Limitleri

### Ücretsiz Kullanım:
- 🆓 Aylık 15 milyon karakter
- 🆓 Dakikada 60 istek
- 🆓 Saniyede 1 istek

### Ücretli Kullanım:
- 💰 Ek kullanım için ücretlendirme
- 💰 Fiyatlandırma: $0.00025 / 1K karakter
- 💰 Yüksek hacimli kullanım için özel planlar

### Limit Kontrolü:
```python
# API kullanımını kontrol etmek için
import time

def check_api_limits():
    # Dakikada 60 istek limiti
    time.sleep(1)  # Her istek arasında 1 saniye bekle
```

## 🔧 Sorun Giderme

### Yaygın Sorunlar ve Çözümleri:

#### 1. "API key not found" Hatası
**Sorun**: API anahtarı bulunamıyor
**Çözüm**:
- `.env` dosyasının doğru konumda olduğunu kontrol edin
- API anahtarının doğru formatta olduğunu kontrol edin
- Dosya adının `.env` olduğunu kontrol edin (`.env.txt` değil)

#### 2. "Quota exceeded" Hatası
**Sorun**: API kullanım limiti aşıldı
**Çözüm**:
- Kullanım istatistiklerini kontrol edin
- Bir sonraki ayı bekleyin
- Ücretli plana geçin

#### 3. "Invalid API key" Hatası
**Sorun**: API anahtarı geçersiz
**Çözüm**:
- Yeni bir API anahtarı oluşturun
- Eski anahtarı silin
- `.env` dosyasını güncelleyin

#### 4. "Rate limit exceeded" Hatası
**Sorun**: Çok hızlı istek gönderiliyor
**Çözüm**:
- İstekler arasında bekleme süresi ekleyin
- Batch işlemleri kullanın

### Debug Modu:
```python
# Debug modunda API isteklerini izleyin
import os
import logging

logging.basicConfig(level=logging.DEBUG)
print(f"API Key: {os.getenv('GEMINI_API_KEY')[:10]}...")
```

## ❓ SSS (Sık Sorulan Sorular)

### Q: API anahtarı ücretsiz mi?
**A**: Evet, aylık 15 milyon karakter ücretsiz. Daha fazlası için ücretlendirme var.

### Q: API anahtarımı kaybettim, ne yapmalıyım?
**A**: Google AI Studio'ya gidin, eski anahtarı silin ve yeni bir tane oluşturun.

### Q: Birden fazla API anahtarı alabilir miyim?
**A**: Evet, farklı projeler için birden fazla API anahtarı alabilirsiniz.

### Q: API anahtarım çalışmıyor, ne yapmalıyım?
**A**: 
1. API anahtarının doğru kopyalandığını kontrol edin
2. `.env` dosyasının doğru konumda olduğunu kontrol edin
3. İnternet bağlantınızı kontrol edin
4. Google AI Studio'da test edin

### Q: Kullanım limitlerini nasıl kontrol edebilirim?
**A**: Google AI Studio'da "Usage" sekmesinden kullanım istatistiklerini görebilirsiniz.

### Q: API anahtarımı başkalarıyla paylaşabilir miyim?
**A**: Hayır, API anahtarınızı kimseyle paylaşmayın. Herkes kendi anahtarını almalı.

### Q: Bot çalışmıyor, API anahtarı gerekli mi?
**A**: Hayır, API anahtarı olmadan da bot çalışır ama fallback metinler kullanır.

## 📞 Destek

### Google AI Studio Destek:
- 🌐 [Google AI Studio Help](https://aistudio.google.com/help)
- 📧 [Support Email](mailto:ai-studio-support@google.com)
- 💬 [Community Forum](https://developers.google.com/community)

### Proje Destek:
- 📖 [README.md](README.md) - Proje dokümantasyonu
- 🐛 [GitHub Issues](https://github.com/bsekercioglu/google-review-bot/issues) - Hata bildirimi
- 💡 [GitHub Discussions](https://github.com/bsekercioglu/google-review-bot/discussions) - Sorular

## 🎯 Sonuç

Gemini API anahtarınızı aldıktan sonra:

1. ✅ `.env` dosyasına ekleyin
2. ✅ `.gitignore` dosyasına `.env` ekleyin
3. ✅ Bot'u test edin
4. ✅ Kullanım limitlerini takip edin
5. ✅ Güvenlik önlemlerini uygulayın

Artık Google Review Bot'unuz AI destekli değerlendirme metinleri oluşturabilir! 🚀

---

**Son Güncelleme**: 15 Ocak 2024  
**Versiyon**: 1.0  
**Yazar**: Google Review Bot Geliştirme Ekibi
