import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as gloss

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Med-AI Karar Destek", page_icon="🏥", layout="wide")

# CSS: İsmail Stili Pro Dokunuşu (Sade ve Kurumsal)
st.markdown("""
    <style>
    .report-box { padding: 20px; border-radius: 10px; background-color: #ffffff; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    .ai-box { padding: 25px; border-radius: 12px; background-color: #f0f7ff; border-left: 6px solid #1e40af; }
    .stButton>button { background: #1e40af; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- ENTEGRASYON ÇÖZÜMÜ ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # 404 HATASINI ÇÖZEN KRİTİK TANIMLAMA
    # 'models/' ön eki olmadan ve versiyon belirterek çağırıyoruz
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config={"temperature": 0.3}
    )
    AI_READY = True
except Exception as e:
    AI_READY = False
    AI_ERR = str(e)

# --- ARAYÜZ ---
st.title("🏥 Klinik Karar Destek Sistemi")
st.write("İsmail Orhan | Dahiliye Servisi Profesyonel Analiz Modülü")
st.divider()

col_vitals, col_sym = st.columns([1, 2.5])

with col_vitals:
    st.markdown("### 📋 Hasta & Vitaller")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    ates = st.number_input("Ateş (°C)", 35.0, 42.0, 36.6)
    spo2 = st.slider("SpO2 (%)", 70, 100, 98)
    tansiyon = st.text_input("Tansiyon", "120/80")
    nabiz = st.number_input("Nabız", 30, 220, 80)

with col_sym:
    st.markdown("### 🔍 Semptom Analizi")
    tabs = st.tabs(["Genel/Solunum", "Kardiyo/Gastro", "Nöro/Diğer"])
    
    with tabs[0]:
        genel = st.multiselect("Sistemik", ["Halsizlik", "Kilo Kaybı", "Yüksek Ateş", "Lenfadenopati"])
        solunum = st.multiselect("Solunum", ["Dispne", "Öksürük", "Hemoptizi", "Wheezing"])
    with tabs[1]:
        kardiyo = st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Çarpıntı", "Ödem"])
        gastro = st.multiselect("Gastrointestinal", ["Karın Ağrısı", "Bulantı/Kusma", "Melena", "Hematemez"])
    with tabs[2]:
        noro = st.multiselect("Diğer", ["Baş Ağrısı", "Bilinç Bulanıklığı", "Eklem Ağrısı", "Hematüri"])

    secilen = genel + solunum + kardiyo + gastro + noro

    if st.button("📊 KAPSAMLI ANALİZ RAPORU OLUŞTUR"):
        if not secilen:
            st.warning("Lütfen semptom seçiniz.")
        else:
            # 1. ÖN DEĞERLENDİRME VE TETKİKLER (STATİK)
            st.markdown("### 📑 Klinik Ön Değerlendirme")
            st.markdown("<div class='report-box'>", unsafe_allow_html=True)
            
            # Detaylı Ön Tanı Algoritması
            if "Göğüs Ağrısı" in kardiyo:
                st.write("🚩 **Olası Tanı:** Akut Koroner Sendrom / Perikardit")
                st.write("🧪 **Tetkik:** EKG (Seri), Troponin I/T, CK-MB, EKO, Akciğer Grafisi.")
            
            if "Karın Ağrısı" in gastro:
                st.write("🚩 **Olası Tanı:** Akut Batın / Kolefistit / Pankreatit")
                st.write("🧪 **Tetkik:** Hemogram, CRP, Amilaz, Lipaz, USG-Tüm Batın, ADBG.")
                
            if "Nefes Darlığı" in solunum or spo2 < 93:
                st.write("🚩 **Olası Tanı:** Pnömoni / Pulmoner Emboli / KY Alevlenme")
                st.write("🧪 **Tetkik:** D-Dimer, AKG, Pro-BNP, Toraks BT.")

            if ates > 38:
                st.write("🚩 **Olası Tanı:** Enfeksiyon / Sepsis")
                st.write("🧪 **Tetkik:** Kan/İdrar Kültürü, Prokalsitonin, CRP.")
            
            st.markdown("</div>", unsafe_allow_html=True)

            # 2. YAPAY ZEKA GÖRÜŞÜ
            st.markdown("### 🤖 Yapay Zeka (Gemini) Uzman Analizi")
            if AI_READY:
                prompt = (
                    f"Bir hekim yardımcısı gibi davran. Hasta: {yas} yaşında {cinsiyet}. "
                    f"Vitaller: Ateş {ates}, SpO2 %{spo2}, TA {tansiyon}, Nabız {nabiz}. "
                    f"Semptomlar: {', '.join(secilen)}. "
                    f"Lütfen: 1- Ayırıcı tanıları detaylandır. 2- Spesifik laboratuvar ve görüntüleme önerilerini yaz. "
                    f"3- Klinik seyir için önerilerini ver."
                )
                try:
                    # Direk generate_content çağrısı (Entegre çözüm)
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='ai-box'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as ai_e:
                    st.error(f"Entegrasyon Hatası: {str(ai_e)}. Lütfen API sürümünü kontrol edin.")
            else:
                st.error(f"AI Başlatılamadı: {AI_ERR}")

st.divider()
st.caption("Geliştirici: İsmail Orhan | Med-AI v2.5 Entegre Sürüm")
