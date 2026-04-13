import streamlit as st
import google.generativeai as genai
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Klinik Karar Destek Sistemi",
    page_icon="⚕️",
    layout="wide"
)

# --- GEMINI API ENTEGRASYONU ---
# API Anahtarını Streamlit Secrets'tan alıyoruz (Local'de çalışırken os.getenv kullanabilirsin)
API_KEY = st.secrets.get("GEMINI_API_KEY") 

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro') # Tıbbi analiz için Pro modeli daha iyidir
else:
    st.error("Lütfen API anahtarınızı Streamlit Secrets içine 'GEMINI_API_KEY' adıyla ekleyin.")

# --- SIDEBAR (YAN PANEL) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2785/2785482.png", width=100)
    st.title("Sistem Bilgileri")
    st.info("""
    Bu uygulama, hekimlerin tanı ve tetkik süreçlerine yardımcı olmak amacıyla geliştirilmiş bir **Karar Destek Sistemi**dir.
    """)
    st.divider()
    st.write("### Geliştirici")
    st.success("**İSMAİL ORHAN**")
    st.write("[GitHub Profilim](https://github.com/ismailorhan)") # Buraya kendi linkini ekle

# --- ANA ARAYÜZ ---
st.title("⚕️ Akıllı Tanı ve Tetkik Asistanı")
st.markdown("---")

# Giriş Alanları: İki sütunlu yapı
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Hasta Temel Bilgileri")
    yas = st.number_input("Yaş", min_value=0, max_value=120, step=1)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtilmemiş"])
    sikayet = st.text_area("Ana Şikayet ve Öykü", height=150, 
                          placeholder="Örn: 3 gündür devam eden sağ alt kadran ağrısı, bulantı ve iştahsızlık...")

with col2:
    st.subheader("🔍 Muayene ve Özgeçmiş")
    fizik_muayene = st.text_area("Fizik Muayene Bulguları", height=100, 
                               placeholder="Örn: Rebound (+) pozitif, defans mevcut, ateş 38.5...")
    ozgecmis = st.text_area("Özgeçmiş ve Ek Hastalıklar", height=100, 
                           placeholder="Örn: Bilinen DM ve HT mevcut. Daha önce kolesistektomi geçirmiş.")

# --- ANALİZ MANTIĞI ---
if st.button("Vakayı Analiz Et ve Görüş Al"):
    if not sikayet:
        st.warning("Lütfen analiz için en azından ana şikayeti giriniz.")
    else:
        with st.spinner('Gemini vaka üzerinde çalışıyor...'):
            # Gemini'ye gönderilecek 'Prompt' tasarımı
            prompt = f"""
            Sen uzman bir tıp doktoru asistanısın. Aşağıdaki hasta verilerini analiz et:
            
            HASTA VERİLERİ:
            - Yaş/Cinsiyet: {yas} / {cinsiyet}
            - Ana Şikayet: {sikayet}
            - Fizik Muayene: {fizik_muayene}
            - Özgeçmiş: {ozgecmis}
            
            Lütfen şu başlıklarla profesyonel bir rapor sun:
            1. Olası Ön Tanılar (Diferansiyel Tanı)
            2. İstenmesi Gereken Öncelikli Tetkikler (Laboratuvar ve Görüntüleme)
            3. Ayırıcı Tanı İçin Kritik Sorular
            4. Tedavi Yaklaşımı Önerisi (Genel Bilgilendirme Amaçlı)
            
            Not: Yanıtın sonuna 'Bu bir asistan görüşüdür, kesin tanı doktor kontrolündedir' notunu ekle.
            """
            
            try:
                response = model.generate_content(prompt)
                
                st.markdown("### 🧬 Gemini Klinik Değerlendirme")
                st.light_blue_area = st.info(response.text)
                
                # Çıktıyı PDF veya metin olarak kaydetme seçeneği (Opsiyonel)
                st.download_button("Raporu İndir", response.text, file_name="klinik_rapor.txt")
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption(f"© 2026 | Geliştirici: İSMAİL ORHAN | Streamlit & Gemini Pro Entegrasyonu")
