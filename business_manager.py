#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google İşletme Yönetim Modülü
Google Review Bot için işletme listesi ve yönetimi
"""

import json
import random
import logging
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

class BusinessManager:
    """Google işletme yönetimi ve rotasyonu için sınıf"""
    
    def __init__(self, businesses_file="businesses.json"):
        """İşletme manager başlatıcı"""
        self.businesses_file = businesses_file
        self.businesses = []
        self.settings = {}
        self.metadata = {}
        self.used_businesses = []
        self.business_stats = {}
        
        # İşletme kullanım limitleri
        self.max_reviews_per_business = 3
        self.cooldown_hours = 24
        
        # İşletme durumları
        self.business_status = {
            'active': 'active',      # Aktif
            'cooldown': 'cooldown',  # Bekleme süresinde
            'completed': 'completed', # Tamamlanmış
            'error': 'error'         # Hata durumu
        }
    
    def load_businesses(self) -> bool:
        """JSON dosyasından işletme bilgilerini yükler"""
        try:
            if not os.path.exists(self.businesses_file):
                logging.warning(f"📁 {self.businesses_file} dosyası bulunamadı!")
                return False
            
            with open(self.businesses_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.businesses = data.get('businesses', [])
                self.settings = data.get('settings', {})
                self.metadata = data.get('metadata', {})
            
            # İstatistikleri yükle
            self.business_stats = data.get('stats', {})
            
            # Ayarları güncelle
            self.max_reviews_per_business = self.settings.get('max_reviews_per_business', 3)
            self.cooldown_hours = self.settings.get('cooldown_period_hours', 24)
            
            logging.info(f"✅ {len(self.businesses)} işletme yüklendi")
            return True
            
        except Exception as e:
            logging.error(f"İşletme yükleme hatası: {e}")
            return False
    
    def save_businesses(self) -> bool:
        """İşletme bilgilerini JSON dosyasına kaydeder"""
        try:
            data = {
                'businesses': self.businesses,
                'settings': self.settings,
                'metadata': self.metadata,
                'stats': self.business_stats,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.businesses_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logging.info("✅ İşletme bilgileri kaydedildi")
            return True
            
        except Exception as e:
            logging.error(f"İşletme kaydetme hatası: {e}")
            return False
    
    def get_available_businesses(self, business_type: str = None, location: str = None) -> List[Dict]:
        """Kullanılabilir işletmeleri döndürür"""
        available = []
        
        for business in self.businesses:
            # Durum kontrolü
            if business.get('status') != 'active':
                continue
            
            # İşletme türü filtresi
            if business_type and business.get('type') != business_type:
                continue
            
            # Konum filtresi
            if location and location.lower() not in business.get('location', '').lower():
                continue
            
            # Değerlendirme sayısı kontrolü
            if business.get('review_count', 0) >= self.max_reviews_per_business:
                continue
            
            # Son değerlendirme tarihi kontrolü
            last_review = business.get('last_review_date')
            if last_review:
                try:
                    last_date = datetime.fromisoformat(last_review)
                    if datetime.now() - last_date < timedelta(hours=self.cooldown_hours):
                        continue
                except:
                    pass
            
            available.append(business)
        
        return available
    
    def get_random_business(self, business_type: str = None, location: str = None) -> Optional[Dict]:
        """Rastgele bir işletme seçer"""
        available = self.get_available_businesses(business_type, location)
        
        if not available:
            logging.warning("⚠️ Kullanılabilir işletme bulunamadı!")
            return None
        
        business = random.choice(available)
        logging.info(f"🎯 Seçilen işletme: {business.get('name')} ({business.get('type')})")
        return business
    
    def get_business_by_id(self, business_id: str) -> Optional[Dict]:
        """ID ile işletme bulur"""
        for business in self.businesses:
            if business.get('id') == business_id:
                return business
        return None
    
    def get_businesses_by_type(self, business_type: str) -> List[Dict]:
        """İşletme türüne göre filtreler"""
        return [b for b in self.businesses if b.get('type') == business_type]
    
    def get_businesses_by_location(self, location: str) -> List[Dict]:
        """Konuma göre filtreler"""
        return [b for b in self.businesses if location.lower() in b.get('location', '').lower()]
    
    def mark_business_reviewed(self, business_id: str, success: bool = True) -> bool:
        """İşletmeye değerlendirme bırakıldığını işaretler"""
        business = self.get_business_by_id(business_id)
        if not business:
            logging.error(f"❌ İşletme bulunamadı: {business_id}")
            return False
        
        # Değerlendirme sayısını artır
        current_count = business.get('review_count', 0)
        business['review_count'] = current_count + 1
        
        # Son değerlendirme tarihini güncelle
        business['last_review_date'] = datetime.now().isoformat()
        
        # Durumu güncelle
        if business['review_count'] >= self.max_reviews_per_business:
            business['status'] = 'completed'
            logging.info(f"✅ İşletme tamamlandı: {business.get('name')}")
        elif not success:
            business['status'] = 'error'
            logging.warning(f"⚠️ İşletme hata durumunda: {business.get('name')}")
        
        # İstatistikleri güncelle
        self._update_business_stats(business, success)
        
        # Değişiklikleri kaydet
        return self.save_businesses()
    
    def _update_business_stats(self, business: Dict, success: bool):
        """İşletme istatistiklerini günceller"""
        business_id = business.get('id')
        if not business_id:
            return
        
        if business_id not in self.business_stats:
            self.business_stats[business_id] = {
                'total_reviews': 0,
                'successful_reviews': 0,
                'failed_reviews': 0,
                'last_review_date': None
            }
        
        stats = self.business_stats[business_id]
        stats['total_reviews'] += 1
        stats['last_review_date'] = datetime.now().isoformat()
        
        if success:
            stats['successful_reviews'] += 1
        else:
            stats['failed_reviews'] += 1
    
    def get_rating_distribution(self) -> Dict:
        """Yıldız dağılımını döndürür"""
        return self.settings.get('auto_rating_distribution', {
            "5_star": 0.6,
            "4_star": 0.3,
            "3_star": 0.1
        })
    
    def generate_random_rating(self, business_type: str = None, business_id: str = None) -> int:
        """İşletme türüne göre rastgele yıldız üretir"""
        
        # Belirli bir işletme için yıldız aralığını al
        if business_id:
            business = self.get_business_by_id(business_id)
            if business:
                min_rating = business.get('min_rating', 3)
                max_rating = business.get('max_rating', 5)
                return random.randint(min_rating, max_rating)
        
        # İşletme türüne göre ayarları al
        type_settings = self.get_business_type_settings(business_type)
        if type_settings:
            min_rating = type_settings.get('min_rating', 3)
            max_rating = type_settings.get('max_rating', 5)
            return random.randint(min_rating, max_rating)
        
        # Genel dağılımı kullan
        distribution = self.get_rating_distribution()
        rand = random.random()
        
        if rand < distribution.get('5_star', 0.6):
            return 5
        elif rand < distribution.get('5_star', 0.6) + distribution.get('4_star', 0.3):
            return 4
        else:
            return 3
    
    def get_business_type_settings(self, business_type: str) -> Dict:
        """İşletme türü ayarlarını döndürür"""
        return self.settings.get('business_types', {}).get(business_type, {})
    
    def get_ai_prompts_for_business(self, business_type: str) -> List[str]:
        """İşletme türü için AI prompt'larını döndürür"""
        type_settings = self.get_business_type_settings(business_type)
        return type_settings.get('ai_prompts', [])
    
    def reset_business_status(self, business_id: str = None) -> bool:
        """İşletme durumunu sıfırlar"""
        if business_id:
            business = self.get_business_by_id(business_id)
            if business:
                business['status'] = 'active'
                business['review_count'] = 0
                business['last_review_date'] = None
                logging.info(f"✅ İşletme durumu sıfırlandı: {business.get('name')}")
                return self.save_businesses()
        else:
            # Tüm işletmeleri sıfırla
            for business in self.businesses:
                business['status'] = 'active'
                business['review_count'] = 0
                business['last_review_date'] = None
            
            logging.info("✅ Tüm işletme durumları sıfırlandı")
            return self.save_businesses()
        
        return False
    
    def add_business(self, business_data: Dict) -> bool:
        """Yeni işletme ekler"""
        # ID kontrolü
        if not business_data.get('id'):
            business_data['id'] = f"biz_{len(self.businesses) + 1:03d}"
        
        # Varsayılan değerler
        business_data.setdefault('review_count', 0)
        business_data.setdefault('last_review_date', None)
        business_data.setdefault('status', 'active')
        
        self.businesses.append(business_data)
        logging.info(f"✅ Yeni işletme eklendi: {business_data.get('name')}")
        return self.save_businesses()
    
    def remove_business(self, business_id: str) -> bool:
        """İşletme kaldırır"""
        business = self.get_business_by_id(business_id)
        if business:
            self.businesses.remove(business)
            logging.info(f"✅ İşletme kaldırıldı: {business.get('name')}")
            return self.save_businesses()
        return False
    
    def print_business_status(self):
        """İşletme durumlarını yazdırır"""
        print("\n" + "="*60)
        print("📊 İŞLETME DURUMU")
        print("="*60)
        
        total = len(self.businesses)
        active = len([b for b in self.businesses if b.get('status') == 'active'])
        completed = len([b for b in self.businesses if b.get('status') == 'completed'])
        error = len([b for b in self.businesses if b.get('status') == 'error'])
        
        print(f"📈 Toplam İşletme: {total}")
        print(f"✅ Aktif: {active}")
        print(f"🎯 Tamamlanan: {completed}")
        print(f"❌ Hata: {error}")
        
        print("\n📋 İşletme Listesi:")
        print("-" * 60)
        
        for business in self.businesses:
            status_icon = {
                'active': '✅',
                'completed': '🎯',
                'error': '❌',
                'cooldown': '⏳'
            }.get(business.get('status'), '❓')
            
            print(f"{status_icon} {business.get('name')} ({business.get('type')})")
            print(f"   📍 {business.get('location')}")
            print(f"   ⭐ {business.get('review_count', 0)}/{self.max_reviews_per_business} değerlendirme")
            print(f"   🌟 {business.get('min_rating')}-{business.get('max_rating')} yıldız")
            print()
    
    def get_business_summary(self) -> Dict:
        """İşletme özeti döndürür"""
        total = len(self.businesses)
        active = len([b for b in self.businesses if b.get('status') == 'active'])
        completed = len([b for b in self.businesses if b.get('status') == 'completed'])
        
        type_distribution = {}
        for business in self.businesses:
            biz_type = business.get('type', 'unknown')
            type_distribution[biz_type] = type_distribution.get(biz_type, 0) + 1
        
        return {
            'total_businesses': total,
            'active_businesses': active,
            'completed_businesses': completed,
            'type_distribution': type_distribution,
            'max_reviews_per_business': self.max_reviews_per_business,
            'cooldown_hours': self.cooldown_hours
        }
