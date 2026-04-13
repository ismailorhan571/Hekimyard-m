import streamlit as st
import google.generativeai as genai

# --- PROFESYONEL ARAYÜZ AYARLARI ---
st.set_page_config(page_title="Med-AI Pro Karar Destek", page_icon="🏥", layout="wide")

# Kurumsal Tıbbi Tema CSS
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stApp { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    .medical-card {
        background-color: white; padding: 20px; border-radius: 12px;
        border: 1px solid #e0e6ed; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0052cc 0%, #003d99 100%);
        color: white; border-radius: 8px; font-weight: 600; height: 3.5em; border: none;
    }
    .ai-report-container {
        background-color: #ffffff; border-left: 8px solid #0052cc;
        padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .critical-header { color: #d32f2f; font-weight: bold; border-bottom: 2px solid #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

# --- AI MODÜLÜ (404 HATASI ÇÖZÜMÜ) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # 404 hatasını önlemek için en güncel model ismi
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_STATUS = "Aktif"
except Exception as e:
    AI_STATUS = f"Hata: {str(e)}"

# ÜST BİLGİ BARI
st.markdown("<h1 style='color: #003d99; margin-bottom: 0;'>🏥 MED-AI KLİNİK ANALİZ PRO</h1>", unsafe_allow_html=True)
st.write(f"Sistem Durumu: **{AI_STATUS}** | Geliştirici: **İsmail Orhan**")
st.divider()

# ANA PANEL
col_side, col_main = st.columns([1, 3])

with col_side:
    st.markdown("### 📋 Hasta & Vital")
    with st.container(border=True):
        yas = st.number_input("Yaş", 0, 120, 45)
        cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtilmemiş"])
        ates = st.number_input("Ateş (°C)", 35.0, 42.0, 36.6)
        spo2 = st.slider("SpO2 (%)", 70, 100, 98)
        nabiz = st.number_input("Nabız", 30, 200, 80)
        tansiyon = st.text_input("TA (Örn: 120/80)", "120/80")

with col_main:
    st.markdown("### 🔍 Klinik Semptom Seçimi")
    
    # Semptomları sistemlere göre gruplandırdık (Daha Pro Görünüm)
    s_tabs = st.tabs(["Genel/Enfeksiyon", "Kardiyo/Solunum", "Gastro/Genital", "Nöroloji"])
    
    with s_tabs[0]:
        c1, c2 = st.columns(2)
        sym_genel = c1.multiselect("Genel", ["Halsizlik", "Kilo Kaybı", "Gece Terlemesi", "Yaygın Ağrı"])
        sym_enf = c2.multiselect("Enfeksiyon", ["Yüksek Ateş", "Üşüme-Titreme", "Lenfadenopati"])
        
    with s_tabs[1]:
        c3, c4 = st.columns(2)
        sym_kardiyo = c3.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Çarpıntı", "Ödem", "Senkop"])
        sym_solunum = c4.multiselect("Solunum", ["Nefes Darlığı", "Öksürük", "Hemoptizi", "Hışıltı"])

    with s_tabs[2]:
        c5, c6 = st.columns(2)
        sym_gastro = c5.multiselect("Gastrointestinal", ["Karın Ağrısı", "Bulantı/Kusma", "Melena", "Sarılık"])
        sym_uriner = c6.multiselect("Üriner/Genital", ["Dizüri", "Hematüri", "Yan Ağrısı"])

    with s_tabs[3]:
        sym_noro = st.multiselect("Nörolojik", ["Baş Ağrısı", "Bilinç Bulanıklığı", "Baş Dönmesi", "Güç Kaybı"])

    all_sym = sym_genel + sym_enf + sym_kardiyo + sym_solunum + sym_gastro + sym_uriner + sym_noro

    if st.button("📊 KLİNİK ANALİZİ VE TANILARI OLUŞTUR"):
        if not all_sym:
            st.error("Lütfen en az bir semptom seçiniz.")
        elif "Hata" in AI_STATUS:
            st.error(f"Yapay zeka bağlantı hatası: {AI_STATUS}. Lütfen Secrets ayarlarını kontrol edin.")
        else:
            with st.spinner("AI Tıbbi Literatürü Analiz Ediyor..."):
                prompt = f"""
                Sen bir kıdemli tıp doktoru asistanısın.
                HASTA: Yaş {yas}, {cinsiyet}.
                VİTALLER: Ateş {ates}, SpO2 %{spo2}, Nabız {nabiz}, TA {tansiyon}.
                SEMPTOMLAR: {', '.join(all_sym)}.
                
                Lütfen bu verilerle profesyonel bir rapor oluştur:
                1. ÖNCELİKLİ AYIRICI TANILAR (Gerekçeleriyle)
                2. İSTENMESİ GEREKEN KAN PARAMETRELERİ (Spesifik markerlar dahil)
                3. ÖNERİLEN GÖRÜNTÜLEME VE İLERİ TETKİKLER
                4. KRİTİK UYARILAR (Red Flags)
                
                Tıp dili kullan ve her bölümü net başlıklarla ayır.
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown("<div class='ai-report-container'>", unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"İşlem sırasında bir hata oluştu: {str(e)}")

st.divider()
st.caption("© 2026 Med-AI Karar Destek Sistemleri | Bu uygulama bir tavsiye aracıdır, kesin tanı hekim sorumluluğundadır.")
