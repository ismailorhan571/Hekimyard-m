import streamlit as st
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import json
from streamlit_mic_recorder import mic_recorder
import streamlit.components.v1 as components

# --- 1. PREMIUM UI ARCHITECTURE (İSMAİL ORHAN | V30 TITANIC-GENDER) ---
st.set_page_config(page_title="İSMAİL ORHAN DAHİLİYE ROBOTU", page_icon="💊", layout="wide")

# AI Yapılandırması
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Secrets'da 'GEMINI_API_KEY' bulunamadı!")

# === SESSION STATE BAŞLATMA (SESLİ DOLDURMA İÇİN) ===
if 'yas' not in st.session_state: st.session_state.yas = 45
if 'hb' not in st.session_state: st.session_state.hb = 14.0
if 'kre' not in st.session_state: st.session_state.kre = 1.1
if 'wbc' not in st.session_state: st.session_state.wbc = 8500
if 'plt' not in st.session_state: st.session_state.plt = 245000
if 'cinsiyet' not in st.session_state: st.session_state.cinsiyet = "Erkek"
if 'p_no' not in st.session_state: st.session_state.p_no = "İSMAİL-V30-FINAL"
if 'secili_bulgular' not in st.session_state: st.session_state.secili_bulgular = []

# --- SESLİ OKUMA (TTS) MODÜLÜ ---
def sesli_oku(metin):
    js_kod = f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{metin}');
        msg.lang = 'tr-TR';
        window.speechSynthesis.speak(msg);
        </script>
    """
    components.html(js_kod, height=0)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.98); padding: 40px; border-radius: 50px; text-align: center; margin-bottom: 40px;
        border-top: 20px solid #DC2626; border-bottom: 20px solid #DC2626; border-left: 12px solid #D4AF37; border-right: 12px solid #D4AF37;
        box-shadow: 0 60px 120px rgba(0,0,0,0.3);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 3.2rem; margin: 0; }
    .main-header p { color: #DC2626; font-size: 1.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 5px; margin-top: 15px; }

    .clinical-card { 
        background: #FFFFFF; padding: 50px; border-radius: 60px; margin-bottom: 40px;
        border-left: 35px solid #DC2626; border-right: 18px solid #D4AF37;
        box-shadow: 25px 25px 60px rgba(0,0,0,0.12);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 50px;
        height: 7em; width: 100%; font-weight: 800; font-size: 35px; border: 7px solid #DC2626;
    }
    .stButton>button:hover { background: #DC2626; transform: scale(1.01); color: white; }
    
    [data-testid="stSidebar"] { background-color: #F8F7EB; border-right: 15px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KLİNİK KARAR ROBOTU</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN </p></div>", unsafe_allow_html=True)

# 2. LABORATUVAR TERMİNALİ
with st.sidebar:
    st.markdown("### 🏛️ LABORATUVAR VERİ MERKEZİ")
    
    st.subheader("🎤 SESLİ ASİSTAN (OTO-DOLDUR)")
    audio = mic_recorder(start_prompt="Konuşarak Veri Gir", stop_prompt="Kaydı Bitir", key='voice_input')
    
    if audio:
        try:
            with st.spinner("Veriler ayıklanıyor..."):
                model_voice = genai.GenerativeModel('gemini-1.5-flash')
                voice_prompt = """
                Sesi dinle. İçindeki yaş, hb, kre, wbc, plt değerlerini ve semptomları (varsa) JSON olarak ver.
                Format: {"yas": sayı, "hb": sayı, "kre": sayı, "wbc": sayı, "plt": sayı, "cinsiyet": "Erkek/Kadın", "semptomlar": ["bulgu1", "bulgu2"]}
                Sadece JSON ver.
                """
                response = model_voice.generate_content([voice_prompt, {"mime_type": "audio/wav", "data": audio['bytes']}])
                extracted_data = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
                for k, v in extracted_data.items():
                    if k in st.session_state: st.session_state[k] = v
                st.success("Veriler başarıyla yerleştirildi!")
                st.rerun()
        except:
            st.error("Ses anlaşılamadı.")

    st.divider()
    st.session_state.p_no = st.text_input("Protokol No", st.session_state.p_no)
    st.session_state.cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"], index=0 if st.session_state.cinsiyet == "Erkek" else 1)
    st.session_state.yas = st.number_input("Yaş", 0, 120, st.session_state.yas)
    kilo = st.number_input("Kilo (kg)", 5, 250, 85)
    
    st.subheader("🧠 GKS DEĞERLENDİRMESİ")
    g_e = st.selectbox("Göz (E)", [4, 3, 2, 1])
    g_v = st.selectbox("Sözel (V)", [5, 4, 3, 2, 1])
    g_m = st.selectbox("Motor (M)", [6, 5, 4, 3, 2, 1])
    gcs_skor = g_e + g_v + g_m

    st.session_state.kre = st.number_input("Kreatinin", 0.1, 45.0, st.session_state.kre)
    st.session_state.hb = st.number_input("Hemoglobin (Hb)", 3.0, 25.0, st.session_state.hb)
    st.session_state.wbc = st.number_input("WBC (Lökosit)", 0, 500000, st.session_state.wbc)
    st.session_state.plt = st.number_input("PLT (Trombosit)", 0, 2000000, st.session_state.plt)

# 3. KLİNİK BULGU SEÇİMİ
st.subheader("🔍 Klinik Semptom ve Fizik Muayene Bulguları")
tabs = st.tabs(["🫀 KARDİYO", "🫁 PULMONER", "🤢 GİS-KC", "🧪 ENDOKRİN", "🧠 NÖROLOJİ", "🩸 HEMATO-ONKO", "🧬 ROMATO-ENF"])

with tabs[0]: kardiyo = st.multiselect("KV", ["Göğüs Ağrısı", "Çarpıntı", "Hipotansiyon"], default=[x for x in st.session_state.secili_bulgular if x in ["Göğüs Ağrısı", "Çarpıntı", "Hipotansiyon"]])
with tabs[1]: pulm = st.multiselect("PULM", ["Nefes Darlığı", "Öksürük"], default=[x for x in st.session_state.secili_bulgular if x in ["Nefes Darlığı", "Öksürük"]])
# ... (Diger tablarin senin orijinal listenle dolu oldugunu varsayiyorum)

b = kardiyo + pulm # Tüm seçilenleri birleştir

# 4. MASTER 85+ HASTALIK VERİTABANI
# === İSMAİL, BURAYA SENİN O 85 HASTALIKLIK DEV LİSTENİ YAPIŞTIR ===
master_db = {
    "STEMI": {"b": ["Göğüs Ağrısı", "Çarpıntı"], "t": "EKG", "ted": "Acil Anjiyo"},
    "Pnömoni": {"b": ["Ateş (>38)", "Öksürük"], "t": "AC Grafisi", "ted": "Antibiyotik"}
}

# 5. FINAL ANALİZ MOTORU + GEMINI 2.5 FLASH GÜCÜ
if st.button("🚀 ANALİZİ BAŞLAT"):
    results = []
    for ad, v in master_db.items():
        matches = set(b).intersection(set(v["b"]))
        if matches:
            score = round((len(matches) / len(v["b"])) * 100, 1)
            results.append({"ad": ad, "puan": score, "v": v})
    
    results = sorted(results, key=lambda x: x['puan'], reverse=True)
    
    if results:
        top_pre = results[0]['ad']
        sesli_oku(f"En olası ön tanı {top_pre}") # SESLİ DÖNÜT
        
        for r in results:
            st.markdown(f"""
            <div class='clinical-card'>
                <h2>{r['ad']} (%{r['puan']})</h2>
                <p>🧪 <b>Tetkik:</b> {r['v']['t']}</p>
                <p>💊 <b>Tedavi:</b> {r['v']['ted']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # GEMINI 2.5 FLASH LITE ANALİZİ
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        res = model.generate_content(f"Hasta {st.session_state.yas}y, Bulgular: {b}. Analiz et.")
        st.info(res.text)

st.markdown("---")
st.caption("GELİŞTİRİCİ: İSMAİL ORHAN GEMLİK 2026")
