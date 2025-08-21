#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Review Bot Test Dosyası
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from google_review_bot import GoogleReviewBot

class TestGoogleReviewBot(unittest.TestCase):
    """GoogleReviewBot sınıfı için test sınıfı"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.bot = GoogleReviewBot()
    
    def test_random_delay(self):
        """Rastgele gecikme testi"""
        import time
        start_time = time.time()
        self.bot.random_delay(0.1, 0.2)
        end_time = time.time()
        
        # Gecikme süresini kontrol et
        delay_time = end_time - start_time
        self.assertGreaterEqual(delay_time, 0.1)
        self.assertLessEqual(delay_time, 0.3)  # Biraz tolerans
    
    def test_human_like_typing(self):
        """İnsan gibi yazma testi"""
        # Mock element oluştur
        mock_element = Mock()
        test_text = "Test metni"
        
        # Metodu çağır
        self.bot.human_like_typing(mock_element, test_text)
        
        # Element'in send_keys metodunun çağrıldığını kontrol et
        self.assertEqual(mock_element.send_keys.call_count, len(test_text))
    
    @patch('selenium.webdriver.Chrome')
    def test_setup_driver_success(self, mock_chrome):
        """Driver başarılı başlatma testi"""
        # Mock driver ayarla
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        # Metodu çağır
        result = self.bot.setup_driver()
        
        # Sonucu kontrol et
        self.assertTrue(result)
        self.assertIsNotNone(self.bot.driver)
        self.assertIsNotNone(self.bot.wait)
    
    def test_close_driver(self):
        """Driver kapatma testi"""
        # Mock driver oluştur
        self.bot.driver = Mock()
        
        # Metodu çağır
        self.bot.close_driver()
        
        # Driver'ın quit metodunun çağrıldığını kontrol et
        self.bot.driver.quit.assert_called_once()
        self.assertIsNone(self.bot.driver)

def run_tests():
    """Testleri çalıştır"""
    print("Google Review Bot Testleri Başlatılıyor...")
    print("=" * 50)
    
    # Test suite oluştur
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGoogleReviewBot)
    
    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Sonuçları göster
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ Tüm testler başarılı!")
    else:
        print("❌ Bazı testler başarısız!")
        print(f"Başarısız test sayısı: {len(result.failures)}")
        print(f"Hata sayısı: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_tests()
