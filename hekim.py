import streamlit as st
from datetime import datetime

# 1. ULTRA-PREMIUM VISIONARY INTERFACE (APPLE CLINICAL STYLE)
st.set_page_config(page_title="İSMAİL ORHAN | Omni-Clinical Master V13", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: #F8FAFC; color: #1E293B; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: white; padding: 50px; border-radius: 40px; text-align: center;
        border: 1px solid #E2E8F0; box-shadow: 0 20px 40px rgba(0,0,0,0.03); margin-bottom: 40px;
    }
    .main-header h1 { 
        background: linear-gradient(90deg, #2563EB, #7C3AED);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 3.5rem; 
    }
    
    .status-card {
        background: white; border: 1px solid #E2E8F0; padding: 25px; border-radius: 25px;
        margin-bottom: 20px; border-top: 10px solid #2563EB;
        transition: 0.3s ease; box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .status-card:hover { transform: translateY(-5px); box-shadow: 0 12px 30px rgba(0,0,0,0.05); }
    
    .stButton>button {
        background: linear-gradient(90deg, #2563EB, #7C3AED); color: white; border-radius: 18px;
        height: 5em; width: 100%; font-weight: 800; font-size: 24px; border: none;
    }
    
    .critical-alert { 
        background: #FEF2F2; color: #B91C1C; padding: 15px; border-radius: 15px;
        border: 1px solid #FCA5A5; font-weight: 700; text-align: center; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST BAŞLIK
st.markdown(f"""
    <div class='main-header'>
        <h1>TIBBİ ALTYAPI VE ANALİZ KOMUTA MERKEZİ</h1>
        <p>Geliştirici: <b>İSMAİL ORHAN</b> | Integrated Clinical Intelligence System V13</p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL - HASTA TERMİNALİ VE AKILLI HESAPLAYICILAR
with st.sidebar:
    st.header("👤 HASTA TERMİNALİ")
    h_no = st.text_input("Protokol", "İO-ULTRA-2026")
    yas = st.number_input("Yaş", 0, 110, 45)
    kilo = st.number_input("Kilo (kg)", 3, 200, 75)
    
    st.divider()
    st.markdown("### 🧪 VİTAL & LAB VERİLERİ")
    glu = st.number_input("Glukoz (mg/dL)", 20, 1000, 105)
    kre = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    k_plus = st.number_input("Potasyum (mEq/L)", 1.0, 10.0, 4.2)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 40, 280, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kre), 1) if kre > 0 else 0
    st.metric("eGFR Düzeyi", f"{egfr} ml/dk")
    
    if egfr < 30: st.markdown("<div class='critical-alert'>🚨 RENAL YETMEZLİK</div>", unsafe_allow_html=True)
    if k_plus > 5.5: st.markdown("<div class='critical-alert'>🚨 KRİTİK POTASYUM</div>", unsafe_allow_html=True)

# 4. SKORLAMA SİSTEMLERİ (Eksiksiz Birleşim)
st.subheader("🧮 Klinik Risk ve Ciddiyet Skorları")
col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown("**Wells (PE) & CHA2DS2 (AF)**")
    w_sum = st.checkbox("DVT Bulgusu (+3)") + st.checkbox("Alternatif Tanı Az Olası (+3)")
    st.info(f"Wells Puanı: {w_sum*3}")
with col_s2:
    st.markdown("**GKS (Glasgow Koma)**")
    gks = st.slider("Skala", 3, 15, 15)
    if gks <= 8: st.error("⚠️ ENTÜBASYON DÜŞÜN!")
with col_s3:
    st.markdown("**Sıvı Hesaplayıcı**")
    def_sivi = kilo * 30
    st.success(f"Günlük İdame: {def_sivi} cc")

# 5. DEVASA BELİRTİ VE BULGU MATRİSİ (HİÇBİR ŞEY SİLİNMEDİ)
st.subheader("🔍 Kapsamlı Klinik Sorgulama")
tabs = st.tabs(["🧬 SİSTEMİK", "🫀 KARDİYO-PULMONER", "🤢 GİS & HEPATOBİLİER", "🧠 NÖRO & ENDOKRİN", "🩸 HEMATO & ROMATO"])

hepsi = []
with tabs[0]: 
    hepsi.extend(st.multiselect("Genel", ["Ateş", "Kilo Kaybı", "Gece Terlemesi", "Halsizlik", "Lenfadenopati", "Kaşıntı", "Ödem (Genel)", "Sarılık"]))
with tabs[1]: 
    hepsi.extend(st.multiselect("Kalp-Akciğer", ["Göğüs Ağrısı", "Nefes Darlığı", "Ortopne", "PND", "Hemoptizi", "Taşikardi", "Bilateral Ödem", "Unilateral Ödem", "Boyun Ven Dolgunluğu", "Ral/Ronküs", "Wheezing"]))
with tabs[2]: 
    hepsi.extend(st.multiselect("Gis-Kc", ["Karın Ağrısı", "Kuşak Tarzı Ağrı", "Hematemez", "Melena", "Asit", "Hepatomegali", "Splenomegali", "Caput Medusae", "Asteriksis", "Murphy (+)", "Bulantı/Kusma"]))
with tabs[3]: 
    hepsi.extend(st.multiselect("Nöro-Endo", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Ani Baş Ağrısı", "Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi"]))
with tabs[4]: 
    hepsi.extend(st.multiselect("Hematoloji-Romatoloji", ["Peteşi/Purpura", "Kelebek Döküntü", "Raynaud", "Sabah Sertliği", "Eklem Ağrısı", "Ağızda Aft", "Fotosensitivite", "Deri Sertliği"]))

# 6. EN GENİŞ TIBBİ VERİ TABANI (TANI + TETKİK + TEDAVİ)
# Tüm önceki konuşmalardaki hastalıklar ve daha fazlası eklendi.
master_database = {
    "Karaciğer Sirozu": {
        "bulgu": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"],
        "tetkik": "INR, Albümin, Amonyak, Batın USG, Portal Doppler",
        "tedavi": "Spironolakton 100mg + Furosemid 40mg, Laktüloz, Tuz Kısıtlaması"
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgu": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Karın Ağrısı"],
        "tetkik": "Venöz Kan Gazı (pH < 7.3), İdrar Ketoni, Kan Şekeri > 250",
        "tedavi": f"İnsülin Perfüzyon (0.1 Ü/kg/saat = {round(kilo*0.1,1)} Ü/sa), SF Hidrasyonu, Potasyum Takibi"
    },
    "Pulmoner Emboli": {
        "bulgu": ["Hemoptizi", "Unilateral Ödem", "Taşikardi", "Nefes Darlığı", "Plevritik Ağrı"],
        "tetkik": "BT Anjiyo, D-Dimer, EKG (S1Q3T3), Troponin",
        "tedavi": f"Enoksaparin {kilo}mg 2x1 S.C., Stabil değilse Trombolitik"
    },
    "Sistemik Lupus (SLE)": {
        "bulgu": ["Kelebek Döküntü", "Eklem Ağrısı", "Peteşi/Purpura", "Oral Aft", "Fotosensitivite"],
        "tetkik": "ANA, Anti-dsDNA, C3-C4 Seviyeleri, Tam İdrar (Proteinüri)",
        "tedavi": "Hidroksiklorokin, Sistemik Steroid, İmmünsupresif"
    },
    "Akut Pankreatit": {
        "bulgu": ["Kuşak Tarzı Ağrı", "Bulantı/Kusma", "Hipotansiyon"],
        "tetkik": "Lipaz/Amilaz (3 kat artış), Batın BT",
        "tedavi": "NPO (Oral Stop), Agresif SF Hidrasyonu, Analjezi"
    },
    "Menedjit (Bakteriyel)": {
        "bulgu": ["Ateş", "Ense Sertliği", "Konfüzyon", "Ani Baş Ağrısı"],
        "tetkik": "Lomber Ponksiyon, BOS Kültürü, Kafa BT (Önce)",
        "tedavi": "Seftriakson 2x2g + Vankomisin + Deksametazon"
    },
    "Feokromositoma": {
        "bulgu": ["Taşikardi", "Ani Baş Ağrısı", "Terleme", "Hipotansiyon"],
        "tetkik": "Plazma Metanefrinleri, Sürrenal BT",
        "tedavi": "Alfa Bloker (Doksazosin) - Sonra Beta Bloker"
    },
    "Addison Krizi": {
        "bulgu": ["Hiperpigmentasyon", "Hipotansiyon", "Halsizlik"],
        "tetkik": "ACTH Stimülasyon, Na (Düşük), K (Yüksek), Kortizol",
        "tedavi": "IV Hidrokortizon + Agresif Sıvı"
    },
    "Nefrotik Sendrom": {
        "bulgu": ["Bilateral Ödem", "Asit", "Oligüri"],
        "tetkik": "24h İdrar Proteini, Albümin, Lipid Paneli",
        "tedavi": "Steroid + ACEi + Diüretik"
    },
    "Wegener (GPA)": {
        "bulgu": ["Hemoptizi", "Peteşi/Purpura", "Nefes Darlığı"],
        "tetkik": "c-ANCA, Akciğer BT, Böbrek Biyopsisi",
        "tedavi": "Pulse Steroid + Siklofosfamid"
    }
}

# 7. ANALİZ MOTORU
if st.button("🚀 OMNI-HEAL ANALİZİNİ ÇALIŞTIR (V13)"):
    if not hepsi:
        st.error("Lütfen klinik belirti seçimi yapınız!")
    else:
        sonuclar = []
        for ad, d in master_database.items():
            eslesme = set(hepsi).intersection(set(d["bulgu"]))
            if eslesme:
                skor = round((len(eslesme) / len(d["bulgu"])) * 100, 1)
                sonuclar.append({"ad": ad, "skor": skor, "veri": d, "ortak": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['skor'], reverse=True)
        
        res1, res2 = st.columns([1.6, 1])
        with res1:
            st.markdown("### 🔬 Diferansiyel Tanı ve Tedavi")
            for s in sonuclar:
                st.markdown(f"""
                <div class='status-card'>
                    <div style='font-size:1.9em; color:#2563EB; font-weight:800;'>{s['ad']} (%{s['skor']})</div>
                    <p>🎯 <b>Tespit Edilen:</b> {", ".join(s['ortak'])}</p>
                    <p>🧪 <b>Tetkik Planı:</b> {s['veri']['tetkik']}</p>
                    <p>💊 <b>Tedavi Protokolü:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with res2:
            st.markdown("### 📝 RESMİ EPİKRİZ RAPORU")
            r_not = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK ŞART"
            epikriz = f"""KLİNİK KARAR VE ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
PROTOKOL: {h_no}

[HASTA VİTALLERİ]
Yaş: {yas} | Kilo: {kilo}kg | eGFR: {egfr}
Glukoz: {glu} | Potasyum: {k_plus} | TA: {ta_sis}

[SEÇİLEN KLİNİK BULGULAR]
{", ".join(hepsi)}

[OLASI TANILAR VE UYUM]
{chr(10).join([f"- {x['ad']} (%{x['skor']})" for x in sonuclar[:5]])}

[RADYOLOJİK GÜVENLİK]
- {r_not}
- GKS: {gks} | Günlük İdame: {def_sivi}cc

--------------------------------------------------
ONAY: İSMAİL ORHAN
"""
            st.markdown(f"<pre style='background:white; padding:30px; border:1px solid #E2E8F0; border-radius:15px; font-size:13px;'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Raporu PDF Arşivine Al", epikriz, file_name=f"{h_no}_io_final.txt")

st.markdown("---")
st.caption("Geliştirici: İSMAİL ORHAN | Global Integrated Clinical Network | 2026")
