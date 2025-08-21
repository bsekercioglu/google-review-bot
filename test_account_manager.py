#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hesap Yönetimi Test Dosyası
AccountManager sınıfının test edilmesi için
"""

import os
import logging
from account_manager import AccountManager, create_sample_csv

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_account_manager():
    """AccountManager'ı test eder"""
    print("🧪 Hesap Yönetimi Testi")
    print("=" * 50)
    
    # AccountManager oluştur
    am = AccountManager()
    
    # Örnek dosyaları oluştur
    print("\n📁 Örnek dosyalar oluşturuluyor...")
    
    if not os.path.exists("accounts.json"):
        am.create_sample_accounts_file()
        print("✅ accounts.json oluşturuldu")
    
    if not os.path.exists("accounts.csv"):
        create_sample_csv()
        print("✅ accounts.csv oluşturuldu")
    
    # JSON dosyasından hesapları yükle
    print("\n📥 JSON dosyasından hesaplar yükleniyor...")
    if am.load_accounts_from_json():
        print(f"✅ {len(am.accounts)} hesap yüklendi")
        
        # Hesap durumunu göster
        am.print_account_status()
        
        # Hesap rotasyon testi
        print("\n🔄 Hesap Rotasyon Testi:")
        for i in range(5):
            account = am.get_available_account()
            if account:
                print(f"{i+1}. Seçilen: {account['email']}")
                
                # Hesabı kullanıldı olarak işaretle
                am.mark_account_used(account['email'], True)
            else:
                print(f"{i+1}. Kullanılabilir hesap bulunamadı!")
                break
        
        # Güncel durumu göster
        print("\n📊 Güncel Hesap Durumu:")
        am.print_account_status()
        
    else:
        print("❌ JSON dosyası yüklenemedi!")
    
    # CSV dosyasından yükleme testi
    print("\n📥 CSV dosyasından yükleme testi...")
    am_csv = AccountManager("accounts_csv.json")
    if am_csv.load_accounts_from_csv("accounts.csv"):
        print(f"✅ CSV'den {len(am_csv.accounts)} hesap yüklendi")
        am_csv.print_account_status()
    else:
        print("❌ CSV dosyası yüklenemedi!")

def test_account_limits():
    """Hesap limitlerini test eder"""
    print("\n🔒 Hesap Limitleri Testi")
    print("=" * 30)
    
    am = AccountManager()
    am.load_accounts_from_json()
    
    # Limitleri düşür (test için)
    am.max_reviews_per_account = 2
    am.cooldown_hours = 0  # Test için bekleme süresini kaldır
    
    print(f"📊 Hesap başına maksimum değerlendirme: {am.max_reviews_per_account}")
    
    # Hesapları kullan
    for i in range(10):
        account = am.get_available_account()
        if account:
            print(f"{i+1}. {account['email']} kullanıldı")
            am.mark_account_used(account['email'], True)
        else:
            print(f"{i+1}. Kullanılabilir hesap kalmadı!")
            break
    
    am.print_account_status()

def test_account_status():
    """Hesap durumlarını test eder"""
    print("\n📊 Hesap Durumları Testi")
    print("=" * 30)
    
    am = AccountManager()
    am.load_accounts_from_json()
    
    # İstatistikleri göster
    stats = am.get_account_stats()
    print("📈 İstatistikler:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Hesap durumlarını değiştir
    if am.accounts:
        # İlk hesabı banla
        am.mark_account_banned(am.accounts[0]['email'])
        print(f"\n🚫 {am.accounts[0]['email']} banlandı")
        
        # İkinci hesabı hata durumuna getir
        if len(am.accounts) > 1:
            am.mark_account_used(am.accounts[1]['email'], False)
            print(f"❌ {am.accounts[1]['email']} hata durumuna getirildi")
        
        # Güncel durumu göster
        am.print_account_status()

if __name__ == "__main__":
    # Ana test
    test_account_manager()
    
    # Limit testi
    test_account_limits()
    
    # Durum testi
    test_account_status()
    
    print("\n✅ Tüm testler tamamlandı!")
