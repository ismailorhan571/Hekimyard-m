import streamlit as st
import google.generativeai as genai

# --- PROFESYONEL SAYFA AYARLARI ---
st.set_page_config(page_title="Med-AI Karar Destek", page_icon="⚕️", layout="wide")

# Kurumsal Tıbbi Arayüz Tasarımı (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stApp { font-family: 'Inter', sans-serif; }
    /* Kart Yapıları */
    .med-container {
        background-color: white; padding: 2rem; border-radius: 12px;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    /* Profesyonel Buton */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        color: white; border: none; padding: 0.75rem 1.5rem;
        border-radius: 8px; font-weight: 600; width: 100%; transition: all 0.2s;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(37,99,235,0.2); }
    /* Rapor Alanı */
    .ai-report {
        background-color: #ffffff; border-left: 6px solid #2563eb;
        padding: 2rem; border-radius: 8px; margin-top: 2rem;
        font-size: 1.1rem; line-height: 1.6; color: #1e293b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AI BAĞLANTISI (Hata Yakalama Geliştirildi) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # 404 hatası için tam yol kullanıyoruz: models/gemini-1.5-flash
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
    AI_READY = True
except Exception as e:
    AI_READY = False
    AI_ERROR = str(e)

# --- ÜST PANEL ---
st.markdown("<h1 style='color: #1e3a8a; margin-bottom: 0;'>⚕️ MED-AI KLİNİK DESTEK SİSTEMİ</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b;'>Profesyonel Tanı ve Analiz Modülü | v2.1 PRO</p>", unsafe_allow_html=True)
st.divider()

# --- ANA ARAYÜZ ---
col_side, col_main = st.columns([1, 2.5], gap="large")

with col_side:
    st.markdown("### 📋 Hasta Parametreleri")
    with st.container(border=True):
        yas = st.number_input("Yaş", 0, 120, 30)
        cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Diğer"])
        st.divider()
        st.markdown("**🩸 Vital Bulgular**")
        ates = st.number_input("Ateş (°C)", 34.0, 42.0, 36.6, step=0.1)
        nabiz = st.number_input("Nabız (bpm)", 30, 220, 80)
        spo2 = st.slider("SpO2 (%)", 70, 100, 98)
        ta = st.text_input("Tansiyon", "120/80")

with col_main:
    st.markdown("### 🔍 Klinik Semptom Grupları")
    
    # Sistemlere göre ayırarak daha "PRO" bir görünüm sağlıyoruz
    t1, t2, t3 = st.tabs(["Genel & Solunum", "Kardiyo & Gastro", "Nöro & Diğer"])
    
    with t1:
        s1, s2 = st.columns(2)
        genel = s1.multiselect("Sistemik", ["Halsizlik", "Kilo Kaybı", "Ateş", "Lenfadenopati"])
        solunum = s2.multiselect("Solunum", ["Dispne", "Öksürük", "Hemoptizi", "Wheezing"])
    
    with t2:
        s3, s4 = st.columns(2)
        kardiyo = s3.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Çarpıntı", "Ödem", "Ortopne"])
        gastro = s4.multiselect("Sindirim", ["Karın Ağrısı", "Bulantı/Kusma", "Melena", "Sarılık"])
        
    with t3:
        noro = st.multiselect("Nörolojik", ["Şiddetli Baş Ağrısı", "Bilinç Bulanıklığı", "Vertigo", "Parestezi"])
        ek = st.multiselect("Ek Şikayetler", ["Dizüri", "Hematüri", "Döküntü", "Eklem Ağrısı"])

    secilenler = genel + solunum + kardiyo + gastro + noro + ek

    if st.button("ANALİZ RAPORUNU OLUŞTUR"):
        if not secilenler:
            st.warning("Lütfen analiz için en az bir semptom seçiniz.")
        elif not AI_READY:
            st.error(f"Yapay Zeka Bağlantı Hatası: {AI_ERROR}")
        else:
            with st.spinner("Tıbbi literatür taranıyor ve analiz ediliyor..."):
                prompt = f"""
                Sen uzman bir hekim danışmanısın.
                HASTA VERİLERİ: Yaş {yas}, {cinsiyet}.
                VİTALLER: Ateş {ates}, Nabız {nabiz}, SpO2 %{spo2}, TA {ta}.
                BELİRTİLER: {', '.join(secilenler)}.
                
                Lütfen şu formatta profesyonel bir rapor hazırla:
                # 🩺 OLASI ÖN TANILAR
                (Nedenleriyle birlikte en az 3 ayırıcı tanı)
                
                # 🧪 İLERİ TETKİK ÖNERİLERİ
                (Kan tahlilleri ve görüntüleme yöntemleri)
                
                # ⚠️ KRİTİK UYARILAR (RED FLAGS)
                (Acil müdahale gerektiren durumlar)
                
                Tıp diline uygun, net ve akademik bir üslup kullan.
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown("<div class='ai-report'>", unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Rapor oluşturulurken bir hata oluştu: {str(e)}")

st.divider()
st.caption(f"Geliştirici: İsmail Orhan | Med-AI Karar Destek Sistemi © 2026")
