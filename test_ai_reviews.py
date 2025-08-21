#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Değerlendirme Metinleri Test Dosyası
"""

import os
import random
import time

def test_fallback_reviews():
    """Fallback değerlendirme metinlerini test eder"""
    print("🔄 Fallback Değerlendirme Metinleri Testi")
    print("=" * 50)
    
    # Fallback değerlendirme metinleri
    fallback_reviews = {
        "restaurant": [
            "Harika bir deneyimdi! Yemekler çok lezzetli ve servis hızlıydı. Kesinlikle tekrar geleceğim.",
            "Mükemmel bir restoran. Yemekler taze ve kaliteli. Personel çok ilgili ve güler yüzlü.",
            "Çok memnun kaldım. Yemekler lezzetli, ortam temiz ve hizmet kaliteli. Tavsiye ederim.",
            "Harika bir yer! Yemekler çok güzel, fiyatlar makul. Ailemle birlikte çok keyifli vakit geçirdik.",
            "Kesinlikle tavsiye ederim. Yemekler lezzetli, servis hızlı ve personel çok nazik."
        ],
        "cafe": [
            "Çok güzel bir kafe. Kahve lezzetli, ortam rahat. Çalışmak için ideal bir yer.",
            "Harika bir deneyim! Kahve çok güzel, tatlılar lezzetli. Personel çok ilgili.",
            "Mükemmel bir kafe. Ortam sakin, kahve kaliteli. Arkadaşlarla buluşmak için ideal.",
            "Çok memnun kaldım. Kahve harika, servis hızlı. Kesinlikle tekrar geleceğim.",
            "Harika bir yer! Kahve lezzetli, ortam temiz. Çalışmak için çok uygun."
        ],
        "hotel": [
            "Harika bir otel! Odalar temiz, personel çok ilgili. Konforlu bir konaklama deneyimi yaşadık.",
            "Mükemmel bir deneyim. Oda çok temiz, kahvaltı lezzetli. Personel çok nazik.",
            "Çok memnun kaldım. Otel çok güzel, hizmet kaliteli. Kesinlikle tekrar kalacağım.",
            "Harika bir otel! Konumu ideal, odalar temiz. Personel çok yardımsever.",
            "Mükemmel bir konaklama deneyimi. Oda çok rahat, hizmet kaliteli. Tavsiye ederim."
        ],
        "shop": [
            "Harika bir mağaza! Ürünler kaliteli, fiyatlar makul. Personel çok yardımsever.",
            "Mükemmel bir alışveriş deneyimi. Ürün çeşitliliği fazla, hizmet kaliteli.",
            "Çok memnun kaldım. Mağaza çok güzel, ürünler kaliteli. Kesinlikle tekrar geleceğim.",
            "Harika bir yer! Ürünler taze, fiyatlar uygun. Personel çok ilgili.",
            "Mükemmel bir mağaza. Ürün kalitesi yüksek, hizmet hızlı. Tavsiye ederim."
        ],
        "service": [
            "Harika bir hizmet! Çok profesyonel ve kaliteli. Kesinlikle tavsiye ederim.",
            "Mükemmel bir deneyim. Hizmet kaliteli, personel çok ilgili. Çok memnun kaldım.",
            "Çok profesyonel bir hizmet. Kaliteli ve güvenilir. Tekrar tercih edeceğim.",
            "Harika bir hizmet deneyimi! Çok memnun kaldım. Personel çok yardımsever.",
            "Mükemmel bir hizmet. Kaliteli ve hızlı. Kesinlikle tavsiye ederim."
        ]
    }
    
    business_types = ["restaurant", "cafe", "hotel", "shop", "service"]
    
    for business_type in business_types:
        print(f"\n📋 {business_type.upper()}:")
        print("-" * 20)
        
        reviews = fallback_reviews.get(business_type, fallback_reviews["service"])
        for i in range(3):
            review = random.choice(reviews)
            print(f"{i+1}. {review}")
        
        print()

def test_business_manager_integration():
    """Business Manager entegrasyonunu test eder"""
    print("\n🏢 Business Manager Entegrasyon Testi")
    print("=" * 50)
    
    try:
        from business_manager import BusinessManager
        
        # BusinessManager'ı başlat
        bm = BusinessManager()
        
        # İşletmeleri yükle
        if bm.load_businesses():
            print("✅ İşletme listesi başarıyla yüklendi")
            
            # Rastgele yıldız üretme testi
            print("\n⭐ Rastgele Yıldız Üretme Testi:")
            for i in range(5):
                rating = bm.generate_random_rating(business_type="restaurant")
                print(f"  {i+1}. {rating} yıldız")
            
            # İşletme türü ayarları testi
            print("\n🏷️ İşletme Türü Ayarları:")
            type_settings = bm.get_business_type_settings("restaurant")
            print(f"  Restoran ayarları: {type_settings}")
            
            # AI prompt'ları testi
            print("\n🤖 AI Prompt'ları:")
            ai_prompts = bm.get_ai_prompts_for_business("restaurant")
            print(f"  Restoran AI prompt'ları: {ai_prompts}")
            
        else:
            print("❌ İşletme listesi yüklenemedi")
            
    except ImportError as e:
        print(f"❌ BusinessManager import hatası: {e}")
    except Exception as e:
        print(f"❌ Test hatası: {e}")

def test_rating_distribution():
    """Yıldız dağılımını test eder"""
    print("\n📊 Yıldız Dağılımı Testi")
    print("=" * 50)
    
    try:
        from business_manager import BusinessManager
        
        bm = BusinessManager()
        bm.load_businesses()
        
        # 100 kez test et
        ratings = []
        for _ in range(100):
            rating = bm.generate_random_rating(business_type="restaurant")
            ratings.append(rating)
        
        # Dağılımı hesapla
        five_star = ratings.count(5)
        four_star = ratings.count(4)
        three_star = ratings.count(3)
        
        print(f"5 yıldız: {five_star} ({five_star/100*100:.1f}%)")
        print(f"4 yıldız: {four_star} ({four_star/100*100:.1f}%)")
        print(f"3 yıldız: {three_star} ({three_star/100*100:.1f}%)")
        
        # Dağılım kontrolü
        if five_star > 50 and five_star < 70:
            print("✅ 5 yıldız dağılımı normal")
        else:
            print("⚠️ 5 yıldız dağılımı beklenenden farklı")
            
    except Exception as e:
        print(f"❌ Yıldız dağılımı test hatası: {e}")

if __name__ == "__main__":
    # Fallback testleri
    test_fallback_reviews()
    
    # Business Manager entegrasyon testi
    test_business_manager_integration()
    
    # Yıldız dağılımı testi
    test_rating_distribution()
    
    print("\n🎯 Test Sonuçları:")
    print("- Fallback metinler her zaman çalışır")
    print("- Business Manager entegrasyonu test edildi")
    print("- Yıldız dağılımı kontrol edildi")
    print("- AI metinler için GEMINI_API_KEY gerekli")
    print("- API anahtarı yoksa otomatik olarak fallback kullanılır")
