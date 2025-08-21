#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail Hesap Yönetim Modülü
Google Review Bot için hesap rotasyonu ve yönetimi
"""

import json
import csv
import random
import logging
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

class AccountManager:
    """Gmail hesap yönetimi ve rotasyonu için sınıf"""
    
    def __init__(self, accounts_file="accounts.json"):
        """Hesap manager başlatıcı"""
        self.accounts_file = accounts_file
        self.accounts = []
        self.used_accounts = []
        self.current_index = 0
        self.account_stats = {}
        
        # Hesap kullanım limitleri
        self.max_reviews_per_account = 3  # Hesap başına maksimum değerlendirme
        self.cooldown_hours = 24  # Hesap kullanımı arası bekleme süresi (saat)
        
        # Hesap durumları
        self.account_status = {
            'active': 'active',      # Aktif
            'cooldown': 'cooldown',  # Bekleme süresinde
            'banned': 'banned',      # Banlanmış
            'error': 'error'         # Hata durumu
        }
    
    def load_accounts_from_json(self) -> bool:
        """JSON dosyasından hesap bilgilerini yükler"""
        try:
            if not os.path.exists(self.accounts_file):
                logging.warning(f"📁 {self.accounts_file} dosyası bulunamadı!")
                return False
            
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.accounts = data.get('accounts', [])
            
            # Hesap istatistiklerini yükle
            self.account_stats = data.get('stats', {})
            
            logging.info(f"✅ {len(self.accounts)} hesap yüklendi")
            return True
            
        except Exception as e:
            logging.error(f"JSON hesap yükleme hatası: {e}")
            return False
    
    def load_accounts_from_csv(self, csv_file="accounts.csv") -> bool:
        """CSV dosyasından hesap bilgilerini yükler"""
        try:
            if not os.path.exists(csv_file):
                logging.warning(f"📁 {csv_file} dosyası bulunamadı!")
                return False
            
            self.accounts = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    account = {
                        'email': row.get('email', '').strip(),
                        'password': row.get('password', '').strip(),
                        'status': row.get('status', 'active'),
                        'last_used': row.get('last_used', ''),
                        'review_count': int(row.get('review_count', 0)),
                        'notes': row.get('notes', '')
                    }
                    if account['email'] and account['password']:
                        self.accounts.append(account)
            
            logging.info(f"✅ {len(self.accounts)} hesap CSV'den yüklendi")
            return True
            
        except Exception as e:
            logging.error(f"CSV hesap yükleme hatası: {e}")
            return False
    
    def save_accounts_to_json(self) -> bool:
        """Hesap bilgilerini JSON dosyasına kaydeder"""
        try:
            data = {
                'accounts': self.accounts,
                'stats': self.account_stats,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"✅ Hesap bilgileri {self.accounts_file} dosyasına kaydedildi")
            return True
            
        except Exception as e:
            logging.error(f"JSON hesap kaydetme hatası: {e}")
            return False
    
    def create_sample_accounts_file(self):
        """Örnek hesap dosyası oluşturur"""
        sample_accounts = {
            "accounts": [
                {
                    "email": "ornek1@gmail.com",
                    "password": "sifre123",
                    "status": "active",
                    "last_used": "",
                    "review_count": 0,
                    "notes": "Örnek hesap 1"
                },
                {
                    "email": "ornek2@gmail.com", 
                    "password": "sifre456",
                    "status": "active",
                    "last_used": "",
                    "review_count": 0,
                    "notes": "Örnek hesap 2"
                }
            ],
            "stats": {
                "total_accounts": 2,
                "active_accounts": 2,
                "total_reviews": 0
            }
        }
        
        try:
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(sample_accounts, f, indent=2, ensure_ascii=False)
            
            logging.info(f"✅ Örnek hesap dosyası oluşturuldu: {self.accounts_file}")
            return True
            
        except Exception as e:
            logging.error(f"Örnek dosya oluşturma hatası: {e}")
            return False
    
    def get_available_account(self) -> Optional[Dict]:
        """Kullanılabilir bir hesap döndürür"""
        available_accounts = []
        
        for account in self.accounts:
            if account['status'] == 'active':
                # Son kullanım zamanını kontrol et
                last_used = account.get('last_used', '')
                if last_used:
                    try:
                        last_used_time = datetime.fromisoformat(last_used)
                        cooldown_end = last_used_time + timedelta(hours=self.cooldown_hours)
                        
                        if datetime.now() < cooldown_end:
                            continue  # Bekleme süresinde
                    except:
                        pass
                
                # Günlük limit kontrolü
                if account.get('review_count', 0) < self.max_reviews_per_account:
                    available_accounts.append(account)
        
        if not available_accounts:
            logging.warning("⚠️ Kullanılabilir hesap bulunamadı!")
            return None
        
        # Rastgele bir hesap seç
        selected_account = random.choice(available_accounts)
        logging.info(f"✅ Hesap seçildi: {selected_account['email']}")
        
        return selected_account
    
    def get_next_account(self) -> Optional[Dict]:
        """Sıradaki hesabı döndürür (round-robin)"""
        available_accounts = []
        
        for account in self.accounts:
            if account['status'] == 'active':
                # Son kullanım zamanını kontrol et
                last_used = account.get('last_used', '')
                if last_used:
                    try:
                        last_used_time = datetime.fromisoformat(last_used)
                        cooldown_end = last_used_time + timedelta(hours=self.cooldown_hours)
                        
                        if datetime.now() < cooldown_end:
                            continue  # Bekleme süresinde
                    except:
                        pass
                
                # Günlük limit kontrolü
                if account.get('review_count', 0) < self.max_reviews_per_account:
                    available_accounts.append(account)
        
        if not available_accounts:
            logging.warning("⚠️ Kullanılabilir hesap bulunamadı!")
            return None
        
        # Sıradaki hesabı seç
        selected_account = available_accounts[self.current_index % len(available_accounts)]
        self.current_index += 1
        
        logging.info(f"✅ Sıradaki hesap seçildi: {selected_account['email']}")
        return selected_account
    
    def mark_account_used(self, email: str, success: bool = True):
        """Hesabın kullanıldığını işaretler"""
        for account in self.accounts:
            if account['email'] == email:
                account['last_used'] = datetime.now().isoformat()
                
                if success:
                    account['review_count'] = account.get('review_count', 0) + 1
                    logging.info(f"✅ Hesap kullanıldı: {email} (Toplam: {account['review_count']})")
                else:
                    account['status'] = 'error'
                    logging.warning(f"❌ Hesap hatası: {email}")
                
                # Hesap bilgilerini kaydet
                self.save_accounts_to_json()
                break
    
    def mark_account_banned(self, email: str):
        """Hesabı banlanmış olarak işaretler"""
        for account in self.accounts:
            if account['email'] == email:
                account['status'] = 'banned'
                account['notes'] = f"Banlandı: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                logging.warning(f"🚫 Hesap banlandı: {email}")
                
                # Hesap bilgilerini kaydet
                self.save_accounts_to_json()
                break
    
    def reset_account_cooldown(self, email: str):
        """Hesabın bekleme süresini sıfırlar"""
        for account in self.accounts:
            if account['email'] == email:
                account['last_used'] = ""
                account['review_count'] = 0
                account['status'] = 'active'
                logging.info(f"🔄 Hesap sıfırlandı: {email}")
                
                # Hesap bilgilerini kaydet
                self.save_accounts_to_json()
                break
    
    def get_account_stats(self) -> Dict:
        """Hesap istatistiklerini döndürür"""
        stats = {
            'total_accounts': len(self.accounts),
            'active_accounts': 0,
            'cooldown_accounts': 0,
            'banned_accounts': 0,
            'error_accounts': 0,
            'total_reviews': 0,
            'available_accounts': 0
        }
        
        for account in self.accounts:
            status = account.get('status', 'active')
            stats[f'{status}_accounts'] += 1
            stats['total_reviews'] += account.get('review_count', 0)
            
            # Kullanılabilir hesap sayısı
            if status == 'active':
                last_used = account.get('last_used', '')
                if last_used:
                    try:
                        last_used_time = datetime.fromisoformat(last_used)
                        cooldown_end = last_used_time + timedelta(hours=self.cooldown_hours)
                        
                        if datetime.now() >= cooldown_end and account.get('review_count', 0) < self.max_reviews_per_account:
                            stats['available_accounts'] += 1
                    except:
                        stats['available_accounts'] += 1
                else:
                    stats['available_accounts'] += 1
        
        return stats
    
    def print_account_status(self):
        """Hesap durumlarını yazdırır"""
        stats = self.get_account_stats()
        
        print("\n📊 HESAP DURUMU:")
        print("=" * 40)
        print(f"📧 Toplam Hesap: {stats['total_accounts']}")
        print(f"✅ Aktif: {stats['active_accounts']}")
        print(f"⏳ Bekleme: {stats['cooldown_accounts']}")
        print(f"🚫 Banlanmış: {stats['banned_accounts']}")
        print(f"❌ Hata: {stats['error_accounts']}")
        print(f"🎯 Kullanılabilir: {stats['available_accounts']}")
        print(f"⭐ Toplam Değerlendirme: {stats['total_reviews']}")
        print("=" * 40)
        
        # Detaylı hesap listesi
        print("\n📋 HESAP LİSTESİ:")
        for i, account in enumerate(self.accounts, 1):
            status_emoji = {
                'active': '✅',
                'cooldown': '⏳', 
                'banned': '🚫',
                'error': '❌'
            }
            
            status = account.get('status', 'active')
            emoji = status_emoji.get(status, '❓')
            
            print(f"{i}. {emoji} {account['email']} (Değerlendirme: {account.get('review_count', 0)})")
            
            if account.get('notes'):
                print(f"   📝 Not: {account['notes']}")

def create_sample_csv():
    """Örnek CSV dosyası oluşturur"""
    sample_data = [
        ['email', 'password', 'status', 'last_used', 'review_count', 'notes'],
        ['ornek1@gmail.com', 'sifre123', 'active', '', '0', 'Örnek hesap 1'],
        ['ornek2@gmail.com', 'sifre456', 'active', '', '0', 'Örnek hesap 2'],
        ['ornek3@gmail.com', 'sifre789', 'active', '', '0', 'Örnek hesap 3']
    ]
    
    try:
        with open('accounts.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
        
        logging.info("✅ Örnek CSV dosyası oluşturuldu: accounts.csv")
        return True
        
    except Exception as e:
        logging.error(f"CSV oluşturma hatası: {e}")
        return False

def test_account_manager():
    """Hesap manager'ı test eder"""
    print("🧪 Hesap Manager Testi")
    print("=" * 40)
    
    # Hesap manager oluştur
    am = AccountManager()
    
    # Örnek dosya oluştur
    if not os.path.exists(am.accounts_file):
        am.create_sample_accounts_file()
    
    # Hesapları yükle
    if am.load_accounts_from_json():
        print(f"✅ {len(am.accounts)} hesap yüklendi")
        
        # İstatistikleri göster
        am.print_account_status()
        
        # Kullanılabilir hesap al
        account = am.get_available_account()
        if account:
            print(f"\n🎯 Seçilen hesap: {account['email']}")
            
            # Hesabı kullanıldı olarak işaretle
            am.mark_account_used(account['email'], True)
            
            # Güncel durumu göster
            am.print_account_status()
        else:
            print("❌ Kullanılabilir hesap bulunamadı!")
    else:
        print("❌ Hesap yükleme başarısız!")

if __name__ == "__main__":
    # Test çalıştır
    test_account_manager()
