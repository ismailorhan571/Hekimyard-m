import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Hekim Yardımcı Paneli", page_icon="⚕️", layout="wide")

# Kurumsal ve Temiz Tasarım
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stButton>button { width: 100%; background-color: #1a73e8; color: white; border-radius: 5px; height: 3em; font-weight: bold; }
    .diagnosis-box { padding: 20px; border-radius: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; margin-bottom: 15px; }
    .ai-box { padding: 25px; border-radius: 10px; background-color: #f0f4ff; border-left: 5px solid #1a73e8; }
    .critical { color: #d93025; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- AI CONFIG (404 HATASI ÇÖZÜMÜ) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Model ismini en stabil haliyle tanımlıyoruz
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_AVAILABLE = True
except Exception as e:
    AI_AVAILABLE = False

st.title("⚕️ Klinik Karar Destek ve Teşhis Paneli")
st.write("Dahiliye Servisi Hekim Yardımcı Yazılımı | **Geliştiren: İsmail Orhan**")
st.divider()

# --- SOL PANEL: VİTALLER ---
with st.sidebar:
    st.header("📋 Hasta Verileri")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    st.subheader("🩸 Vital Bulgular")
    ates = st.number_input("Ateş (°C)", 35.0, 42.0, 36.6)
    spo2 = st.slider("SpO2 (%)", 70, 100, 98)
    nabiz = st.number_input("Nabız", 30, 200, 80)
    tansiyon = st.text_input("Tansiyon (Örn: 120/80)", "120/80")

# --- ANA PANEL: SEMPTOMLAR ---
st.subheader("🔍 Klinik Semptom Seçimi")
col1, col2 = st.columns(2)

with col1:
    genel = st.multiselect("Genel / Enfeksiyon", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Lenfadenopati", "Kilo Kaybı"])
    kardiyo = st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Çarpıntı", "Nefes Darlığı", "Ödem"])
    noro = st.multiselect("Nörolojik", ["Baş Ağrısı", "Bilinç Bulanıklığı", "Baş Dönmesi", "Güç Kaybı"])

with col2:
    gastro = st.multiselect("Gastrointestinal", ["Karın Ağrısı", "Bulantı/Kusma", "Melena", "Hematemez", "Sarılık"])
    uriner = st.multiselect("Üriner / Diğer", ["Dizüri", "Hematüri", "Yan Ağrısı", "Eklem Ağrısı", "Döküntü"])

secilenler = genel + kardiyo + noro + gastro + uriner

# --- ANALİZ MOTORU ---
if st.button("KLİNİK ANALİZİ BAŞLAT"):
    if not secilenler:
        st.warning("Lütfen en az bir semptom seçin.")
    else:
        with st.spinner("Veriler analiz ediliyor..."):
            # 1. BÖLÜM: STATİK TANI VE ÖNERİLER (Sistemin kendi mantığı)
            st.markdown("### 📑 Klinik Ön Değerlendirme")
            
            with st.container():
                st.markdown("<div class='diagnosis-box'>", unsafe_allow_html=True)
                
                # Örnek Statik Mantık (Senin eklediğin detaylar)
                if "Göğüs Ağrısı" in secilenler and "Nefes Darlığı" in kardiyo:
                    st.write("👉 **Ön Tanı Adayı:** Akut Koroner Sendrom / Pulmoner Emboli")
                    st.write("🧪 **Gerekli Tetkikler:** EKG, Troponin, D-Dimer, PA Akciğer Grafisi.")
                
                if "Karın Ağrısı" in gastro and "Bulantı/Kusma" in gastro:
                    st.write("👉 **Ön Tanı Adayı:** Akut Batın / Gastroenterit / Pankreatit")
                    st.write("🧪 **Gerekli Tetkikler:** Hemogram, Amilaz-Lipaz, Ayakta Direkt Karın Grafisi.")
                
                if ates > 38 and "Halsizlik" in genel:
                    st.write("👉 **Ön Tanı Adayı:** Enfeksiyon Hastalıkları / Sepsis")
                    st.write("🧪 **Gerekli Tetkikler:** Tam Kan, CRP, Prokalsitonin, Kültür Testleri.")
                
                if spo2 < 93:
                    st.markdown("<p class='critical'>⚠️ KRİTİK: Düşük Oksijen Satürasyonu! Solunum desteği ve arteriyel kan gazı (AKG) değerlendirilmelidir.</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

            # 2. BÖLÜM: YAPAY ZEKA GÖRÜŞÜ (Gemini)
            st.divider()
            st.markdown("### 🤖 Yapay Zeka (Gemini) Uzman Görüşü")
            
            if AI_AVAILABLE:
                prompt = f"""
                Sen uzman bir klinisyen yardımcısısın.
                HASTA: {yas} yaş, {cinsiyet}.
                VİTALLER: Ateş {ates}, SpO2 %{spo2}, Nabız {nabiz}, TA {tansiyon}.
                BELİRTİLER: {', '.join(secilenler)}.
                
                Lütfen bu veriler ışığında:
                1. En olası 3 AYIRICI TANIYI detaylı açıkla.
                2. İstenecek SPESİFİK TETKİKLERİ (Kan, Görüntüleme) listele.
                3. ACİL MÜDAHALE gerektiren bir durum var mı belirt.
                
                Tıp terminolojisi kullan ve profesyonel bir rapor sun.
                """
                try:
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='ai-box'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Yapay zeka yanıt veremedi. Hata: {str(e)}")
            else:
                st.info("Yapay zeka yapılandırması eksik.")

st.divider()
st.caption(f"© 2026 Med-AI Karar Destek | Geliştirici: İsmail Orhan")
