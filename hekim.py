import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Klinik Karar Destek", layout="wide")

API_KEY = st.secrets.get("GEMINI_API_KEY") 

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        # 'latest' takısı genellikle 404 hatalarını çözer
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
    except Exception as e:
        st.error(f"Yapılandırma Hatası: {e}")
else:
    st.error("API Anahtarı bulunamadı!")

st.title("⚕️ Akıllı Tanı Asistanı")
st.divider()

# Basit girişler
sikayet = st.text_area("Vaka Detayları")

if st.button("Analiz Et"):
    if sikayet:
        with st.spinner('Analiz ediliyor...'):
            try:
                # Test amaçlı çok kısa bir prompt
                response = model.generate_content(f"Bir doktor asistanı olarak şu vakayı yorumla: {sikayet}")
                st.write(response.text)
            except Exception as e:
                st.error(f"Hata Detayı: {e}")
                st.info("Eğer hala 404 alıyorsan, Google AI Studio'dan yeni bir API anahtarı almayı dene, bazen anahtarın bağlı olduğu proje eski kalabiliyor.")

st.sidebar.write("Geliştirici: **İSMAİL ORHAN**")
