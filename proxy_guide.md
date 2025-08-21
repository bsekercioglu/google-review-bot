# 🌐 Proxy Yönetimi Kılavuzu

Bu kılavuz, Google Review Bot'un proxy yönetimi özelliklerini kullanmanız için hazırlanmıştır.

## 📋 İçindekiler

1. [Proxy Dosyası Formatı](#proxy-dosyası-formatı)
2. [Proxy Durumları](#proxy-durumları)
3. [Proxy Limitleri](#proxy-limitleri)
4. [Kullanım Örnekleri](#kullanım-örnekleri)
5. [Güvenlik Önerileri](#güvenlik-önerileri)

---

## 📄 Proxy Dosyası Formatı

### JSON Format (Önerilen)

`proxies.json` dosyası:

```json
{
  "proxies": [
    {
      "ip": "192.168.1.100",
      "port": "8080",
      "protocol": "http",
      "username": "",
      "password": "",
      "status": "active",
      "last_used": "",
      "request_count": 0,
      "response_time": 0,
      "country": "TR",
      "notes": "Ana proxy"
    },
    {
      "ip": "10.0.0.50",
      "port": "3128",
      "protocol": "https",
      "username": "user1",
      "password": "pass123",
      "status": "active",
      "last_used": "",
      "request_count": 0,
      "response_time": 0,
      "country": "TR",
      "notes": "Kimlik doğrulamalı proxy"
    }
  ],
  "stats": {
    "total_proxies": 2,
    "active_proxies": 2,
    "total_requests": 0
  }
}
```

---

## 📊 Proxy Durumları

### ✅ Active (Aktif)
- Proxy kullanıma hazır
- Limitler aşılmamış
- Bekleme süresi tamamlanmış

### ⏳ Cooldown (Bekleme)
- Son kullanımdan sonra 30 dakika geçmemiş
- Otomatik olarak aktif duruma geçer

### 💀 Dead (Çalışmıyor)
- Test sırasında hata alınmış
- Bağlantı kurulamıyor
- Kullanılamaz

### 🐌 Slow (Yavaş)
- Yanıt süresi çok uzun
- Performans düşük
- Manuel olarak işaretlenir

---

## 🔒 Proxy Limitleri

### Varsayılan Limitler
- **Proxy başına maksimum istek**: 50
- **Bekleme süresi**: 30 dakika
- **Test timeout**: 10 saniye

### Limit Değiştirme

`proxy_manager.py` dosyasında:

```python
class ProxyManager:
    def __init__(self, proxy_file="proxies.json"):
        # Bu değerleri değiştirin
        self.max_requests_per_proxy = 100  # Proxy başına 100 istek
        self.cooldown_minutes = 15  # 15 dakika bekleme
```

---

## 💡 Kullanım Örnekleri

### 1. Basit Proxy Listesi Oluşturma

```python
from proxy_manager import ProxyManager

# Proxy manager oluştur
pm = ProxyManager()

# Örnek proxy dosyası oluştur
pm.create_sample_proxies_file()

# Proxy'leri yükle
pm.load_proxies_from_json()

# Proxy durumunu göster
pm.print_proxy_status()
```

### 2. Proxy Rotasyonu

```python
# Kullanılabilir proxy al
proxy = pm.get_available_proxy()
if proxy:
    print(f"Seçilen proxy: {proxy['ip']}:{proxy['port']}")
    
    # Proxy'yi kullan
    # ... bot işlemleri ...
    
    # Başarılı kullanım işaretle
    pm.mark_proxy_used(proxy['ip'], proxy['port'], proxy['protocol'], True)
```

### 3. Proxy Durumu Yönetimi

```python
# Proxy'yi çalışmıyor olarak işaretle
pm.mark_proxy_dead("192.168.1.100", "8080", "http")

# Proxy'yi yavaş olarak işaretle
pm.mark_proxy_slow("10.0.0.50", "3128", "https")

# Proxy'yi sıfırla
pm.reset_proxy_cooldown("172.16.0.10", "8080", "http")

# İstatistikleri al
stats = pm.get_proxy_stats()
print(f"Toplam proxy: {stats['total_proxies']}")
print(f"Kullanılabilir: {stats['available_proxies']}")
```

### 4. Yeni Proxy Ekleme

```python
# Basit proxy ekle
pm.add_proxy("192.168.1.200", "9090", "http", "", "", "TR", "Yeni proxy")

# Kimlik doğrulamalı proxy ekle
pm.add_proxy("10.0.0.100", "8080", "https", "user", "pass", "TR", "Güvenli proxy")
```

---

## 🛡️ Güvenlik Önerileri

### 🔐 Proxy Güvenliği

1. **Güvenilir Proxy Servisleri Kullanın**
   - Ücretli proxy servisleri tercih edin
   - SSL/TLS destekli proxy'ler kullanın
   - Kimlik doğrulamalı proxy'ler tercih edin

2. **Proxy Çeşitliliği**
   - Farklı ülkelerden proxy'ler
   - Farklı protokoller (HTTP/HTTPS/SOCKS)
   - Farklı sağlayıcılardan proxy'ler

3. **Düzenli Test**
   - Proxy'leri düzenli olarak test edin
   - Çalışmayan proxy'leri hemen işaretleyin
   - Yeni proxy'ler ekleyin

### 📊 Kullanım Stratejisi

1. **Yavaş Başlangıç**
   - İlk gün sadece 1-2 proxy kullanın
   - Proxy'leri test edin
   - Sorunları tespit edin

2. **Düzenli Rotasyon**
   - Her proxy'yi eşit kullanın
   - Limitleri aşmayın
   - Bekleme sürelerine uyun

3. **İzleme ve Takip**
   - Proxy durumlarını düzenli kontrol edin
   - Çalışmayan proxy'leri hemen işaretleyin
   - Yeni proxy'ler ekleyin

### 🚫 Yasaklı İşlemler

- ❌ Ücretsiz proxy listelerini güvenilir kaynak olarak kullanma
- ❌ Çok hızlı proxy değiştirme
- ❌ Aynı proxy'yi çok fazla kullanma
- ❌ Çalışmayan proxy'leri kullanmaya devam etme

---

## 🔧 Sorun Giderme

### Proxy Test Hatası

```python
# Proxy'yi test et
pm.test_proxy(proxy)

# Tüm proxy'leri test et
pm.test_all_proxies()

# Proxy durumunu kontrol et
for proxy in pm.proxies:
    if proxy['ip'] == "192.168.1.100":
        print(f"Durum: {proxy['status']}")
        print(f"Not: {proxy.get('notes', '')}")
```

### Kullanılabilir Proxy Bulunamadı

```python
# Tüm proxy'leri kontrol et
stats = pm.get_proxy_stats()
print(f"Toplam: {stats['total_proxies']}")
print(f"Aktif: {stats['active_proxies']}")
print(f"Kullanılabilir: {stats['available_proxies']}")

# Bekleme sürelerini kontrol et
for proxy in pm.proxies:
    if proxy['status'] == 'active':
        last_used = proxy.get('last_used', '')
        if last_used:
            print(f"{proxy['ip']}:{proxy['port']}: Son kullanım {last_used}")
```

### Proxy Sıfırlama

```python
# Tüm proxy'leri sıfırla
for proxy in pm.proxies:
    pm.reset_proxy_cooldown(proxy['ip'], proxy['port'], proxy['protocol'])

print("✅ Tüm proxy'ler sıfırlandı!")
```

---

## 📈 Performans İpuçları

### Optimal Proxy Sayısı
- **Küçük ölçek**: 5-10 proxy
- **Orta ölçek**: 10-25 proxy  
- **Büyük ölçek**: 25+ proxy

### Günlük Kullanım
- Proxy başına maksimum 50 istek
- 30 dakika bekleme süresi
- Düzenli rotasyon

### Proxy'leri Yenileme
- Aylık %10-20 yeni proxy ekleme
- Çalışmayan proxy'leri değiştirme
- Eski proxy'leri dinlendirme

---

## 🌍 Proxy Türleri

### HTTP Proxy
```json
{
  "ip": "192.168.1.100",
  "port": "8080",
  "protocol": "http"
}
```

### HTTPS Proxy
```json
{
  "ip": "10.0.0.50",
  "port": "3128",
  "protocol": "https"
}
```

### Kimlik Doğrulamalı Proxy
```json
{
  "ip": "172.16.0.10",
  "port": "8080",
  "protocol": "http",
  "username": "user1",
  "password": "pass123"
}
```

### SOCKS Proxy
```json
{
  "ip": "192.168.1.200",
  "port": "1080",
  "protocol": "socks5"
}
```

---

## ⚠️ Önemli Notlar

1. **Yasal Uyarı**: Bu sistem sadece eğitim amaçlıdır
2. **Proxy Güvenliği**: Güvenilir proxy servisleri kullanın
3. **Limitlere Uyun**: Proxy banlanmasını önlemek için
4. **Düzenli Yedekleme**: Proxy dosyalarını yedekleyin
5. **İzleme**: Proxy durumlarını sürekli takip edin

---

## 🔗 Faydalı Kaynaklar

### Ücretsiz Proxy Listeleri
- https://free-proxy-list.net/
- https://www.proxynova.com/
- https://www.proxy-list.download/

### Ücretli Proxy Servisleri
- **Bright Data** (eski Luminati)
- **Oxylabs**
- **SmartProxy**
- **ProxyMesh**

### Proxy Test Araçları
- **Proxy Checker**: https://www.proxy-checker.org/
- **IP Checker**: https://whatismyipaddress.com/
- **Speed Test**: https://www.speedtest.net/

---

**Son Güncelleme:** 2024  
**Versiyon:** 1.0  
**Lisans:** Eğitim amaçlı
