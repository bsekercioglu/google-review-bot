# 🌐 Güvenilir Proxy Listeleri

⚠️ **ÖNEMLİ UYARI: Bu listeler sadece bilgilendirme amaçlıdır. Kullanım sorumluluğu kullanıcıya aittir.**

## 📋 İçindekiler

1. [Ücretsiz Proxy Servisleri](#ücretsiz-proxy-servisleri)
2. [Ücretli Premium Proxy Servisleri](#ücretli-premium-proxy-servisleri)
3. [Proxy Test ve Doğrulama Araçları](#proxy-test-ve-doğrulama-araçları)
4. [Proxy Türleri](#proxy-türleri)
5. [Güvenlik Önerileri](#güvenlik-önerileri)
6. [Bot İçin Proxy Ayarlama](#bot-için-proxy-ayarlama)

---

## 🆓 Ücretsiz Proxy Servisleri

### 🔄 Otomatik Güncelenen Listeler

#### 1. **Free Proxy List**
- **Website:** https://free-proxy-list.net/
- **Güncelleme:** Gerçek zamanlı
- **Türler:** HTTP, HTTPS, SOCKS4, SOCKS5
- **Özellik:** Ülke filtreleme, anonimlik seviyesi
- **Format:** IP:Port

#### 2. **ProxyList.geonode.com**
- **Website:** https://proxylist.geonode.com/
- **Güncelleme:** Günlük
- **Türler:** HTTP, HTTPS, SOCKS4, SOCKS5
- **Özellik:** API desteği, JSON format
- **Örnek:** `195.123.45.67:8080`

#### 3. **SSL Proxies**
- **Website:** https://www.sslproxies.org/
- **Güncelleme:** Saatlik
- **Türler:** HTTPS
- **Özellik:** SSL destekli
- **Güvenlik:** Yüksek

#### 4. **HideMyName**
- **Website:** https://hidemy.name/tr/proxy-list/
- **Güncelleme:** Sürekli
- **Türler:** HTTP, HTTPS, SOCKS4, SOCKS5
- **Özellik:** Türkçe arayüz, detaylı filtreleme
- **Ülkeler:** 100+ ülke

#### 5. **ProxyNova**
- **Website:** https://www.proxynova.com/proxy-server-list/
- **Güncelleme:** Günlük
- **Türler:** HTTP, HTTPS
- **Özellik:** Hız testi, uptime bilgisi

### 📝 Örnek Ücretsiz Proxy Listesi

```
# HTTP Proxies
104.248.63.15:30588
178.62.201.21:80
159.65.69.186:9300
167.172.109.12:39533

# HTTPS Proxies
185.162.231.166:80
45.67.212.45:8085
103.149.162.194:80
177.222.118.23:8080

# SOCKS5 Proxies
72.221.164.34:60671
184.178.172.5:15303
72.195.34.59:4145
184.178.172.25:15291
```

---

## 💰 Ücretli Premium Proxy Servisleri

### 🏆 En Güvenilir Servisler

#### 1. **Bright Data (Luminati)**
- **Website:** https://brightdata.com/
- **Fiyat:** $500+/ay
- **Özellik:** 72M+ IP, 195 ülke
- **Güvenilirlik:** ⭐⭐⭐⭐⭐
- **Kullanım:** Kurumsal, yüksek hacim

#### 2. **Oxylabs**
- **Website:** https://oxylabs.io/
- **Fiyat:** $300+/ay
- **Özellik:** 100M+ IP, datacenter+residential
- **Güvenilirlik:** ⭐⭐⭐⭐⭐
- **API:** RESTful API desteği

#### 3. **Smartproxy**
- **Website:** https://smartproxy.com/
- **Fiyat:** $75+/ay
- **Özellik:** 55M+ IP, 195+ lokasyon
- **Güvenilirlik:** ⭐⭐⭐⭐
- **Özel:** Rotating proxies

#### 4. **ProxyMesh**
- **Website:** https://proxymesh.com/
- **Fiyat:** $10+/ay
- **Özellik:** Düşük maliyetli, güvenilir
- **Güvenilirlik:** ⭐⭐⭐⭐
- **Özel:** API entegrasyonu

#### 5. **IPRoyal**
- **Website:** https://iproyal.com/
- **Fiyat:** $1.75/GB
- **Özellik:** Residential+datacenter
- **Güvenilirlik:** ⭐⭐⭐⭐
- **Özel:** Pay-as-you-go

### 💳 Bütçe Dostu Seçenekler

#### 1. **Proxy-Cheap**
- **Website:** https://proxy-cheap.com/
- **Fiyat:** $2.99+/ay
- **Özellik:** Düşük maliyetli
- **Güvenilirlik:** ⭐⭐⭐

#### 2. **ProxyRack**
- **Website:** https://www.proxyrack.com/
- **Fiyat:** $49+/ay
- **Özellik:** Unlimited bandwidth
- **Güvenilirlik:** ⭐⭐⭐

#### 3. **MyPrivateProxy**
- **Website:** https://www.myprivateproxy.net/
- **Fiyat:** $2.49+/proxy
- **Özellik:** Dedicated proxies
- **Güvenilirlik:** ⭐⭐⭐

---

## 🔍 Proxy Test ve Doğrulama Araçları

### 🧪 Online Test Araçları

#### 1. **ProxyChecker.co**
```
https://www.proxychecker.co/
- Toplu proxy testi
- Anonimlik seviyesi kontrolü
- Hız testi
```

#### 2. **WhatIsMyIPAddress**
```
https://whatismyipaddress.com/proxy-check
- IP leak kontrolü
- DNS leak testi
- WebRTC leak kontrolü
```

#### 3. **ProxyJudge**
```
http://proxyjudge.info/
- Anonimlik seviyesi
- Proxy türü tespiti
- Header bilgileri
```

### 🛠️ Python ile Proxy Testi

```python
import requests
import time

def test_proxy(proxy_url, test_url="http://httpbin.org/ip"):
    """Proxy'yi test eder"""
    try:
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        start_time = time.time()
        response = requests.get(test_url, proxies=proxies, timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            speed = end_time - start_time
            return True, speed, response.json()
        else:
            return False, None, None
            
    except Exception as e:
        return False, None, str(e)

# Kullanım örneği
proxy = "http://104.248.63.15:30588"
is_working, speed, ip_info = test_proxy(proxy)

if is_working:
    print(f"✅ Proxy çalışıyor! Hız: {speed:.2f}s")
    print(f"IP: {ip_info.get('origin', 'N/A')}")
else:
    print("❌ Proxy çalışmıyor!")
```

---

## 🔧 Proxy Türleri

### 📡 HTTP/HTTPS Proxies
```
✅ Avantajlar:
- Web trafiği için ideal
- Yaygın destek
- Kolay yapılandırma

❌ Dezavantajlar:
- Sadece HTTP/HTTPS
- Daha az güvenli
```

### 🚀 SOCKS5 Proxies
```
✅ Avantajlar:
- Tüm protokoller
- Daha hızlı
- UDP desteği

❌ Dezavantajlar:
- Daha karmaşık
- Daha pahalı
```

### 🏠 Residential Proxies
```
✅ Avantajlar:
- Gerçek IP adresleri
- Düşük tespit riski
- Yüksek başarı oranı

❌ Dezavantajlar:
- Pahalı
- Değişken hız
```

### 🏢 Datacenter Proxies
```
✅ Avantajlar:
- Hızlı
- Güvenilir
- Uygun fiyatlı

❌ Dezavantajlar:
- Kolay tespit
- Daha az gerçekçi
```

---

## 🛡️ Güvenlik Önerileri

### ⚠️ Güvenlik Kontrol Listesi

```
✅ Proxy sağlayıcısının güvenilirliğini araştırın
✅ HTTPS kullanan proxy'leri tercih edin
✅ Log politikasını kontrol edin
✅ DNS leak koruması sağlayın
✅ Düzenli olarak IP'nizi kontrol edin
✅ Kişisel bilgileri proxy üzerinden göndermeyin
✅ Ücretli servisleri ücretsizlere tercih edin
✅ Proxy rotasyonu kullanın
```

### 🚫 Güvenlik Riskleri

```
❌ Ücretsiz proxy'lerde log tutulabilir
❌ Kötü niyetli proxy'ler veri çalabilir
❌ DNS leak'ler gerçek IP'nizi açığa çıkarabilir
❌ HTTP proxy'ler şifrelenmemiş trafiği görür
❌ Yavaş proxy'ler performansı düşürür
```

---

## 🤖 Bot İçin Proxy Ayarlama

### 📝 .env Dosyasında Proxy Ayarı

```bash
# Tek proxy
PROXY=http://104.248.63.15:30588

# Authentication ile
PROXY=http://username:password@proxy.example.com:8080

# SOCKS5 proxy
PROXY=socks5://72.221.164.34:60671
```

### 🔄 Proxy Rotasyonu

```python
import random

class ProxyRotator:
    def __init__(self):
        self.proxies = [
            "http://104.248.63.15:30588",
            "http://178.62.201.21:80",
            "http://159.65.69.186:9300",
            "http://167.172.109.12:39533"
        ]
        self.current_index = 0
    
    def get_next_proxy(self):
        """Sonraki proxy'yi döndürür"""
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def get_random_proxy(self):
        """Rastgele proxy döndürür"""
        return random.choice(self.proxies)
```

### 🎯 Bot'ta Kullanım

```python
# google_review_bot.py içinde
def setup_driver(self):
    chrome_options = Options()
    
    # Proxy ayarı
    proxy = os.getenv('PROXY')
    if proxy:
        chrome_options.add_argument(f"--proxy-server={proxy}")
        logging.info(f"Proxy kullanılıyor: {proxy}")
    
    # Diğer ayarlar...
    return webdriver.Chrome(service=service, options=chrome_options)
```

---

## 📊 Proxy Performans Karşılaştırması

| Servis | Fiyat | Hız | Güvenilirlik | Anonimlik | Önerilen |
|--------|-------|-----|--------------|-----------|-----------|
| Bright Data | 💰💰💰💰💰 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Kurumsal |
| Oxylabs | 💰💰💰💰 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Profesyonel |
| Smartproxy | 💰💰💰 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Orta seviye |
| ProxyMesh | 💰💰 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Başlangıç |
| Ücretsiz | 💰 | ⭐⭐ | ⭐⭐ | ⭐⭐ | Test |

---

## 🔗 Yararlı Linkler

### 📚 Dokümantasyon
- [Selenium Proxy Ayarları](https://selenium-python.readthedocs.io/api.html)
- [Requests Proxy Kullanımı](https://docs.python-requests.org/en/latest/user/advanced/#proxies)
- [Chrome Proxy Arguments](https://peter.sh/experiments/chromium-command-line-switches/)

### 🛠️ Araçlar
- [Proxy Checker](https://www.proxychecker.co/)
- [IP Leak Test](https://ipleak.net/)
- [DNS Leak Test](https://www.dnsleaktest.com/)

### 📰 Güncel Listeler
- [Free Proxy List](https://free-proxy-list.net/)
- [ProxyList](https://proxylist.geonode.com/)
- [SSL Proxies](https://www.sslproxies.org/)

---

## ⚠️ Yasal Uyarı

```
Bu proxy listeleri sadece eğitim ve test amaçlıdır.
Proxy kullanımında aşağıdaki hususlara dikkat edin:

• Proxy sağlayıcısının hizmet şartlarını okuyun
• Hedef sitenin kullanım koşullarına uyun
• Yasal düzenlemelere saygı gösterin
• Kişisel verileri koruyun
• Ticari kullanımda lisans gereksinimlerini kontrol edin

Kullanım sorumluluğu tamamen kullanıcıya aittir.
```

---

**Son Güncelleme:** 2024
**Versiyon:** 1.0
**Lisans:** Eğitim amaçlı
