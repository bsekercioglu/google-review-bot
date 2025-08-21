#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proxy Yönetim Modülü
Google Review Bot için proxy rotasyonu ve yönetimi
"""

import requests
import random
import logging
import json
import os
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

class ProxyManager:
    """Proxy yönetimi ve rotasyonu için sınıf"""
    
    def __init__(self, proxy_file="proxies.json"):
        """Proxy manager başlatıcı"""
        self.proxy_file = proxy_file
        self.proxies = []
        self.working_proxies = []
        self.current_index = 0
        self.proxy_stats = {}
        
        # Proxy kullanım limitleri
        self.max_requests_per_proxy = 50  # Proxy başına maksimum istek
        self.cooldown_minutes = 30  # Proxy kullanımı arası bekleme süresi (dakika)
        
        # Proxy durumları
        self.proxy_status = {
            'active': 'active',      # Aktif
            'cooldown': 'cooldown',  # Bekleme süresinde
            'dead': 'dead',          # Çalışmıyor
            'slow': 'slow'           # Yavaş
        }
    
    def load_proxies_from_json(self) -> bool:
        """JSON dosyasından proxy bilgilerini yükler"""
        try:
            if not os.path.exists(self.proxy_file):
                logging.warning(f"📁 {self.proxy_file} dosyası bulunamadı!")
                return False
            
            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.proxies = data.get('proxies', [])
            
            # Proxy istatistiklerini yükle
            self.proxy_stats = data.get('stats', {})
            
            logging.info(f"✅ {len(self.proxies)} proxy yüklendi")
            return True
            
        except Exception as e:
            logging.error(f"JSON proxy yükleme hatası: {e}")
            return False
    
    def save_proxies_to_json(self) -> bool:
        """Proxy bilgilerini JSON dosyasına kaydeder"""
        try:
            data = {
                'proxies': self.proxies,
                'stats': self.proxy_stats,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.proxy_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"✅ Proxy bilgileri {self.proxy_file} dosyasına kaydedildi")
            return True
            
        except Exception as e:
            logging.error(f"JSON proxy kaydetme hatası: {e}")
            return False
    
    def create_sample_proxies_file(self):
        """Örnek proxy dosyası oluşturur"""
        sample_proxies = {
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
                    "notes": "Örnek proxy 1"
                },
                {
                    "ip": "10.0.0.50",
                    "port": "3128",
                    "protocol": "http",
                    "username": "",
                    "password": "",
                    "status": "active",
                    "last_used": "",
                    "request_count": 0,
                    "response_time": 0,
                    "country": "TR",
                    "notes": "Örnek proxy 2"
                }
            ],
            "stats": {
                "total_proxies": 2,
                "active_proxies": 2,
                "total_requests": 0
            }
        }
        
        try:
            with open(self.proxy_file, 'w', encoding='utf-8') as f:
                json.dump(sample_proxies, f, indent=2, ensure_ascii=False)
            
            logging.info(f"✅ Örnek proxy dosyası oluşturuldu: {self.proxy_file}")
            return True
            
        except Exception as e:
            logging.error(f"Örnek dosya oluşturma hatası: {e}")
            return False
    
    def add_proxy(self, ip: str, port: str, protocol: str = "http", username: str = "", password: str = "", country: str = "TR", notes: str = ""):
        """Yeni proxy ekler"""
        proxy = {
            "ip": ip.strip(),
            "port": port.strip(),
            "protocol": protocol.lower(),
            "username": username.strip(),
            "password": password.strip(),
            "status": "active",
            "last_used": "",
            "request_count": 0,
            "response_time": 0,
            "country": country.upper(),
            "notes": notes
        }
        
        # Aynı proxy var mı kontrol et
        for existing_proxy in self.proxies:
            if (existing_proxy['ip'] == proxy['ip'] and 
                existing_proxy['port'] == proxy['port'] and 
                existing_proxy['protocol'] == proxy['protocol']):
                logging.warning(f"⚠️ Proxy zaten mevcut: {ip}:{port}")
                return False
        
        self.proxies.append(proxy)
        logging.info(f"✅ Proxy eklendi: {ip}:{port}")
        
        # Dosyaya kaydet
        self.save_proxies_to_json()
        return True
    
    def remove_proxy(self, ip: str, port: str, protocol: str = "http"):
        """Proxy'yi kaldırır"""
        for i, proxy in enumerate(self.proxies):
            if (proxy['ip'] == ip and 
                proxy['port'] == port and 
                proxy['protocol'] == protocol):
                removed_proxy = self.proxies.pop(i)
                logging.info(f"🗑️ Proxy kaldırıldı: {ip}:{port}")
                
                # Dosyaya kaydet
                self.save_proxies_to_json()
                return True
        
        logging.warning(f"⚠️ Proxy bulunamadı: {ip}:{port}")
        return False
    
    def get_available_proxy(self) -> Optional[Dict]:
        """Kullanılabilir bir proxy döndürür"""
        available_proxies = []
        
        for proxy in self.proxies:
            if proxy['status'] == 'active':
                # Son kullanım zamanını kontrol et
                last_used = proxy.get('last_used', '')
                if last_used:
                    try:
                        last_used_time = datetime.fromisoformat(last_used)
                        cooldown_end = last_used_time + timedelta(minutes=self.cooldown_minutes)
                        
                        if datetime.now() < cooldown_end:
                            continue  # Bekleme süresinde
                    except:
                        pass
                
                # Günlük limit kontrolü
                if proxy.get('request_count', 0) < self.max_requests_per_proxy:
                    available_proxies.append(proxy)
        
        if not available_proxies:
            logging.warning("⚠️ Kullanılabilir proxy bulunamadı!")
            return None
        
        # Rastgele bir proxy seç
        selected_proxy = random.choice(available_proxies)
        logging.info(f"✅ Proxy seçildi: {selected_proxy['ip']}:{selected_proxy['port']}")
        
        return selected_proxy
    
    def get_next_proxy(self) -> Optional[Dict]:
        """Sıradaki proxy'yi döndürür (round-robin)"""
        available_proxies = []
        
        for proxy in self.proxies:
            if proxy['status'] == 'active':
                # Son kullanım zamanını kontrol et
                last_used = proxy.get('last_used', '')
                if last_used:
                    try:
                        last_used_time = datetime.fromisoformat(last_used)
                        cooldown_end = last_used_time + timedelta(minutes=self.cooldown_minutes)
                        
                        if datetime.now() < cooldown_end:
                            continue  # Bekleme süresinde
                    except:
                        pass
                
                # Günlük limit kontrolü
                if proxy.get('request_count', 0) < self.max_requests_per_proxy:
                    available_proxies.append(proxy)
        
        if not available_proxies:
            logging.warning("⚠️ Kullanılabilir proxy bulunamadı!")
            return None
        
        # Sıradaki proxy'yi seç
        selected_proxy = available_proxies[self.current_index % len(available_proxies)]
        self.current_index += 1
        
        logging.info(f"✅ Sıradaki proxy seçildi: {selected_proxy['ip']}:{selected_proxy['port']}")
        return selected_proxy
    
    def mark_proxy_used(self, ip: str, port: str, protocol: str = "http", success: bool = True, response_time: float = 0):
        """Proxy'nin kullanıldığını işaretler"""
        for proxy in self.proxies:
            if (proxy['ip'] == ip and 
                proxy['port'] == port and 
                proxy['protocol'] == protocol):
                
                proxy['last_used'] = datetime.now().isoformat()
                
                if success:
                    proxy['request_count'] = proxy.get('request_count', 0) + 1
                    if response_time > 0:
                        proxy['response_time'] = response_time
                    logging.info(f"✅ Proxy kullanıldı: {ip}:{port} (Toplam: {proxy['request_count']})")
                else:
                    proxy['status'] = 'dead'
                    logging.warning(f"❌ Proxy hatası: {ip}:{port}")
                
                # Proxy bilgilerini kaydet
                self.save_proxies_to_json()
                break
    
    def mark_proxy_dead(self, ip: str, port: str, protocol: str = "http"):
        """Proxy'yi çalışmıyor olarak işaretler"""
        for proxy in self.proxies:
            if (proxy['ip'] == ip and 
                proxy['port'] == port and 
                proxy['protocol'] == protocol):
                
                proxy['status'] = 'dead'
                proxy['notes'] = f"Çalışmıyor: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                logging.warning(f"💀 Proxy çalışmıyor: {ip}:{port}")
                
                # Proxy bilgilerini kaydet
                self.save_proxies_to_json()
                break
    
    def mark_proxy_slow(self, ip: str, port: str, protocol: str = "http"):
        """Proxy'yi yavaş olarak işaretler"""
        for proxy in self.proxies:
            if (proxy['ip'] == ip and 
                proxy['port'] == port and 
                proxy['protocol'] == protocol):
                
                proxy['status'] = 'slow'
                proxy['notes'] = f"Yavaş: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                logging.warning(f"🐌 Proxy yavaş: {ip}:{port}")
                
                # Proxy bilgilerini kaydet
                self.save_proxies_to_json()
                break
    
    def reset_proxy_cooldown(self, ip: str, port: str, protocol: str = "http"):
        """Proxy'nin bekleme süresini sıfırlar"""
        for proxy in self.proxies:
            if (proxy['ip'] == ip and 
                proxy['port'] == port and 
                proxy['protocol'] == protocol):
                
                proxy['last_used'] = ""
                proxy['request_count'] = 0
                proxy['status'] = 'active'
                logging.info(f"🔄 Proxy sıfırlandı: {ip}:{port}")
                
                # Proxy bilgilerini kaydet
                self.save_proxies_to_json()
                break
    
    def test_proxy(self, proxy: Dict) -> bool:
        """Tek bir proxy'yi test eder"""
        try:
            # Proxy URL'sini oluştur
            if proxy.get('username') and proxy.get('password'):
                proxy_url = f"{proxy['protocol']}://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
            else:
                proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
            
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Test isteği gönder
            start_time = time.time()
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                logging.info(f"✅ Proxy çalışıyor: {proxy['ip']}:{proxy['port']} ({response_time:.2f}s)")
                
                # Başarılı kullanım işaretle
                self.mark_proxy_used(proxy['ip'], proxy['port'], proxy['protocol'], True, response_time)
                return True
            else:
                logging.warning(f"❌ Proxy test başarısız: {proxy['ip']}:{proxy['port']}")
                self.mark_proxy_dead(proxy['ip'], proxy['port'], proxy['protocol'])
                return False
                
        except Exception as e:
            logging.error(f"❌ Proxy test hatası {proxy['ip']}:{proxy['port']} - {e}")
            self.mark_proxy_dead(proxy['ip'], proxy['port'], proxy['protocol'])
            return False
    
    def test_all_proxies(self, max_workers: int = 5):
        """Tüm proxy'leri test eder"""
        logging.info("🧪 Tüm proxy'ler test ediliyor...")
        
        # Çalışan proxy'leri temizle
        self.working_proxies = []
        
        # Thread pool ile paralel test
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {
                executor.submit(self.test_proxy, proxy): proxy 
                for proxy in self.proxies if proxy['status'] == 'active'
            }
            
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    if future.result():
                        self.working_proxies.append(proxy)
                except Exception as e:
                    logging.error(f"Proxy test exception: {e}")
        
        logging.info(f"✅ {len(self.working_proxies)}/{len(self.proxies)} proxy çalışıyor")
        return len(self.working_proxies) > 0
    
    def get_proxy_stats(self) -> Dict:
        """Proxy istatistiklerini döndürür"""
        stats = {
            'total_proxies': len(self.proxies),
            'active_proxies': 0,
            'cooldown_proxies': 0,
            'dead_proxies': 0,
            'slow_proxies': 0,
            'total_requests': 0,
            'available_proxies': 0
        }
        
        for proxy in self.proxies:
            status = proxy.get('status', 'active')
            stats[f'{status}_proxies'] += 1
            stats['total_requests'] += proxy.get('request_count', 0)
            
            # Kullanılabilir proxy sayısı
            if status == 'active':
                last_used = proxy.get('last_used', '')
                if last_used:
                    try:
                        last_used_time = datetime.fromisoformat(last_used)
                        cooldown_end = last_used_time + timedelta(minutes=self.cooldown_minutes)
                        
                        if datetime.now() >= cooldown_end and proxy.get('request_count', 0) < self.max_requests_per_proxy:
                            stats['available_proxies'] += 1
                    except:
                        stats['available_proxies'] += 1
                else:
                    stats['available_proxies'] += 1
        
        return stats
    
    def print_proxy_status(self):
        """Proxy durumlarını yazdırır"""
        stats = self.get_proxy_stats()
        
        print("\n🌐 PROXY DURUMU:")
        print("=" * 40)
        print(f"🌍 Toplam Proxy: {stats['total_proxies']}")
        print(f"✅ Aktif: {stats['active_proxies']}")
        print(f"⏳ Bekleme: {stats['cooldown_proxies']}")
        print(f"💀 Çalışmıyor: {stats['dead_proxies']}")
        print(f"🐌 Yavaş: {stats['slow_proxies']}")
        print(f"🎯 Kullanılabilir: {stats['available_proxies']}")
        print(f"📊 Toplam İstek: {stats['total_requests']}")
        print("=" * 40)
        
        # Detaylı proxy listesi
        print("\n📋 PROXY LİSTESİ:")
        for i, proxy in enumerate(self.proxies, 1):
            status_emoji = {
                'active': '✅',
                'cooldown': '⏳', 
                'dead': '💀',
                'slow': '🐌'
            }
            
            status = proxy.get('status', 'active')
            emoji = status_emoji.get(status, '❓')
            
            print(f"{i}. {emoji} {proxy['ip']}:{proxy['port']} ({proxy['protocol']}) - İstek: {proxy.get('request_count', 0)}")
            
            if proxy.get('notes'):
                print(f"   📝 Not: {proxy['notes']}")
    
    def get_random_proxy(self) -> Optional[str]:
        """Rastgele çalışan proxy URL'si döndürür"""
        if not self.working_proxies:
            # Çalışan proxy yoksa test et
            if not self.test_all_proxies():
                return None
        
        if self.working_proxies:
            proxy = random.choice(self.working_proxies)
            
            # Proxy URL'sini oluştur
            if proxy.get('username') and proxy.get('password'):
                proxy_url = f"{proxy['protocol']}://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
            else:
                proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
            
            return proxy_url
        
        return None
    
    def initialize_proxies(self) -> bool:
        """Proxy'leri başlatır ve test eder"""
        # JSON dosyasından yükle
        if not self.load_proxies_from_json():
            # Dosya yoksa örnek oluştur
            self.create_sample_proxies_file()
            self.load_proxies_from_json()
        
        # Proxy'leri test et
        return self.test_all_proxies()

def create_sample_proxies_file():
    """Örnek proxy dosyası oluşturur"""
    sample_proxies = {
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
                "notes": "Örnek proxy 1"
            },
            {
                "ip": "10.0.0.50",
                "port": "3128",
                "protocol": "http",
                "username": "",
                "password": "",
                "status": "active",
                "last_used": "",
                "request_count": 0,
                "response_time": 0,
                "country": "TR",
                "notes": "Örnek proxy 2"
            }
        ],
        "stats": {
            "total_proxies": 2,
            "active_proxies": 2,
            "total_requests": 0
        }
    }
    
    try:
        with open('proxies.json', 'w', encoding='utf-8') as f:
            json.dump(sample_proxies, f, indent=2, ensure_ascii=False)
        
        logging.info("✅ Örnek proxy dosyası oluşturuldu: proxies.json")
        return True
        
    except Exception as e:
        logging.error(f"Proxy dosyası oluşturma hatası: {e}")
        return False

def test_proxy_manager():
    """Proxy manager'ı test eder"""
    print("🧪 Proxy Manager Testi")
    print("=" * 40)
    
    # Proxy manager oluştur
    pm = ProxyManager()
    
    # Örnek dosya oluştur
    if not os.path.exists(pm.proxy_file):
        pm.create_sample_proxies_file()
    
    # Proxy'leri yükle
    if pm.load_proxies_from_json():
        print(f"✅ {len(pm.proxies)} proxy yüklendi")
        
        # İstatistikleri göster
        pm.print_proxy_status()
        
        # Kullanılabilir proxy al
        proxy = pm.get_available_proxy()
        if proxy:
            print(f"\n🎯 Seçilen proxy: {proxy['ip']}:{proxy['port']}")
            
            # Proxy'yi kullanıldı olarak işaretle
            pm.mark_proxy_used(proxy['ip'], proxy['port'], proxy['protocol'], True)
            
            # Güncel durumu göster
            pm.print_proxy_status()
        else:
            print("❌ Kullanılabilir proxy bulunamadı!")
    else:
        print("❌ Proxy yükleme başarısız!")

if __name__ == "__main__":
    # Test çalıştır
    test_proxy_manager()
