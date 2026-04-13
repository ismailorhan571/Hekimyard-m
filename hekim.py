import streamlit as st
import google.generativeai as genai

# --- PROFESYONEL SAYFA AYARLARI ---
st.set_page_config(page_title="Med-AI Karar Destek", page_icon="⚕️", layout="wide")

# Kurumsal ve Temiz Arayüz (Galatasaray Renklerine Küçük Göndermeli Ama Sade)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #d32f2f; color: white; border-radius: 8px; font-weight: bold; }
    .diagnosis-card { padding: 20px; border-radius: 12px; background-color: white; border-left: 6px solid #ffca28; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .ai-card { padding: 25px; border-radius: 12px; background-color: #fff9e6; border: 1px solid #ffe082; color: #333; }
    .critical-alert { background-color: #ffebee; color: #c62828; padding: 15px; border-radius: 8px; border: 1px solid #ffcdd2; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- AI MODÜLÜ YAPILANDIRMASI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Hata almamak için model ismini en yalın haliyle kullanıyoruz
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_STATUS = True
except Exception as e:
    AI_STATUS = False
    AI_ERR = str(e)

# --- ÜST PANEL ---
st.title("🏥 Klinik Karar Destek Paneli")
st.write("Dahiliye Servisi Hekim Yardımcı Yazılımı | **Geliştirici: İsmail Orhan**")
st.divider()

# --- PANEL YAPISI ---
col_sidebar, col_content = st.columns([1, 3], gap="large")

with col_sidebar:
    st.header("📋 Hasta Bilgileri")
    with st.container(border=True):
        yas = st.number_input("Yaş", 0, 120, 45)
        cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
        ates = st.number_input("Ateş (°C)", 35.0, 42.0, 36.6, step=0.1)
        spo2 = st.slider("SpO2 (%)", 70, 100, 98)
        nabiz = st.number_input("Nabız (atım/dk)", 30, 220, 80)
        ta = st.text_input("Tansiyon (TA)", "120/80")

with col_content:
    st.subheader("🔍 Klinik Bulgular ve Semptomlar")
    
    t1, t2, t3, t4 = st.tabs(["Genel & Enfeksiyon", "Kardiyo & Solunum", "Gastro & Üro", "Nöro & Diğer"])
    
    with t1:
        c1, c2 = st.columns(2)
        sym_genel = c1.multiselect("Sistemik", ["Halsizlik", "Kilo Kaybı", "Gece Terlemesi", "Yaygın Ağrı"])
        sym_enf = c2.multiselect("Enfeksiyon", ["Yüksek Ateş", "Üşüme-Titreme", "Lenfadenopati", "Döküntü"])
        
    with t2:
        c3, c4 = st.columns(2)
        sym_kardiyo = c3.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Çarpıntı", "Ödem", "Ortopne"])
        sym_solunum = c4.multiselect("Solunum", ["Nefes Darlığı", "Öksürük", "Hemoptizi", "Hışıltı"])

    with t3:
        c5, c6 = st.columns(2)
        sym_gastro = c5.multiselect("Gastrointestinal", ["Karın Ağrısı", "Bulantı/Kusma", "Melena", "Sarılık"])
        sym_uriner = c6.multiselect("Üriner", ["Dizüri", "Hematüri", "Yan Ağrısı", "Sık İdrar"])

    with t4:
        sym_noro = st.multiselect("Nöroloji/Diğer", ["Baş Ağrısı", "Bilinç Bulanıklığı", "Vertigo", "Eklem Ağrısı"])

    all_symptoms = sym_genel + sym_enf + sym_kardiyo + sym_solunum + sym_gastro + sym_uriner + sym_noro

    if st.button("📊 KLİNİK ANALİZİ BAŞLAT"):
        if not all_symptoms:
            st.error("Lütfen analiz için en az bir bulgu seçiniz.")
        else:
            with st.spinner("Analiz ediliyor..."):
                # 1. ÖN DEĞERLENDİRME (STATİK MANTIK)
                st.markdown("### 📑 Klinik Ön Değerlendirme ve Tetkikler")
                
                with st.container():
                    # KRİTİK UYARI
                    if spo2 < 92:
                        st.markdown("<div class='critical-alert'>🚨 ACİL: Hipoksi Saptandı! Oksijen desteği ve AKG düşünülmelidir.</div>", unsafe_allow_html=True)
                    
                    st.markdown("<div class='diagnosis-card'>", unsafe_allow_html=True)
                    
                    if "Göğüs Ağrısı" in sym_kardiyo:
                        st.write("🚩 **Ön Tanı:** Akut Koroner Sendrom?")
                        st.write("🧪 **Tetkikler:** Seri EKG, Troponin, CK-MB, EKO.")
                        
                    if "Karın Ağrısı" in sym_gastro and "Bulantı/Kusma" in sym_gastro:
                        st.write("🚩 **Ön Tanı:** Akut Batın / Pankreatit?")
                        st.write("🧪 **Tetkikler:** Hemogram, Amilaz, Lipaz, Ayakta Direkt Batın Grafisi (ADBG).")
                        
                    if ates > 38 and "Halsizlik" in sym_genel:
                        st.write("🚩 **Ön Tanı:** Enfeksiyon / Sepsis?")
                        st.write("🧪 **Tetkikler:** CRP, Prokalsitonin, Kan/İdrar Kültürü, Akciğer Grafisi.")

                    if not any(x in all_symptoms for x in ["Göğüs Ağrısı", "Karın Ağrısı"]):
                        st.write("✅ Mevcut bulgular üzerinden spesifik ön tanıları aşağıda AI detaylandıracaktır.")
                    
                    st.markdown("</div>", unsafe_allow_html=True)

                # 2. YAPAY ZEKA GÖRÜŞÜ
                st.divider()
                st.subheader("🤖 Yapay Zeka (Gemini) Detaylı Analizi")
                
                if AI_STATUS:
                    # Syntax hatasını önlemek için promptu temizledik
                    prompt_text = (
                        f"Sen deneyimli bir tıp doktoru asistanısın. "
                        f"Hasta: {yas} yaşında {cinsiyet}. "
                        f"Vitaller: Ateş {ates}, Nabız {nabiz}, SpO2 %{spo2}, TA {ta}. "
                        f"Semptomlar: {', '.join(all_symptoms)}. "
                        f"Lütfen şunları açıkla: 1. En olası 3 ayırıcı tanı ve nedenleri. "
                        f"2. İstenmesi gereken spesifik laboratuvar ve görüntüleme tetkikleri. "
                        f"3. Takipte dikkat edilmesi gereken kırmızı bayraklar."
                    )
                    
                    try:
                        response = model.generate_content(prompt_text)
                        st.markdown(f"<div class='ai-card'>{response.text}</div>", unsafe_allow_html=True)
                    except Exception as ai_e:
                        st.error(f"AI Analiz Hatası: {str(ai_e)}")
                else:
                    st.error(f"Yapay Zeka bağlantısı kurulamadı: {AI_ERR}")

st.divider()
st.caption("© 2026 Med-AI Karar Destek Sistemi | İsmail Orhan")
