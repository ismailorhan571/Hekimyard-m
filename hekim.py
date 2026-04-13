import streamlit as st
import google.generativeai as genai

# --- PROFESYONEL SAYFA AYARLARI ---
st.set_page_config(page_title="Med-AI Karar Destek", page_icon="🏥", layout="wide")

# Kurumsal Dahiliye Teması
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .report-card { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #d1d5db; margin-bottom: 20px; }
    .ai-response { background-color: #eef2ff; padding: 25px; border-radius: 10px; border-left: 5px solid #4f46e5; color: #1e1b4b; }
    .stButton>button { background-color: #059669; color: white; font-weight: bold; border-radius: 8px; width: 100%; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- AI BAĞLANTI AYARI (KRİTİK ÇÖZÜM) ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 404 hatasını önlemek için EN STABİL tanımlama
        model = genai.GenerativeModel('gemini-1.5-flash')
        AI_READY = True
    else:
        AI_READY = False
        st.error("API Key bulunamadı! Lütfen Secrets ayarlarını kontrol edin.")
except Exception as e:
    AI_READY = False
    st.error(f"Bağlantı Hatası: {str(e)}")

# --- ARAYÜZ ---
st.title("🏥 Klinik Karar Destek Sistemi")
st.write("Dahiliye Servisi Hekim Asistanı | **Geliştiren: İsmail Orhan**")
st.divider()

col_v, col_s = st.columns([1, 2], gap="large")

with col_v:
    st.markdown("### 📋 Hasta & Vitaller")
    with st.container(border=True):
        yas = st.number_input("Yaş", 0, 120, 45)
        cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
        ates = st.number_input("Ateş (°C)", 35.0, 42.0, 36.6, step=0.1)
        spo2 = st.slider("SpO2 (%)", 70, 100, 98)
        tansiyon = st.text_input("Tansiyon (TA)", "120/80")
        nabiz = st.number_input("Nabız", 30, 200, 80)

with col_s:
    st.markdown("### 🔍 Klinik Şikayetler")
    tabs = st.tabs(["Genel/Solunum", "Kardiyo/Gastro", "Nöroloji/Diğer"])
    
    with tabs[0]:
        c1, c2 = st.columns(2)
        genel = c1.multiselect("Sistemik", ["Halsizlik", "Kilo Kaybı", "Gece Terlemesi", "Yaygın Ağrı"])
        solunum = c2.multiselect("Solunum", ["Dispne", "Öksürük", "Hemoptizi", "Hışıltı"])
    with tabs[1]:
        c3, c4 = st.columns(2)
        kardiyo = c3.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Çarpıntı", "Ödem"])
        gastro = c4.multiselect("Gastrointestinal", ["Karın Ağrısı", "Bulantı/Kusma", "Melena", "Sarılık"])
    with tabs[2]:
        noro = st.multiselect("Diğer", ["Baş Ağrısı", "Bilinç Bulanıklığı", "Vertigo", "Eklem Ağrısı"])

    secilen_semptomlar = genel + solunum + kardiyo + gastro + noro

    if st.button("ANALİZ RAPORUNU TAMAMLA"):
        if not secilen_semptomlar:
            st.warning("Lütfen en az bir semptom seçin.")
        else:
            with st.spinner("Klinik algoritma ve AI çalışıyor..."):
                # 1. ÖN DEĞERLENDİRME (SENİN İSTEDİĞİN DETAYLI YAPI)
                st.markdown("### 📑 Klinik Ön Değerlendirme")
                with st.container():
                    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
                    
                    if "Göğüs Ağrısı" in kardiyo:
                        st.write("🚩 **Olası Ön Tanı:** Akut Koroner Sendrom / Perikardit")
                        st.write("🧪 **Tetkik Önerisi:** Seri EKG, Troponin I/T, CK-MB, EKO.")
                    
                    if "Karın Ağrısı" in gastro:
                        st.write("🚩 **Olası Ön Tanı:** Akut Batın / Kolefistit / Pankreatit")
                        st.write("🧪 **Tetkik Önerisi:** Hemogram, CRP, Amilaz, Lipaz, Tüm Batın USG.")

                    if ates > 38:
                        st.write("🚩 **Olası Ön Tanı:** Enfeksiyon / Sepsis")
                        st.write("🧪 **Tetkik Önerisi:** Kan/İdrar Kültürü, Prokalsitonin, CRP, Akciğer Grafisi.")

                    if spo2 < 93:
                        st.error("⚠️ KRİTİK UYARI: Hipoksi! Arteriyel Kan Gazı ve Oksijen Desteği düşünülmelidir.")
                    
                    st.markdown("</div>", unsafe_allow_html=True)

                # 2. YAPAY ZEKA GÖRÜŞÜ
                st.divider()
                st.markdown("### 🤖 Yapay Zeka (Gemini) Detaylı Analizi")
                if AI_READY:
                    # Hatasız prompt yapısı
                    prompt = (
                        f"Sen profesyonel bir hekim asistanısın. "
                        f"Hasta: {yas} yaşında {cinsiyet}. "
                        f"Vitaller: Ateş {ates}, SpO2 %{spo2}, TA {tansiyon}, Nabız {nabiz}. "
                        f"Semptomlar: {', '.join(secilen_semptomlar)}. "
                        f"Lütfen şunları detaylandır: 1. Ayırıcı tanılar. 2. İstenecek laboratuvar ve görüntüleme testleri. "
                        f"3- İzlenmesi gereken kritik bulgular."
                    )
                    try:
                        response = model.generate_content(prompt)
                        st.markdown(f"<div class='ai-response'>{response.text}</div>", unsafe_allow_html=True)
                    except Exception as ai_e:
                        st.error(f"AI Analiz sırasında hata oluştu: {str(ai_e)}")
                else:
                    st.warning("AI Entegrasyonu aktif değil.")

st.divider()
st.caption("Med-AI v3.0 Pro | Geliştirici: İsmail Orhan © 2026")
