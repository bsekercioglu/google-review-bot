#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Değerlendirme Metinleri Test Dosyası
"""

import os
from dotenv import load_dotenv
from google_review_bot import ReviewTextGenerator

def test_ai_review_generation():
    """AI ile değerlendirme metni oluşturmayı test eder"""
    print("🤖 AI Değerlendirme Metinleri Testi")
    print("=" * 50)
    
    # Çevre değişkenlerini yükle
    load_dotenv()
    
    # API anahtarını kontrol et
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("⚠️  GEMINI_API_KEY bulunamadı!")
        print("📝 env.example dosyasını .env olarak kopyalayın ve API anahtarınızı ekleyin:")
        print("   copy env.example .env")
        print("   # .env dosyasını düzenleyin ve GEMINI_API_KEY=your_api_key_here ekleyin")
        print("\n🔄 Fallback metinlerle test ediliyor...")
    
    # ReviewTextGenerator'ı başlat
    generator = ReviewTextGenerator(api_key)
    
    # Test edilecek işletme türleri
    business_types = [
        "restaurant", "cafe", "hotel", "shop", "service",
        "medical", "beauty", "fitness", "education"
    ]
    
    print(f"\n📋 {len(business_types)} farklı işletme türü için test ediliyor...")
    
    for i, business_type in enumerate(business_types, 1):
        print(f"\n{i}. {business_type.upper()} için değerlendirme:")
        print("-" * 30)
        
        try:
            # AI ile değerlendirme metni oluştur
            review = generator.generate_review_text(
                business_type=business_type,
                rating=5,
                language="Turkish"
            )
            
            print(f"✅ Oluşturulan metin ({len(review)} karakter):")
            print(f"   {review}")
            
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    # Çoklu değerlendirme testi
    print(f"\n🔄 Çoklu değerlendirme testi (3 adet):")
    print("-" * 40)
    
    try:
        multiple_reviews = generator.generate_multiple_reviews(
            business_type="restaurant",
            rating=5,
            count=3,
            language="Turkish"
        )
        
        for i, review in enumerate(multiple_reviews, 1):
            print(f"{i}. {review}")
            print()
            
    except Exception as e:
        print(f"❌ Çoklu değerlendirme hatası: {e}")
    
    print("=" * 50)
    print("✅ Test tamamlandı!")

def test_fallback_reviews():
    """Fallback değerlendirme metinlerini test eder"""
    print("\n🔄 Fallback Değerlendirme Metinleri Testi")
    print("=" * 50)
    
    # API anahtarı olmadan generator oluştur
    generator = ReviewTextGenerator()
    
    business_types = ["restaurant", "cafe", "hotel", "shop", "service"]
    
    for business_type in business_types:
        print(f"\n📋 {business_type.upper()}:")
        print("-" * 20)
        
        for i in range(3):
            review = generator._get_fallback_review(business_type, 5)
            print(f"{i+1}. {review}")
        
        print()

if __name__ == "__main__":
    # Fallback testleri
    test_fallback_reviews()
    
    # AI testleri
    test_ai_review_generation()
    
    print("\n🎯 Test Sonuçları:")
    print("- Fallback metinler her zaman çalışır")
    print("- AI metinler için GEMINI_API_KEY gerekli")
    print("- API anahtarı yoksa otomatik olarak fallback kullanılır")
