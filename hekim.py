import streamlit as st
import google.generativeai as genai
import time

# --- GÜVENLİK VE YAPAY ZEKA AYARLARI ---
# Streamlit Cloud üzerinde 'Settings > Secrets' kısmına GEMINI_API_KEY eklemeyi unutmayın.
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False

# 1. SAYFA KONFİGÜRASYONU (Profesyonel Temiz Tema)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .report-card { padding: 20px; border-radius: 12px; background-color: white; border: 1px solid #dee2e6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .ai-response { background-color: #f0f7ff; border-left: 5px solid #0d6efd; padding: 20px; border-radius: 0 10px 10px 0; color: #1e293b; }
    .critical-alert { background-color: #fff5f5; border: 1px solid #feb2b2; color: #c53030; padding: 15px; border-radius: 8px; font-weight: bold; }
    h1, h2, h3 { color: #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST BİLGİ VE LOGO
st.title("⚕️ Klinik Karar Destek ve Tanı Asistanı")
st.write("Profesyonel Hekim ve Sağlık Çalışanı Paneli | Veri Tabanı V1.0")
st.divider()

# 3. YAN PANEL: VİTAL BULGULAR
with st.sidebar:
    st.header("📋 Hasta Profili")
    yas = st.number_input("Yaş", 0, 120, 30)
    cinsiyet = st.selectbox("Cinsiyet", ["Belirtilmemiş", "Erkek", "Kadın"])
    
    st.header("🫀 Vital Bulgular")
    ates = st.number_input("Ateş (°C)", 34.0, 42.0, 36.6, step=0.1)
    ta_sistolik = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    nabiz = st.number_input("Nabız (/dk)", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)
    
    st.markdown("---")
    st.warning("⚠️ **Yasal Uyarı:** Bu yazılım bir tavsiye niteliğindedir. Kesin tanı ve tedavi planı hekim sorumluluğundadır.")

# 4. ANA PANEL: SİSTEMİK BELİRTİ SEÇİMİ
st.subheader("🔍 Klinik Semptom Grupları")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Genel & Enfeksiyon", "Kardiyoloji & Göğüs", "Gastrointestinal", "Nöroloji", "Nefroloji & Üroloji"
])

secilenler = []

with tab1:
    genel = st.multiselect("Semptomlar", ["Yüksek Ateş", "Üşüme-Titreme", "Gece Terlemesi", "Halsizlik", "Kilo Kaybı", "Lenfadenopati (Şişlik)", "Eklem Ağrısı", "Kas Ağrısı", "Döküntü"])
    secilenler.extend(genel)

with tab2:
    kardiyo = st.multiselect("Semptomlar ", ["Baskı Tarzı Göğüs Ağrısı", "Batıcı Göğüs Ağrısı", "Eforla Gelen Nefes Darlığı", "İstirahatte Nefes Darlığı", "Çarpıntı", "Öksürük", "Balgam (Pürülan)", "Hemoptizi (Kanlı Balgam)", "Wheezing (Hışıltı)"])
    secilenler.extend(kardiyo)

with tab3:
    gastro = st.multiselect("Semptomlar  ", ["Karın Ağrısı (Yaygın)", "Karın Ağrısı (Lokalize)", "Bulantı/Kusma", "İshal (Diyare)", "Kabızlık", "Sarılık", "Melena (Siyah Dışkı)", "Hematemez (Kanlı Kusma)", "Yutma Güçlüğü"])
    secilenler.extend(gastro)

with tab4:
    noro = st.multiselect("Semptomlar   ", ["Şiddetli Baş Ağrısı", "Bilinç Bulanıklığı", "Baş Dönmesi (Vertigo)", "Konuşma Bozukluğu", "Motor Kayıp (Güçsüzlük)", "Duyu Kaybı (Uyuşma)", "Ense Sertliği", "Nöbet"])
    secilenler.extend(noro)

with tab5:
    uriner = st.multiselect("Semptomlar    ", ["İdrarda Yanma", "Sık İdrara Çıkma", "İdrar Yapamama (Anüri)", "Yan Ağrısı (Flank Ağrı)", "Hematüri (Kanlı İdrar)", "Bacaklarda Şişlik (Ödem)"])
    secilenler.extend(uriner)

# 5. ANALİZ VE GEMINI ENTEGRASYONU
def gemini_analiz_yap(belirtiler, vitaller):
    prompt = f"""
    Sen uzman bir klinik hekim asistanısın. 
    Hekim tarafından girilen bulgular şunlardır:
    - Semptomlar: {', '.join(belirtiler)}
    - Vitaller: Yaş {vitaller['yas']}, Ateş {vitaller['ates']}, TA {vitaller['ta']}, Nabız {vitaller['nabiz']}, SpO2 %{vitaller['spo2']}.
    
    Lütfen şu yapıda detaylı bir rapor sun:
    1. AYIRICI TANI: En olası 3-4 tanıyı ve nedenlerini açıkla.
    2. TETKİK PLANI: İstenmesi gereken spesifik laboratuvar (örn: Hemogram, CRP, Troponin, D-Dimer, Kültür) ve görüntüleme (örn: USG, BT, MR) tetkikleri.
    3. KRİTİK UYARI: Varsa acil müdahale gerektiren durumları (Red Flags) belirt.
    Tıbbi terminoloji kullan ve profesyonel ol.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Yapay zeka analizine şu an ulaşılamıyor. Hata: {str(e)}"

# 6. ÇALIŞTIRMA BUTONU VE SONUÇLAR
if st.button("KLİNİK ANALİZİ BAŞLAT"):
    if not secilenler:
        st.error("Lütfen en az bir belirti seçiniz.")
    else:
        with st.spinner("Klinik algoritmalar çalıştırılıyor ve Gemini AI analiz yapıyor..."):
            vital_dict = {"yas": yas, "ates": ates, "ta": ta_sistolik, "nabiz": nabiz, "spo2": spo2}
            
            # Statik Uyarı Mekanizması (Kritik Durumlar)
            if spo2 < 92 or (ta_sistolik < 90 and ates > 38):
                st.markdown("<div class='critical-alert'>🚨 DİKKAT: Hasta instabil olabilir. Sepsis veya solunum yetmezliği açısından acil müdahale gerekebilir!</div>", unsafe_allow_html=True)
            
            st.divider()
            
            # AI Analiz Bölümü
            if AI_AVAILABLE:
                st.subheader("🤖 Yapay Zeka (Gemini) Detaylı Klinik Yorumu")
                ai_rapor = gemini_analiz_yap(secilenler, vital_dict)
                st.markdown(f"<div class='ai-response'>{ai_rapor}</div>", unsafe_allow_html=True)
            else:
                st.info("ℹ️ AI Entegrasyonu pasif. API Anahtarınızı 'Secrets' kısmına ekleyerek aktif edebilirsiniz.")

            st.divider()
            st.write("© 2026 Klinik Destek Yazılımı - Tüm hakları saklıdır.")
