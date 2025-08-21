# 🔐 Hesap Yönetimi Kılavuzu

Bu kılavuz, Google Review Bot'un hesap yönetimi özelliklerini kullanmanız için hazırlanmıştır.

## 📋 İçindekiler

1. [Hesap Dosyası Formatları](#hesap-dosyası-formatları)
2. [Hesap Durumları](#hesap-durumları)
3. [Hesap Limitleri](#hesap-limitleri)
4. [Kullanım Örnekleri](#kullanım-örnekleri)
5. [Güvenlik Önerileri](#güvenlik-önerileri)

---

## 📄 Hesap Dosyası Formatları

### JSON Format (Önerilen)

`accounts.json` dosyası:

```json
{
  "accounts": [
    {
      "email": "hesap1@gmail.com",
      "password": "sifre123",
      "status": "active",
      "last_used": "",
      "review_count": 0,
      "notes": "Ana hesap"
    },
    {
      "email": "hesap2@gmail.com",
      "password": "sifre456",
      "status": "active",
      "last_used": "",
      "review_count": 0,
      "notes": "Yedek hesap"
    }
  ],
  "stats": {
    "total_accounts": 2,
    "active_accounts": 2,
    "total_reviews": 0
  }
}
```

### CSV Format

`accounts.csv` dosyası:

```csv
email,password,status,last_used,review_count,notes
hesap1@gmail.com,sifre123,active,,0,Ana hesap
hesap2@gmail.com,sifre456,active,,0,Yedek hesap
```

---

## 📊 Hesap Durumları

### ✅ Active (Aktif)
- Hesap kullanıma hazır
- Limitler aşılmamış
- Bekleme süresi tamamlanmış

### ⏳ Cooldown (Bekleme)
- Son kullanımdan sonra 24 saat geçmemiş
- Otomatik olarak aktif duruma geçer

### 🚫 Banned (Banlanmış)
- Google tarafından banlanmış
- Manuel olarak işaretlenir
- Kullanılamaz

### ❌ Error (Hata)
- Giriş hatası yaşanmış
- Şifre yanlış olabilir
- 2FA sorunu olabilir

---

## 🔒 Hesap Limitleri

### Varsayılan Limitler
- **Hesap başına maksimum değerlendirme**: 3
- **Bekleme süresi**: 24 saat
- **Günlük toplam değerlendirme**: Sınırsız (hesap sayısına bağlı)

### Limit Değiştirme

`account_manager.py` dosyasında:

```python
class AccountManager:
    def __init__(self, accounts_file="accounts.json"):
        # Bu değerleri değiştirin
        self.max_reviews_per_account = 5  # Hesap başına 5 değerlendirme
        self.cooldown_hours = 12  # 12 saat bekleme
```

---

## 💡 Kullanım Örnekleri

### 1. Basit Hesap Listesi Oluşturma

```python
from account_manager import AccountManager

# Hesap manager oluştur
am = AccountManager()

# Örnek hesap dosyası oluştur
am.create_sample_accounts_file()

# Hesapları yükle
am.load_accounts_from_json()

# Hesap durumunu göster
am.print_account_status()
```

### 2. Hesap Rotasyonu

```python
# Kullanılabilir hesap al
account = am.get_available_account()
if account:
    print(f"Seçilen hesap: {account['email']}")
    
    # Hesabı kullan
    # ... bot işlemleri ...
    
    # Başarılı kullanım işaretle
    am.mark_account_used(account['email'], True)
```

### 3. Hesap Durumu Yönetimi

```python
# Hesabı banla
am.mark_account_banned("banlanan@gmail.com")

# Hesabı sıfırla
am.reset_account_cooldown("sifirlanacak@gmail.com")

# İstatistikleri al
stats = am.get_account_stats()
print(f"Toplam hesap: {stats['total_accounts']}")
print(f"Kullanılabilir: {stats['available_accounts']}")
```

---

## 🛡️ Güvenlik Önerileri

### 🔐 Hesap Güvenliği

1. **Güçlü Şifreler Kullanın**
   - En az 12 karakter
   - Büyük/küçük harf, sayı, özel karakter
   - Her hesap için farklı şifre

2. **2FA Aktif Edin**
   - SMS veya Authenticator app
   - Hesap güvenliğini artırır

3. **Hesap Çeşitliliği**
   - Farklı IP'lerden oluşturulan hesaplar
   - Farklı tarihlerde açılan hesaplar
   - Farklı cihazlardan erişim geçmişi

### 📊 Kullanım Stratejisi

1. **Yavaş Başlangıç**
   - İlk gün sadece 1-2 değerlendirme
   - Hesapları test edin
   - Sorunları tespit edin

2. **Düzenli Rotasyon**
   - Her hesabı eşit kullanın
   - Limitleri aşmayın
   - Bekleme sürelerine uyun

3. **İzleme ve Takip**
   - Hesap durumlarını düzenli kontrol edin
   - Banlanan hesapları hemen işaretleyin
   - Yeni hesaplar ekleyin

### 🚫 Yasaklı İşlemler

- ❌ Aynı IP'den çok fazla hesap oluşturma
- ❌ Çok hızlı değerlendirme bırakma
- ❌ Aynı metni birden fazla hesaptan kullanma
- ❌ Şüpheli aktivite tespit edilen hesapları kullanmaya devam etme

---

## 🔧 Sorun Giderme

### Hesap Giriş Hatası

```python
# Hesabı hata durumuna getir
am.mark_account_used("hatali@gmail.com", False)

# Hesap durumunu kontrol et
for account in am.accounts:
    if account['email'] == "hatali@gmail.com":
        print(f"Durum: {account['status']}")
        print(f"Not: {account.get('notes', '')}")
```

### Kullanılabilir Hesap Bulunamadı

```python
# Tüm hesapları kontrol et
stats = am.get_account_stats()
print(f"Toplam: {stats['total_accounts']}")
print(f"Aktif: {stats['active_accounts']}")
print(f"Kullanılabilir: {stats['available_accounts']}")

# Bekleme sürelerini kontrol et
for account in am.accounts:
    if account['status'] == 'active':
        last_used = account.get('last_used', '')
        if last_used:
            print(f"{account['email']}: Son kullanım {last_used}")
```

### Hesap Sıfırlama

```python
# Tüm hesapları sıfırla
for account in am.accounts:
    am.reset_account_cooldown(account['email'])

print("✅ Tüm hesaplar sıfırlandı!")
```

---

## 📈 Performans İpuçları

### Optimal Hesap Sayısı
- **Küçük ölçek**: 5-10 hesap
- **Orta ölçek**: 10-25 hesap  
- **Büyük ölçek**: 25+ hesap

### Günlük Kullanım
- Hesap başına maksimum 3 değerlendirme
- 24 saat bekleme süresi
- Düzenli rotasyon

### Hesapları Yenileme
- Aylık %10-20 yeni hesap ekleme
- Banlanan hesapları değiştirme
- Eski hesapları dinlendirme

---

## ⚠️ Önemli Notlar

1. **Yasal Uyarı**: Bu sistem sadece eğitim amaçlıdır
2. **Hesap Güvenliği**: Gerçek hesaplarda dikkatli kullanın
3. **Limitlere Uyun**: Hesap banlanmasını önlemek için
4. **Düzenli Yedekleme**: Hesap dosyalarını yedekleyin
5. **İzleme**: Hesap durumlarını sürekli takip edin

---

**Son Güncelleme:** 2024  
**Versiyon:** 1.0  
**Lisans:** Eğitim amaçlı
