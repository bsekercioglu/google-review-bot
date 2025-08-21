#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proxy Yönetimi Test Dosyası
ProxyManager sınıfının test edilmesi için
"""

import os
import logging
from proxy_manager import ProxyManager, create_sample_proxies_file

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_proxy_manager():
    """ProxyManager'ı test eder"""
    print("🧪 Proxy Yönetimi Testi")
    print("=" * 50)
    
    # ProxyManager oluştur
    pm = ProxyManager()
    
    # Örnek dosyaları oluştur
    print("\n📁 Örnek dosyalar oluşturuluyor...")
    
    if not os.path.exists("proxies.json"):
        pm.create_sample_proxies_file()
        print("✅ proxies.json oluşturuldu")
    
    # JSON dosyasından proxy'leri yükle
    print("\n📥 JSON dosyasından proxy'ler yükleniyor...")
    if pm.load_proxies_from_json():
        print(f"✅ {len(pm.proxies)} proxy yüklendi")
        
        # Proxy durumunu göster
        pm.print_proxy_status()
        
        # Proxy rotasyon testi
        print("\n🔄 Proxy Rotasyon Testi:")
        for i in range(5):
            proxy = pm.get_available_proxy()
            if proxy:
                print(f"{i+1}. Seçilen: {proxy['ip']}:{proxy['port']}")
                
                # Proxy'yi kullanıldı olarak işaretle
                pm.mark_proxy_used(proxy['ip'], proxy['port'], proxy['protocol'], True)
            else:
                print(f"{i+1}. Kullanılabilir proxy bulunamadı!")
                break
        
        # Güncel durumu göster
        print("\n📊 Güncel Proxy Durumu:")
        pm.print_proxy_status()
        
    else:
        print("❌ JSON dosyası yüklenemedi!")

def test_proxy_limits():
    """Proxy limitlerini test eder"""
    print("\n🔒 Proxy Limitleri Testi")
    print("=" * 30)
    
    pm = ProxyManager()
    pm.load_proxies_from_json()
    
    # Limitleri düşür (test için)
    pm.max_requests_per_proxy = 2
    pm.cooldown_minutes = 0  # Test için bekleme süresini kaldır
    
    print(f"📊 Proxy başına maksimum istek: {pm.max_requests_per_proxy}")
    
    # Proxy'leri kullan
    for i in range(10):
        proxy = pm.get_available_proxy()
        if proxy:
            print(f"{i+1}. {proxy['ip']}:{proxy['port']} kullanıldı")
            pm.mark_proxy_used(proxy['ip'], proxy['port'], proxy['protocol'], True)
        else:
            print(f"{i+1}. Kullanılabilir proxy kalmadı!")
            break
    
    pm.print_proxy_status()

def test_proxy_status():
    """Proxy durumlarını test eder"""
    print("\n📊 Proxy Durumları Testi")
    print("=" * 30)
    
    pm = ProxyManager()
    pm.load_proxies_from_json()
    
    # İstatistikleri göster
    stats = pm.get_proxy_stats()
    print("📈 İstatistikler:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Proxy durumlarını değiştir
    if pm.proxies:
        # İlk proxy'yi çalışmıyor olarak işaretle
        pm.mark_proxy_dead(pm.proxies[0]['ip'], pm.proxies[0]['port'], pm.proxies[0]['protocol'])
        print(f"\n💀 {pm.proxies[0]['ip']}:{pm.proxies[0]['port']} çalışmıyor olarak işaretlendi")
        
        # İkinci proxy'yi yavaş olarak işaretle
        if len(pm.proxies) > 1:
            pm.mark_proxy_slow(pm.proxies[1]['ip'], pm.proxies[1]['port'], pm.proxies[1]['protocol'])
            print(f"🐌 {pm.proxies[1]['ip']}:{pm.proxies[1]['port']} yavaş olarak işaretlendi")
        
        # Güncel durumu göster
        pm.print_proxy_status()

def test_proxy_operations():
    """Proxy işlemlerini test eder"""
    print("\n🔧 Proxy İşlemleri Testi")
    print("=" * 30)
    
    pm = ProxyManager()
    pm.load_proxies_from_json()
    
    # Yeni proxy ekle
    print("\n➕ Yeni proxy ekleniyor...")
    pm.add_proxy("192.168.1.200", "9090", "http", "", "", "TR", "Test proxy")
    
    # Proxy kaldır
    if pm.proxies:
        proxy_to_remove = pm.proxies[-1]
        print(f"\n🗑️ Proxy kaldırılıyor: {proxy_to_remove['ip']}:{proxy_to_remove['port']}")
        pm.remove_proxy(proxy_to_remove['ip'], proxy_to_remove['port'], proxy_to_remove['protocol'])
    
    # Proxy sıfırla
    if pm.proxies:
        proxy_to_reset = pm.proxies[0]
        print(f"\n🔄 Proxy sıfırlanıyor: {proxy_to_reset['ip']}:{proxy_to_reset['port']}")
        pm.reset_proxy_cooldown(proxy_to_reset['ip'], proxy_to_reset['port'], proxy_to_reset['protocol'])
    
    # Güncel durumu göster
    pm.print_proxy_status()

def test_proxy_url_generation():
    """Proxy URL oluşturma testi"""
    print("\n🔗 Proxy URL Oluşturma Testi")
    print("=" * 35)
    
    pm = ProxyManager()
    pm.load_proxies_from_json()
    
    for proxy in pm.proxies:
        # Proxy URL'sini oluştur
        if proxy.get('username') and proxy.get('password'):
            proxy_url = f"{proxy['protocol']}://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
        else:
            proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
        
        print(f"📋 {proxy['ip']}:{proxy['port']} -> {proxy_url}")
    
    # Rastgele proxy URL al
    random_url = pm.get_random_proxy()
    if random_url:
        print(f"\n🎯 Rastgele proxy URL: {random_url}")
    else:
        print("\n❌ Rastgele proxy URL alınamadı!")

if __name__ == "__main__":
    # Ana test
    test_proxy_manager()
    
    # Limit testi
    test_proxy_limits()
    
    # Durum testi
    test_proxy_status()
    
    # İşlem testi
    test_proxy_operations()
    
    # URL testi
    test_proxy_url_generation()
    
    print("\n✅ Tüm testler tamamlandı!")
