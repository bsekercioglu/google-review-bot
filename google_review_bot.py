#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google İşletme Değerlendirme Botu
SADECE EĞİTİM AMAÇLIDIR - KULLANIM SORUMLULUĞU KULLANICIYA AİTTİR
"""

import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import os
from dotenv import load_dotenv
import google.generativeai as genai
from proxy_manager import ProxyManager
from account_manager import AccountManager

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class ReviewTextGenerator:
    """Gemini AI kullanarak rastgele değerlendirme metinleri oluşturur"""
    
    def __init__(self, api_key=None):
        """Gemini AI başlatıcı"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            logging.warning("Gemini API anahtarı bulunamadı. Önceden tanımlı metinler kullanılacak.")
    
    def generate_review_text(self, business_type="restaurant", rating=5, language="Turkish"):
        """Gemini AI ile değerlendirme metni oluşturur"""
        if not self.model:
            return self._get_fallback_review(business_type, rating)
        
        try:
            # İşletme türüne göre prompt oluştur
            business_prompts = {
                "restaurant": "restoran",
                "cafe": "kafe",
                "hotel": "otel",
                "shop": "mağaza",
                "service": "hizmet",
                "medical": "sağlık kurumu",
                "beauty": "güzellik salonu",
                "fitness": "spor salonu",
                "education": "eğitim kurumu"
            }
            
            business_name = business_prompts.get(business_type, "işletme")
            
            prompt = f"""
            {language} dilinde, {business_name} için {rating} yıldızlık bir Google değerlendirme metni yaz.
            
            Gereksinimler:
            - 50-150 kelime arası
            - Gerçekçi ve samimi olmalı
            - Spam veya bot gibi görünmemeli
            - İşletme türüne uygun olmalı
            - Sadece {language} dilinde yaz
            - Emoji kullanma
            - Çok resmi olma
            
            Örnek ton: Samimi, memnun müşteri
            """
            
            response = self.model.generate_content(prompt)
            review_text = response.text.strip()
            
            # Metni temizle ve kontrol et
            if len(review_text) < 20 or len(review_text) > 500:
                return self._get_fallback_review(business_type, rating)
            
            logging.info(f"Gemini AI ile değerlendirme metni oluşturuldu: {len(review_text)} karakter")
            return review_text
            
        except Exception as e:
            logging.error(f"Gemini AI hatası: {e}")
            return self._get_fallback_review(business_type, rating)
    
    def _get_fallback_review(self, business_type, rating):
        """API çalışmadığında kullanılacak önceden tanımlı metinler"""
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
        
        reviews = fallback_reviews.get(business_type, fallback_reviews["service"])
        return random.choice(reviews)
    
    def generate_multiple_reviews(self, business_type="restaurant", rating=5, count=5, language="Turkish"):
        """Birden fazla farklı değerlendirme metni oluşturur"""
        reviews = []
        for i in range(count):
            review = self.generate_review_text(business_type, rating, language)
            reviews.append(review)
            # API limitlerini aşmamak için kısa bekleme
            if self.model:
                time.sleep(1)
        
        return reviews

class GoogleReviewBot:
    def __init__(self, use_ai_reviews=True, use_proxy_rotation=False, use_account_rotation=True):
        """Bot başlatıcı"""
        self.driver = None
        self.wait = None
        self.ua = UserAgent()
        self.use_ai_reviews = use_ai_reviews
        self.use_proxy_rotation = use_proxy_rotation
        self.use_account_rotation = use_account_rotation
        self.review_generator = ReviewTextGenerator() if use_ai_reviews else None
        self.proxy_manager = ProxyManager() if use_proxy_rotation else None
        self.account_manager = AccountManager() if use_account_rotation else None
        load_dotenv()
        
    def setup_driver(self):
        """Chrome driver'ı ayarlar"""
        try:
            chrome_options = Options()
            
            # Tarayıcı gizleme seçenekleri
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User agent rastgeleleştirme
            chrome_options.add_argument(f"--user-agent={self.ua.random}")
            
            # Proxy kullanımı
            proxy_url = None
            
            # Önce proxy rotation kontrol et
            if self.use_proxy_rotation and self.proxy_manager:
                if not hasattr(self.proxy_manager, 'working_proxies') or not self.proxy_manager.working_proxies:
                    logging.info("🔄 Proxy'ler başlatılıyor...")
                    if self.proxy_manager.initialize_proxies():
                        proxy_url = self.proxy_manager.get_random_proxy()
                        logging.info(f"🌐 Otomatik proxy seçildi: {proxy_url}")
                    else:
                        logging.warning("⚠️ Proxy başlatılamadı, proxy olmadan devam ediliyor")
                else:
                    proxy_url = self.proxy_manager.get_random_proxy()
                    logging.info(f"🌐 Mevcut proxy kullanılıyor: {proxy_url}")
            
            # Manuel proxy ayarı (.env dosyasından)
            elif os.getenv('PROXY'):
                proxy_url = os.getenv('PROXY')
                logging.info(f"🌐 Manuel proxy kullanılıyor: {proxy_url}")
            
            # Proxy'yi Chrome'a uygula
            if proxy_url:
                chrome_options.add_argument(f"--proxy-server={proxy_url}")
            
            # Driver servisini ayarla
            service = Service(ChromeDriverManager().install())
            
            # Driver'ı başlat
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Wait objesini ayarla
            self.wait = WebDriverWait(self.driver, 10)
            
            logging.info("Chrome driver başarıyla başlatıldı")
            return True
            
        except Exception as e:
            logging.error(f"Driver başlatma hatası: {e}")
            return False
    
    def random_delay(self, min_delay=2, max_delay=5):
        """Rastgele gecikme ekler"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def human_like_typing(self, element, text):
        """İnsan gibi yavaş yazma simülasyonu"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
    
    def check_google_login(self):
        """Google oturum durumunu kontrol eder"""
        try:
            # Google'a git
            self.driver.get("https://accounts.google.com")
            self.random_delay(2, 4)
            
            # Oturum açık mı kontrol et
            current_url = self.driver.current_url
            
            # Eğer Google hesap sayfasındaysa ve giriş yapılmışsa
            if "myaccount.google.com" in current_url or "accounts.google.com/signin" not in current_url:
                logging.info("✅ Google oturumu açık")
                return True
            else:
                logging.warning("⚠️ Google oturumu açık değil")
                return False
                
        except Exception as e:
            logging.error(f"Google oturum kontrolü hatası: {e}")
            return False
    
    def login_to_google(self, email, password):
        """Google hesabına giriş yapar"""
        try:
            logging.info("🔐 Google hesabına giriş yapılıyor...")
            
            # Google giriş sayfasına git
            self.driver.get("https://accounts.google.com/signin")
            self.random_delay(3, 5)
            
            # Email girişi
            email_field = self.wait.until(
                EC.element_to_be_clickable((By.NAME, "identifier"))
            )
            email_field.clear()
            self.human_like_typing(email_field, email)
            
            # İleri butonuna tıkla
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='İleri'] or //span[text()='Next']"))
            )
            next_button.click()
            self.random_delay(2, 4)
            
            # Şifre girişi
            password_field = self.wait.until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            password_field.clear()
            self.human_like_typing(password_field, password)
            
            # Giriş yap butonuna tıkla
            signin_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='İleri'] or //span[text()='Next']"))
            )
            signin_button.click()
            self.random_delay(5, 8)
            
            # Giriş başarılı mı kontrol et
            if self.check_google_login():
                logging.info("✅ Google hesabına başarıyla giriş yapıldı")
                return True
            else:
                logging.error("❌ Google girişi başarısız")
                return False
                
        except Exception as e:
            logging.error(f"Google giriş hatası: {e}")
            return False
    
    def handle_2fa(self):
        """2FA (İki faktörlü doğrulama) işlemini yönetir"""
        try:
            # 2FA sayfasında mı kontrol et
            if "challenge" in self.driver.current_url or "2fa" in self.driver.current_url:
                logging.info("🔐 2FA doğrulaması gerekiyor")
                
                # Kullanıcıdan 2FA kodunu al
                print("\n🔐 İki faktörlü doğrulama kodu gerekiyor!")
                print("📱 Telefonunuza gelen kodu girin:")
                code = input("2FA Kodu: ").strip()
                
                if code:
                    # 2FA kodunu gir
                    code_field = self.wait.until(
                        EC.element_to_be_clickable((By.NAME, "totpPin") or (By.NAME, "code"))
                    )
                    code_field.clear()
                    self.human_like_typing(code_field, code)
                    
                    # Doğrula butonuna tıkla
                    verify_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Doğrula'] or //span[text()='Verify']"))
                    )
                    verify_button.click()
                    self.random_delay(3, 5)
                    
                    logging.info("✅ 2FA doğrulaması tamamlandı")
                    return True
                
            return False
            
        except Exception as e:
            logging.error(f"2FA işlemi hatası: {e}")
            return False
    
    def leave_review(self, business_url, review_text, rating=5):
        """Google işletme sayfasında değerlendirme bırakır"""
        try:
            logging.info(f"İşletme sayfasına gidiliyor: {business_url}")
            self.driver.get(business_url)
            self.random_delay(3, 6)
            
            # Sayfa yüklenmesini bekle
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Google oturum kontrolü
            if not self.check_google_login():
                logging.error("Google oturumu açık değil! Değerlendirme bırakılamaz.")
                return False
            
            # Değerlendirme butonunu bul ve tıkla
            review_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Değerlendirme yaz') or contains(text(), 'Write a review')]"))
            )
            review_button.click()
            logging.info("Değerlendirme butonu tıklandı")
            self.random_delay(2, 4)
            
            # Yıldız derecelendirmesi
            stars = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@role='button' and @aria-label*='star']"))
            )
            
            if rating == 5 and len(stars) >= 5:
                stars[4].click()  # 5. yıldız (index 4)
                logging.info("5 yıldız seçildi")
            else:
                stars[rating-1].click()
                logging.info(f"{rating} yıldız seçildi")
            
            self.random_delay(1, 3)
            
            # Değerlendirme metni yaz
            review_textarea = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//textarea[@aria-label*='review' or @aria-label*='değerlendirme']"))
            )
            review_textarea.click()
            self.human_like_typing(review_textarea, review_text)
            logging.info("Değerlendirme metni yazıldı")
            self.random_delay(2, 4)
            
            # Gönder butonunu bul ve tıkla
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Gönder') or contains(text(), 'Post') or contains(text(), 'Submit')]"))
            )
            submit_button.click()
            logging.info("Değerlendirme gönderildi")
            
            # Gönderim sonrası bekle
            self.random_delay(3, 6)
            
            return True
            
        except Exception as e:
            logging.error(f"Değerlendirme bırakma hatası: {e}")
            return False
    
    def close_driver(self):
        """Driver'ı kapatır"""
        if self.driver:
            self.driver.quit()
            logging.info("Driver kapatıldı")
    
    def run_bot(self, business_url, review_text=None, num_reviews=1, business_type="restaurant", google_email=None, google_password=None):
        """Ana bot çalıştırma fonksiyonu"""
        try:
            if not self.setup_driver():
                return False
            
            success_count = 0
            
            for i in range(num_reviews):
                logging.info(f"Değerlendirme {i+1}/{num_reviews} başlatılıyor...")
                
                # Hesap seçimi
                current_email = None
                current_password = None
                
                if self.use_account_rotation and self.account_manager:
                    # Hesap rotasyonu kullan
                    account = self.account_manager.get_available_account()
                    if account:
                        current_email = account['email']
                        current_password = account['password']
                        logging.info(f"🔐 Hesap rotasyonu: {current_email}")
                    else:
                        logging.error("❌ Kullanılabilir hesap bulunamadı!")
                        return False
                else:
                    # Manuel hesap kullan
                    current_email = google_email
                    current_password = google_password
                
                # Google hesabına giriş yap
                if current_email and current_password:
                    logging.info(f"🔐 Google hesabına giriş yapılıyor: {current_email}")
                    if not self.login_to_google(current_email, current_password):
                        logging.error(f"❌ Google girişi başarısız: {current_email}")
                        
                        # Hesap hatası işaretle
                        if self.use_account_rotation and self.account_manager:
                            self.account_manager.mark_account_used(current_email, False)
                        
                        continue
                    
                    # 2FA kontrolü
                    self.handle_2fa()
                
                # AI ile değerlendirme metni oluştur veya kullanıcının verdiği metni kullan
                if self.use_ai_reviews and self.review_generator:
                    current_review_text = self.review_generator.generate_review_text(
                        business_type=business_type, 
                        rating=5, 
                        language="Turkish"
                    )
                    logging.info(f"AI ile oluşturulan değerlendirme: {current_review_text[:50]}...")
                else:
                    current_review_text = review_text or "Harika bir deneyimdi! Kesinlikle tavsiye ederim."
                
                if self.leave_review(business_url, current_review_text):
                    success_count += 1
                    logging.info(f"Değerlendirme {i+1} başarıyla tamamlandı")
                    
                    # Hesap başarılı kullanım işaretle
                    if self.use_account_rotation and self.account_manager and current_email:
                        self.account_manager.mark_account_used(current_email, True)
                else:
                    logging.warning(f"Değerlendirme {i+1} başarısız")
                    
                    # Hesap hatası işaretle
                    if self.use_account_rotation and self.account_manager and current_email:
                        self.account_manager.mark_account_used(current_email, False)
                
                # Değerlendirmeler arası uzun bekleme
                if i < num_reviews - 1:
                    wait_time = random.randint(30, 60)
                    logging.info(f"Sonraki değerlendirme için {wait_time} saniye bekleniyor...")
                    time.sleep(wait_time)
            
            logging.info(f"Toplam {success_count}/{num_reviews} değerlendirme başarıyla tamamlandı")
            return success_count > 0
            
        except Exception as e:
            logging.error(f"Bot çalıştırma hatası: {e}")
            return False
        finally:
            self.close_driver()

def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print("GOOGLE İŞLETME DEĞERLENDİRME BOTU")
    print("🤖 AI DESTEKLİ - SADECE EĞİTİM AMAÇLIDIR!")
    print("=" * 60)
    
    # Kullanıcıdan bilgi al
    business_url = input("Google işletme URL'sini girin: ").strip()
    
    if not business_url:
        print("Hata: URL gerekli!")
        return
    
    # Hesap yönetimi seçeneği
    print("\n🔐 Hesap Yönetimi:")
    print("1. Hesap listesi kullan (önerilen)")
    print("2. Tek hesap girişi")
    
    account_choice = input("Seçiminiz (1/2): ").strip()
    
    google_email = None
    google_password = None
    
    if account_choice == "2":
        # Tek hesap girişi
        print("\n🔐 Google Hesap Bilgileri:")
        print("⚠️  NOT: Google işletme değerlendirmesi bırakmak için Google hesabına giriş yapılması gerekir!")
        
        google_email = input("Google Email adresinizi girin: ").strip()
        google_password = input("Google şifrenizi girin (görünmez): ").strip()
        
        if not google_email or not google_password:
            print("Hata: Email ve şifre gerekli!")
            return
    
    # AI kullanımı seçeneği
    print("\n🤖 AI Özellikleri:")
    print("1. AI ile otomatik değerlendirme metni oluştur (önerilen)")
    print("2. Kendi metninizi girin")
    
    ai_choice = input("Seçiminiz (1/2): ").strip()
    
    # Proxy kullanımı seçeneği
    print("\n🌐 Proxy Seçenekleri:")
    print("1. Proxy kullanma (varsayılan)")
    print("2. Manuel proxy (.env dosyasından)")
    print("3. Otomatik proxy rotation (önerilen)")
    
    proxy_choice = input("Seçiminiz (1/2/3): ").strip()
    
    review_text = None
    business_type = "restaurant"
    
    if ai_choice == "1":
        print("\n📋 İşletme türünü seçin:")
        print("1. Restoran")
        print("2. Kafe")
        print("3. Otel")
        print("4. Mağaza")
        print("5. Hizmet")
        print("6. Sağlık")
        print("7. Güzellik")
        print("8. Spor")
        print("9. Eğitim")
        print("10. Diğer")
        
        type_choice = input("Seçiminiz (1-10): ").strip()
        
        business_types = {
            "1": "restaurant", "2": "cafe", "3": "hotel", "4": "shop",
            "5": "service", "6": "medical", "7": "beauty", "8": "fitness",
            "9": "education", "10": "service"
        }
        
        business_type = business_types.get(type_choice, "restaurant")
        print(f"✅ Seçilen işletme türü: {business_type}")
        
    else:
        review_text = input("Değerlendirme metnini girin: ").strip()
        if not review_text:
            print("Hata: Değerlendirme metni gerekli!")
            return
    
    num_reviews = int(input("Kaç değerlendirme bırakılacak? (1-5): ").strip())
    
    if num_reviews < 1 or num_reviews > 5:
        print("Hata: Değerlendirme sayısı 1-5 arasında olmalı!")
        return
    
    # Bot'u başlat
    use_ai = ai_choice == "1"
    use_proxy_rotation = proxy_choice == "3"
    use_account_rotation = account_choice == "1"
    bot = GoogleReviewBot(use_ai_reviews=use_ai, use_proxy_rotation=use_proxy_rotation, use_account_rotation=use_account_rotation)
    
    print(f"\n🤖 Bot başlatılıyor...")
    print(f"URL: {business_url}")
    print(f"Hesap Rotasyonu: {'Evet' if use_account_rotation else 'Hayır'}")
    print(f"AI Kullanımı: {'Evet' if use_ai else 'Hayır'}")
    print(f"Proxy Rotation: {'Evet' if use_proxy_rotation else 'Hayır'}")
    if use_ai:
        print(f"İşletme Türü: {business_type}")
    else:
        print(f"Değerlendirme: {review_text}")
    print(f"Sayı: {num_reviews}")
    
    # Hesap durumunu göster
    if use_account_rotation and bot.account_manager:
        bot.account_manager.print_account_status()
    
    print("\nDevam etmek istiyor musunuz? (e/h): ")
    
    confirm = input().lower().strip()
    if confirm not in ['e', 'evet', 'y', 'yes']:
        print("İşlem iptal edildi.")
        return
    
    # Bot'u çalıştır
    success = bot.run_bot(business_url, review_text, num_reviews, business_type, google_email, google_password)
    
    if success:
        print("\n✅ Bot başarıyla tamamlandı!")
    else:
        print("\n❌ Bot çalıştırılamadı!")

if __name__ == "__main__":
    main()
