import streamlit as st
from datetime import datetime

# 1. MODERN NEON-KLİNİK TASARIM
st.set_page_config(page_title="İSMAİL ORHAN | OMNI-HEAL V6", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500;800&display=swap');
    
    .stApp { background-color: #05070a; color: #e2e8f0; font-family: 'JetBrains Mono', monospace; }
    
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #1d4ed8 100%);
        padding: 60px; border-radius: 30px; text-align: center; margin-bottom: 40px;
        box-shadow: 0 20px 50px rgba(29, 78, 216, 0.3); border: 1px solid #3b82f6;
    }
    
    .category-box {
        background: #0f172a; border: 1px solid #1e293b; padding: 20px;
        border-radius: 20px; margin-bottom: 15px; border-top: 5px solid #3b82f6;
    }
    
    .diag-card { 
        background: #0f172a; border: 1px solid #334155; padding: 30px; border-radius: 20px; 
        margin-bottom: 25px; border-left: 15px solid #10b981;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.5);
    }
    
    .critical-alert { 
        background: rgba(220, 38, 38, 0.15); border: 2px solid #ef4444; 
        color: #fca5a1; padding: 20px; border-radius: 15px; font-weight: 800;
        margin-bottom: 20px; animation: blinker 1.5s linear infinite;
    }
    
    @keyframes blinker { 50% { opacity: 0.5; } }
    
    .epikriz-paper { 
        background: #f8fafc; color: #0f172a; padding: 50px; border-radius: 10px; 
        font-family: 'Courier New', monospace; border: 8px double #1e293b; line-height: 1.5;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #10b981, #059669); color: white; border-radius: 20px; 
        height: 6em; width: 100%; font-weight: 900; font-size: 28px; border: none;
        transition: 0.4s; box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
    }
    .stButton>button:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(16, 185, 129, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>⚡ OMNI-HEAL KLİNİK SİSTEM</h1><p>Maksimum Veri Havuzu | Tanı-Dozaj-Skorlama | İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL - HASTA TERMİNALİ
with st.sidebar:
    st.markdown("### 🖥️ HASTA VİTALLERİ")
    h_ad = st.text_input("Hasta No", "ISMAIL-ORHAN-2026")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 220, 75)
    st.divider()
    seker = st.number_input("Glukoz (mg/dL)", 20, 1000, 105)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    potasyum = st.number_input("Potasyum (mEq/L)", 1.0, 10.0, 4.2, 0.1)
    ta_sis = st.number_input("Sistolik TA", 40, 280, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.metric("Böbrek Fonksiyonu (eGFR)", f"{egfr} ml/dk")
    
    if egfr < 30: st.markdown("<div class='critical-alert'>🚨 RENAL FREN AKTİF</div>", unsafe_allow_html=True)
    if seker > 300: st.markdown("<div class='critical-alert'>🚨 DİKKAT: HİPERGLİSEMİ</div>", unsafe_allow_html=True)

# 4. SİSTEMİK SORGULAMA (DEVASA BELİRTİ HAVUZU)
st.subheader("🔍 Klinik Bulguları Eksiksiz İşleyin")
# Kategorileri daha kolaylaştırdım: Şikayetin bölgesine göre seç.
col_a, col_b = st.columns(2)

with col_a:
    with st.expander("🩺 GENEL & SİSTEMİK BULGULAR (Tüm Vücut)", expanded=True):
        sys = st.multiselect("Belirtiler", ["Ateş", "Gece Terlemesi", "Kilo Kaybı (>%10)", "Yorgunluk", "Lenfadenopati (Genel)", "Peteşi/Purpura", "Sarılık", "Kaşıntı", "Eklem Ağrısı", "Raynaud Fenomeni"])
    with st.expander("🧠 NÖRO-PSİKİYATRİK"):
        nro = st.multiselect("Nöro Belirtiler", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Fokal Güç Kaybı", "Ataksi", "Tremor", "Afazi", "Diplopi", "Ani Baş Ağrısı", "Miyozis", "Midriyazis"])
    with st.expander("🫀 KALP-DAMAR"):
        krd = st.multiselect("Kardiyo Belirtiler", ["Göğüs Ağrısı (Baskı)", "Çarpıntı", "Boyun Ven Dolgunluğu", "Bilateral Ödem", "Unilateral Ödem", "S3/S4 Sesi", "Üfürüm", "Hipotansiyon"])

with col_b:
    with st.expander("🫁 SOLUNUM SİSTEMİ", expanded=True):
        sln = st.multiselect("Solunum Belirtiler", ["Nefes Darlığı", "Öksürük", "Hemoptizi", "Ortopne", "PND", "Plevritik Ağrı", "Ral/Ronküs", "Wheezing", "Stridor"])
    with st.expander("🤢 GASTROENTEROLOJİ & KC"):
        gst = st.multiselect("Gis Belirtiler", ["Karın Ağrısı", "Hematemez", "Melena", "Asit", "Hepatomegali", "Splenomegali", "Caput Medusae", "Asteriksis", "Murphy (+)", "Disfaji"])
    with st.expander("🧪 ENDOKRİN & RENAL"):
        end = st.multiselect("Endo Belirtiler", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Oligüri", "Anüri", "Hiperpigmentasyon", "Ekzoftalmi", "Mor Stria", "Aydede Yüzü"])

hepsi = sys + nro + krd + sln + gst + end

# 5. MAKSİMUM VERİ KÜTÜPHANESİ (HİÇBİR ŞEY SİLİNMEDİ - YENİLERİ EKLENDİ)
arsiv = {
    "Karaciğer Sirozu": {"bulgular": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"], "tetkik": "INR, Albümin, Amonyak, Batın USG", "doz": "Spironolakton 100mg, Furosemid 40mg", "not": "SBP şüphesinde parasentez!"},
    "Diyabetik Ketoasidoz": {"bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Karın Ağrısı"], "tetkik": "Kan Gazı, Kan Şekeri, Ketonyüri", "doz": f"İnsülin: {round(kilo*0.1, 1)} Ü/saat", "not": "K+ < 3.3 ise İnsülini durdur!"},
    "Pulmoner Emboli": {"bulgular": ["Hemoptizi", "Unilateral Ödem", "Taşikardi", "Nefes Darlığı", "Plevritik Ağrı"], "tetkik": "BT Anjiyo, D-Dimer", "doz": f"Enoksaparin {kilo}mg 2x1", "not": "eGFR < 30 ise Heparin!"},
    "Bakteriyel Menenjit": {"bulgular": ["Ateş", "Ense Sertliği", "Konfüzyon", "Ani Baş Ağrısı"], "tetkik": "Lomber Ponksiyon, BOS Kültürü", "doz": "Seftriakson 2x2g + Vankomisin", "not": "LP öncesi BT ile KİBAS ekarte et!"},
    "Nefrotik Sendrom": {"bulgular": ["Bilateral Ödem", "Asit", "Poliüri", "Yorgunluk"], "tetkik": "24h İdrar Proteini, Albümin", "doz": "Steroid + ACE İnhibitörü", "not": "Hiperlipidemi ve tromboz riskine dikkat."},
    "Feokromositoma": {"bulgular": ["Çarpıntı", "Terleme", "Ani Baş Ağrısı", "Hipertansiyon"], "tetkik": "İdrar Metanefrin, Sürrenal MR", "doz": "Alfa Bloker (Doksazosin)", "not": "Asla önce Beta Bloker verme!"},
    "Lupus (SLE)": {"bulgular": ["Kelebek Döküntü", "Eklem Ağrısı", "Peteşi/Purpura", "Ateş", "Plevritik Ağrı"], "tetkik": "ANA, Anti-dsDNA, C3/C4", "doz": "Hidroksiklorokin + Steroid", "not": "Renal tutulumu (Proteinüri) izle."},
    "Konjesif Kalp Yetmezliği": {"bulgular": ["Bilateral Ödem", "Ortopne", "PND", "Boyun Ven Dolgunluğu", "Ral/Ronküs"], "tetkik": "NT-proBNP, EKO", "doz": "Furosemid + ACEi + Beta Bloker", "not": "Kilo takibi ve tuz kısıtlaması şart."},
    "Malignite / Lenfoma": {"bulgular": ["Gece Terlemesi", "Kilo Kaybı (>%10)", "Lenfadenopati (Genel)", "Splenomegali"], "tetkik": "LN Biyopsisi, PET-BT", "doz": "Onkoloji Konsültasyonu", "not": "Tümör Lizis Sendromu açısından izle."}
}

# 6. ANALİZ VE AKILLI DOZAJ MOTORU
if st.button("🚀 OMNI-ANALİZİ BAŞLAT (MAX VERİ)"):
    if not hepsi:
        st.error("Lütfen belirti seçiniz.")
    else:
        sonuclar = []
        for ad, d in arsiv.items():
            eslesme = set(hepsi).intersection(set(d["bulgular"]))
            if eslesme:
                puan = round((len(eslesme) / len(d["bulgular"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": d, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        res1, res2 = st.columns([1.5, 1])
        with res1:
            st.markdown("### 🔬 Klinik Matris Sonuçları")
            for s in sonuclar:
                st.markdown(f"""
                <div class='diag-card'>
                    <div style='font-size:1.8em; color:#10b981; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p>🎯 <b>Eşleşen Belirtiler:</b> {", ".join(s['esles'])}</p>
                    <p>🧪 <b>Tetkik Planı:</b> {s['veri']['tetkik']}</p>
                    <p>💉 <b>Kişiye Özel Doz:</b> {s['veri']['doz']}</p>
                    <p style='color:#f87171;'>⚠️ <b>Kritik Not:</b> {s['veri']['not']}</p>
                </div>
                """, unsafe_allow_html=True)

        with res2:
            st.markdown("### 📝 RESMİ EPİKRİZ RAPORU")
            rad = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ / ÖN HİDRASYON ŞART"
            epikriz = f"""TIBBİ KARAR ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
PROTOKOL: {h_ad} | eGFR: {egfr}

[BELİRTİLER]
{", ".join(hepsi)}

[ÖN TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[RADYOLOJİ VE GÜVENLİK]
- Böbrek Fonksiyonu: {rad}
- Glukoz: {seker} mg/dL ({"Kritik" if seker > 300 else "Stabil"})

--------------------------------------------------
ONAY: İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("📥 Arşive Kaydet", epikriz, file_name=f"{h_ad}_rapor.txt")

st.markdown("---")
st.caption("İSMAİL ORHAN | Modern Clinical Intelligence Center | 2026")
