import streamlit as st
import google.generativeai as genai
import time

# --- GÜVENLİK VE YAPAY ZEKA AYARLARI ---
# Hata almamak için model ismini ve konfigürasyonu optimize ettik.
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # En güncel ve stabil model ismini kullanıyoruz.
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_AVAILABLE = True
except Exception as e:
    AI_AVAILABLE = False
    AI_ERROR = str(e)

# 1. SAYFA KONFİGÜRASYONU
st.set_page_config(page_title="Med-AI Karar Destek", page_icon="🏥", layout="wide")

# PROFESYONEL CSS: Modern Hastane Yazılımı Arayüzü
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f0f2f6; }
    
    /* Kart Yapıları */
    .med-card {
        background-color: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e1e4e8; margin-bottom: 20px;
    }
    
    /* Buton Tasarımı */
    .stButton>button {
        width: 100%; background: linear-gradient(135deg, #0062ff 0%, #0045b5 100%);
        color: white; border-radius: 10px; border: none; height: 3.5em;
        font-weight: 700; font-size: 16px; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,98,255,0.3); }
    
    /* Başlıklar */
    h1 { color: #1a202c; font-weight: 800; letter-spacing: -1px; }
    .section-title { color: #2d3748; font-weight: 700; border-left: 5px solid #0062ff; padding-left: 15px; margin-bottom: 20px; }
    
    /* Yapay Zeka Yanıt Alanı */
    .ai-report {
        background-color: #ffffff; border-left: 6px solid #10b981;
        padding: 30px; border-radius: 12px; line-height: 1.6;
        box-shadow: 0 10px 25px rgba(16,185,129,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<h1>🏥 Klinik Karar Destek Sistemi <span style='font-size: 0.4em; vertical-align: middle; color: #718096;'>v2.0 PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #4a5568;'>Geliştiren: <b>İsmail Orhan</b> | Klinik Analiz ve Teşhis Destek Modülü</p>", unsafe_allow_html=True)

st.divider()

# 3. YAN PANEL: HASTA VİTALLERİ
with st.sidebar:
    st.markdown("### 👤 Hasta Profili")
    yas = st.number_input("Hasta Yaşı", 0, 120, 30)
    cinsiyet = st.selectbox("Cinsiyet", ["Belirtilmemiş", "Erkek", "Kadın"])
    
    st.markdown("### 🫀 Vital Parametreler")
    ates = st.number_input("Ateş (°C)", 34.0, 42.0, 36.6, step=0.1)
    ta = st.text_input("Tansiyon (Örn: 120/80)", "120/80")
    nabiz = st.number_input("Nabız (atım/dk)", 30, 220, 80)
    spo2 = st.slider("SpO2 (%)", 70, 100, 98)
    
    st.info("💡 Vitallerdeki sapmalar, AI tarafından 'Kırmızı Bayrak' olarak değerlendirilir.")

# 4. ANA PANEL: SEMPTOM GRUPLARI
st.markdown("<div class='section-title'>🔍 Klinik Semptom ve Bulgular</div>", unsafe_allow_html=True)

with st.container():
    col_sym1, col_sym2 = st.columns(2)
    
    with col_sym1:
        sistemik = st.multiselect("🚩 Sistemik & Enfeksiyon", 
            ["Yüksek Ateş", "Halsizlik", "Kilo Kaybı", "Lenfadenopati", "Gece Terlemesi", "Yaygın Ağrı"])
        solunum = st.multiselect("🫁 Solunum Sistemi", 
            ["Dispne (Nefes Darlığı)", "Öksürük (Kuru)", "Öksürük (Prodüktif)", "Hemoptizi", "Wheezing", "Plöretik Ağrı"])
        noro = st.multiselect("🧠 Nörolojik Bulgular", 
            ["Bilinç Bulanıklığı", "Fokal Defisit", "Şiddetli Baş Ağrısı", "Vertigo", "Konfüzyon", "Ataksi"])
            
    with col_sym2:
        kardiyo = st.multiselect("🫀 Kardiyovasküler", 
            ["Tipik Göğüs Ağrısı", "Atipik Göğüs Ağrısı", "Çarpıntı", "Senkop", "Ortopne", "Periferik Ödem"])
        gastro = st.multiselect("🧪 Gastrointestinal", 
            ["Akut Karın", "Bulantı/Kusma", "Melena", "Hematemez", "İshal", "Sarılık", "Asit"])
        diger = st.multiselect("🧬 Diğer Bulgular", 
            ["Dizüri", "Hematüri", "Flank Ağrı", "Döküntü", "Eklem Şişliği"])

all_symptoms = sistemik + solunum + noro + kardiyo + gastro + diger

# 5. ANALİZ MOTORU
def generate_medical_report(symptoms, vitals):
    prompt = f"""
    Sen uzman bir klinik hekim danışmanısın. Aşağıdaki hasta verilerini analiz et:
    - Yaş: {yas}, Cinsiyet: {cinsiyet}
    - Vitaller: Ateş: {ates}, TA: {ta}, Nabız: {nabiz}, SpO2: %{spo2}
    - Bulgular: {', '.join(symptoms)}
    
    Lütfen şu formatta bir tıbbi rapor oluştur:
    # 1. ÖNCELİKLİ ÖN TANILAR
    (En olası 3 tanıyı patofizyolojik gerekçeleriyle açıkla)
    
    # 2. ACİL TETKİK PLANI
    - Laboratuvar: (Biyokimya, Hemogram ve Spesifik markerlar)
    - Görüntüleme: (Radyolojik öncelikler)
    
    # 3. KLİNİK UYARI (RED FLAGS)
    (Hayati risk durumlarını ve atlanmaması gerekenleri belirt)
    
    Tıbbi terminolojiye sadık kal, ancak okunabilir bir yapı sun.
    """
    response = model.generate_content(prompt)
    return response.text

# 6. SONUÇ EKRANI
if st.button("Kapsamlı Analizi Başlat"):
    if not all_symptoms:
        st.error("Lütfen analiz için en az bir bulgu seçiniz.")
    else:
        with st.spinner("Yapay Zeka tıbbi verileri işliyor..."):
            st.divider()
            
            # Kritik Durum Kontrolü (Statik)
            if spo2 < 93 or ates > 39:
                st.error("🚨 KRİTİK UYARI: Hasta vitalleri stabil değil. Acil müdahale gerekebilir.")
            
            if AI_AVAILABLE:
                report = generate_medical_report(all_symptoms, {"yas": yas})
                st.markdown("<div class='section-title'>🤖 Yapay Zeka Klinik Raporu</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='ai-report'>{report}</div>", unsafe_allow_html=True)
            else:
                st.error(f"Sistem Hatası: {AI_ERROR}. Lütfen API Key ve Kütüphane versiyonunu kontrol edin.")

st.markdown("<p style='text-align: center; color: #718096; margin-top: 50px;'>© 2026 Med-AI Systems | Güvenli ve Profesyonel Klinik Destek</p>", unsafe_allow_html=True)
