import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Klinik Karar Destek Sistemi",
    page_icon="⚕️",
    layout="wide"
)

# --- GEMINI API ENTEGRASYONU ---
# Streamlit Secrets üzerinden API anahtarını alıyoruz
# Not: Localde çalışırken secrets.toml dosyasına veya kodun içine geçici olarak yazabilirsin.
API_KEY = st.secrets.get("GEMINI_API_KEY") 

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        # Hatanın çözümü için en stabil model olan flash kullanıldı
        model = genai.GenerativeModel('gemini-1.5-flash') 
    except Exception as e:
        st.error(f"API Yapılandırma Hatası: {e}")
else:
    st.error("Lütfen API anahtarınızı Streamlit Secrets içine 'GEMINI_API_KEY' adıyla ekleyin.")

# --- SIDEBAR (YAN PANEL) ---
with st.sidebar:
    st.title("Sistem Bilgileri")
    st.info("Bu uygulama hekimler için bir klinik karar destek asistanıdır.")
    st.divider()
    st.write("### Geliştirici")
    st.success("**İSMAİL ORHAN**")
    st.markdown("[GitHub Profilim](https://github.com/ismailorhan)")

# --- ANA ARAYÜZ ---
st.title("⚕️ Akıllı Tanı ve Tetkik Asistanı")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Hasta Bilgileri")
    yas = st.number_input("Yaş", min_value=0, max_value=120, value=25)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    sikayet = st.text_area("Ana Şikayet ve Öykü", height=150, 
                          placeholder="Örn: 2 gündür süren yaygın karın ağrısı...")

with col2:
    st.subheader("🔍 Muayene ve Geçmiş")
    fizik_muayene = st.text_area("Fizik Muayene Bulguları", height=100, 
                               placeholder="Örn: Ateş 38.2, batın rahat...")
    ozgecmis = st.text_area("Özgeçmiş", height=100, 
                           placeholder="Örn: Bilinen bir hastalık yok...")

# --- ANALİZ BUTONU ---
if st.button("Vakayı Analiz Et"):
    if not sikayet:
        st.warning("Lütfen analiz için bir şikayet girin.")
    elif not API_KEY:
        st.error("API Anahtarı bulunamadı!")
    else:
        with st.spinner('Gemini analiz ediyor...'):
            prompt = f"""
            Sen uzman bir klinik asistansın. Aşağıdaki verileri değerlendir:
            
            VAKA:
            - Yaş/Cinsiyet: {yas} / {cinsiyet}
            - Şikayet: {sikayet}
            - Muayene: {fizik_muayene}
            - Özgeçmiş: {ozgecmis}
            
            LÜTFEN ŞU BAŞLIKLARLA YANITLA:
            1. Olası Ön Tanılar
            2. İstenmesi Gereken Tetkikler (Lab/Görüntüleme)
            3. Kritik Uyarılar
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🧬 Klinik Değerlendirme")
                st.write(response.text)
            except Exception as e:
                st.error(f"Analiz sırasında bir hata oluştu: {e}")
                st.info("Hata kodu 404 ise lütfen model adının doğruluğunu veya API anahtarının yetkisini kontrol edin.")

# --- FOOTER ---
st.markdown("---")
st.caption(f"© 2026 | Geliştirici: İSMAİL ORHAN | Klinik Karar Destek Sistemi")
