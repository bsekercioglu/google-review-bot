#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Business Manager Test Modülü
Google Review Bot için işletme yöneticisi testleri
"""

import unittest
import json
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from business_manager import BusinessManager

class TestBusinessManager(unittest.TestCase):
    """BusinessManager sınıfı için test sınıfı"""
    
    def setUp(self):
        """Test öncesi hazırlık"""
        # Geçici test dosyası oluştur
        self.test_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.test_file.close()
        
        # Test verileri
        self.test_data = {
            "businesses": [
                {
                    "id": "biz_001",
                    "name": "Test Restoran 1",
                    "url": "https://www.google.com/maps/place/Test+Restoran+1/@41.0082,28.9784,17z",
                    "type": "restaurant",
                    "category": "Türk Mutfağı",
                    "location": "İstanbul, Fatih",
                    "max_rating": 5,
                    "min_rating": 4,
                    "review_count": 0,
                    "last_review_date": None,
                    "status": "active",
                    "notes": "Test restoranı"
                },
                {
                    "id": "biz_002",
                    "name": "Test Kafe 1",
                    "url": "https://www.google.com/maps/place/Test+Kafe+1/@41.0082,28.9784,17z",
                    "type": "cafe",
                    "category": "Kahve",
                    "location": "İstanbul, Beşiktaş",
                    "max_rating": 5,
                    "min_rating": 3,
                    "review_count": 1,
                    "last_review_date": "2024-01-14T10:00:00",
                    "status": "active",
                    "notes": "Test kafesi"
                },
                {
                    "id": "biz_003",
                    "name": "Test Otel 1",
                    "url": "https://www.google.com/maps/place/Test+Otel+1/@41.0082,28.9784,17z",
                    "type": "hotel",
                    "category": "Lüks Otel",
                    "location": "İstanbul, Şişli",
                    "max_rating": 5,
                    "min_rating": 4,
                    "review_count": 3,
                    "last_review_date": "2024-01-13T15:30:00",
                    "status": "completed",
                    "notes": "Test oteli"
                }
            ],
            "settings": {
                "max_reviews_per_business": 3,
                "min_delay_between_reviews": 3600,
                "max_delay_between_reviews": 7200,
                "cooldown_period_hours": 24,
                "auto_rating_distribution": {
                    "5_star": 0.6,
                    "4_star": 0.3,
                    "3_star": 0.1
                }
            },
            "metadata": {
                "created_date": "2024-01-15",
                "version": "1.0",
                "description": "Test işletme listesi",
                "total_businesses": 3
            }
        }
        
        # Test dosyasına veri yaz
        with open(self.test_file.name, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, indent=2, ensure_ascii=False)
        
        # BusinessManager'ı test dosyası ile başlat
        self.bm = BusinessManager(self.test_file.name)
    
    def tearDown(self):
        """Test sonrası temizlik"""
        # Test dosyasını sil
        if os.path.exists(self.test_file.name):
            os.unlink(self.test_file.name)
    
    def test_load_businesses(self):
        """İşletme yükleme testi"""
        result = self.bm.load_businesses()
        self.assertTrue(result)
        self.assertEqual(len(self.bm.businesses), 3)
        self.assertEqual(self.bm.businesses[0]['name'], "Test Restoran 1")
    
    def test_get_available_businesses(self):
        """Kullanılabilir işletme testi"""
        self.bm.load_businesses()
        
        # Tüm kullanılabilir işletmeler
        available = self.bm.get_available_businesses()
        self.assertEqual(len(available), 2)  # 2 aktif işletme
        
        # Restoran türünde işletmeler
        restaurants = self.bm.get_available_businesses(business_type="restaurant")
        self.assertEqual(len(restaurants), 1)
        self.assertEqual(restaurants[0]['name'], "Test Restoran 1")
        
        # Tamamlanmış işletmeler hariç
        completed = self.bm.get_available_businesses()
        self.assertNotIn("Test Otel 1", [b['name'] for b in completed])
    
    def test_get_random_business(self):
        """Rastgele işletme seçimi testi"""
        self.bm.load_businesses()
        
        # Rastgele işletme seç
        business = self.bm.get_random_business()
        self.assertIsNotNone(business)
        self.assertIn(business['status'], ['active'])
        
        # Belirli türde işletme seç
        cafe = self.bm.get_random_business(business_type="cafe")
        self.assertIsNotNone(cafe)
        self.assertEqual(cafe['type'], "cafe")
    
    def test_get_business_by_id(self):
        """ID ile işletme bulma testi"""
        self.bm.load_businesses()
        
        # Var olan işletme
        business = self.bm.get_business_by_id("biz_001")
        self.assertIsNotNone(business)
        self.assertEqual(business['name'], "Test Restoran 1")
        
        # Var olmayan işletme
        business = self.bm.get_business_by_id("biz_999")
        self.assertIsNone(business)
    
    def test_mark_business_reviewed(self):
        """İşletme değerlendirme işaretleme testi"""
        self.bm.load_businesses()
        
        # Başarılı değerlendirme
        result = self.bm.mark_business_reviewed("biz_001", True)
        self.assertTrue(result)
        
        # İşletme durumunu kontrol et
        business = self.bm.get_business_by_id("biz_001")
        self.assertEqual(business['review_count'], 1)
        self.assertIsNotNone(business['last_review_date'])
        
        # Başarısız değerlendirme
        result = self.bm.mark_business_reviewed("biz_002", False)
        self.assertTrue(result)
        
        # İşletme durumunu kontrol et
        business = self.bm.get_business_by_id("biz_002")
        self.assertEqual(business['status'], "error")
    
    def test_generate_random_rating(self):
        """Rastgele yıldız üretme testi"""
        self.bm.load_businesses()
        
        # 100 kez test et
        ratings = []
        for _ in range(100):
            rating = self.bm.generate_random_rating(business_type="restaurant")
            ratings.append(rating)
            self.assertIn(rating, [3, 4, 5])
        
        # Dağılımı kontrol et (yaklaşık)
        five_star_count = ratings.count(5)
        four_star_count = ratings.count(4)
        three_star_count = ratings.count(3)
        
        # 5 yıldız oranı yaklaşık %60 olmalı
        self.assertGreater(five_star_count, 50)
        self.assertLess(five_star_count, 70)
    
    def test_add_business(self):
        """İşletme ekleme testi"""
        self.bm.load_businesses()
        
        new_business = {
            "name": "Yeni Test İşletme",
            "url": "https://www.google.com/maps/place/Yeni+Test+İşletme/@41.0082,28.9784,17z",
            "type": "shop",
            "category": "Test Mağaza",
            "location": "İstanbul, Kadıköy",
            "max_rating": 5,
            "min_rating": 3,
            "notes": "Yeni test işletmesi"
        }
        
        result = self.bm.add_business(new_business)
        self.assertTrue(result)
        
        # İşletme sayısını kontrol et
        self.assertEqual(len(self.bm.businesses), 4)
        
        # Yeni işletmeyi kontrol et
        new_biz = self.bm.get_business_by_id("biz_004")
        self.assertIsNotNone(new_biz)
        self.assertEqual(new_biz['name'], "Yeni Test İşletme")
        self.assertEqual(new_biz['status'], "active")
        self.assertEqual(new_biz['review_count'], 0)
    
    def test_remove_business(self):
        """İşletme kaldırma testi"""
        self.bm.load_businesses()
        
        # İşletme kaldır
        result = self.bm.remove_business("biz_001")
        self.assertTrue(result)
        
        # İşletme sayısını kontrol et
        self.assertEqual(len(self.bm.businesses), 2)
        
        # Kaldırılan işletmeyi kontrol et
        business = self.bm.get_business_by_id("biz_001")
        self.assertIsNone(business)
    
    def test_reset_business_status(self):
        """İşletme durumu sıfırlama testi"""
        self.bm.load_businesses()
        
        # Belirli işletme durumunu sıfırla
        result = self.bm.reset_business_status("biz_003")
        self.assertTrue(result)
        
        # İşletme durumunu kontrol et
        business = self.bm.get_business_by_id("biz_003")
        self.assertEqual(business['status'], "active")
        self.assertEqual(business['review_count'], 0)
        self.assertIsNone(business['last_review_date'])
    
    def test_get_business_summary(self):
        """İşletme özeti testi"""
        self.bm.load_businesses()
        
        summary = self.bm.get_business_summary()
        
        self.assertEqual(summary['total_businesses'], 3)
        self.assertEqual(summary['active_businesses'], 2)
        self.assertEqual(summary['completed_businesses'], 1)
        self.assertEqual(summary['max_reviews_per_business'], 3)
        self.assertEqual(summary['cooldown_hours'], 24)
        
        # Tür dağılımını kontrol et
        type_dist = summary['type_distribution']
        self.assertEqual(type_dist['restaurant'], 1)
        self.assertEqual(type_dist['cafe'], 1)
        self.assertEqual(type_dist['hotel'], 1)
    
    def test_cooldown_period(self):
        """Bekleme süresi testi"""
        self.bm.load_businesses()
        
        # Son değerlendirme tarihini güncelle (1 saat önce)
        business = self.bm.get_business_by_id("biz_002")
        business['last_review_date'] = (datetime.now() - timedelta(hours=1)).isoformat()
        self.bm.save_businesses()
        
        # Kullanılabilir işletmeleri kontrol et
        available = self.bm.get_available_businesses()
        self.assertNotIn("biz_002", [b['id'] for b in available])
        
        # Son değerlendirme tarihini güncelle (25 saat önce)
        business['last_review_date'] = (datetime.now() - timedelta(hours=25)).isoformat()
        self.bm.save_businesses()
        
        # Kullanılabilir işletmeleri kontrol et
        available = self.bm.get_available_businesses()
        self.assertIn("biz_002", [b['id'] for b in available])

def run_business_manager_tests():
    """Business Manager testlerini çalıştır"""
    print("=" * 60)
    print("🧪 BUSINESS MANAGER TESTLERİ")
    print("=" * 60)
    
    # Test suite oluştur
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBusinessManager)
    
    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Sonuçları yazdır
    print("\n" + "=" * 60)
    print("📊 TEST SONUÇLARI")
    print("=" * 60)
    print(f"✅ Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Başarısız: {len(result.failures)}")
    print(f"⚠️ Hata: {len(result.errors)}")
    print(f"📈 Toplam: {result.testsRun}")
    
    if result.failures:
        print("\n❌ BAŞARISIZ TESTLER:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n⚠️ HATALI TESTLER:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

def test_business_manager_manual():
    """Manuel Business Manager testi"""
    print("=" * 60)
    print("🔧 MANUEL BUSINESS MANAGER TESTİ")
    print("=" * 60)
    
    # BusinessManager'ı başlat
    bm = BusinessManager()
    
    # İşletmeleri yükle
    if not bm.load_businesses():
        print("❌ İşletme listesi yüklenemedi!")
        return False
    
    print(f"✅ {len(bm.businesses)} işletme yüklendi")
    
    # İşletme durumunu göster
    bm.print_business_status()
    
    # Kullanılabilir işletmeleri göster
    available = bm.get_available_businesses()
    print(f"\n📋 Kullanılabilir İşletmeler: {len(available)}")
    
    for business in available:
        print(f"  - {business['name']} ({business['type']}) - {business['location']}")
    
    # Rastgele işletme seç
    random_business = bm.get_random_business()
    if random_business:
        print(f"\n🎯 Rastgele Seçilen İşletme: {random_business['name']}")
        print(f"   📍 Konum: {random_business['location']}")
        print(f"   🏷️ Tür: {random_business['type']}")
        print(f"   ⭐ Yıldız: {random_business['min_rating']}-{random_business['max_rating']}")
    
    # İşletme özeti
    summary = bm.get_business_summary()
    print(f"\n📊 İşletme Özeti:")
    print(f"   📈 Toplam: {summary['total_businesses']}")
    print(f"   ✅ Aktif: {summary['active_businesses']}")
    print(f"   🎯 Tamamlanan: {summary['completed_businesses']}")
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "manual":
        # Manuel test
        success = test_business_manager_manual()
        sys.exit(0 if success else 1)
    else:
        # Otomatik testler
        success = run_business_manager_tests()
        sys.exit(0 if success else 1)
