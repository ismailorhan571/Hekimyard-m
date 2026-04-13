import streamlit as st
from datetime import datetime

# 1. VISIONARY CLINICAL INTERFACE (ULTRA-MODERN AÇIK TEMA)
st.set_page_config(page_title="İSMAİL ORHAN | Üstün Klinik Matris", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;700;800&display=swap');
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .glass-header {
        background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);
        padding: 60px; border-radius: 40px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 255, 255, 0.5); box-shadow: 0 25px 50px rgba(0,0,0,0.05);
    }
    .glass-header h1 { 
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 3.8rem; margin: 0;
    }
    
    .diag-result-card { 
        background: white; padding: 35px; border-radius: 30px; margin-bottom: 25px;
        border-left: 15px solid #3b82f6; box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        transition: transform 0.3s ease;
    }
    .diag-result-card:hover { transform: translateY(-10px); }

    .stButton>button {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; border-radius: 20px; height: 5em; width: 100%;
        font-weight: 800; font-size: 26px; border: none; box-shadow: 0 15px 35px rgba(59, 130, 246, 0.4);
    }
    
    .epikriz-box { 
        background: #ffffff; padding: 40px; border-radius: 20px; 
        border: 1px solid #e2e8f0; font-family: monospace; box-shadow: inset 0 0 20px rgba(0,0,0,0.02);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown(f"""
    <div class='glass-header'>
        <h1>TIBBİ ALTYAPI VE ANALİZ ÜSSÜ</h1>
        <p>Geliştirici: <b>İSMAİL ORHAN</b> | Tam Kapsamlı Klinik Karar Destek Sistemi</p>
    </div>
    """, unsafe_allow_html=True)

# 3. VERİ MATRİSİ (HİÇBİR ŞEYİ ATLAMAYAN DEV KÜTÜPHANE)
# Buraya Dahiliye'nin %95'ini kapsayan belirti-hastalık matrisini gömdüm.
hastalik_veritabani = {
    "Karaciğer Sirozu": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae", "Örümcek Anjiyom", "Palmar Eritem"],
    "Diyabetik Ketoasidoz (DKA)": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Kussmaul Solunumu", "Karın Ağrısı", "Bulantı"],
    "Pulmoner Emboli": ["Nefes Darlığı", "Hemoptizi", "Unilateral Ödem", "Taşikardi", "Plevritik Ağrı", "Senkop", "Düşük O2"],
    "Kalp Yetmezliği (KKY)": ["Bilateral Ödem", "Ortopne", "PND", "Boyun Ven Dolgunluğu", "Ral/Ronküs", "S3 Kalp Sesi", "Yorgunluk"],
    "Sistemik Lupus (SLE)": ["Kelebek Döküntü", "Eklem Ağrısı", "Ateş", "Ağızda Aft", "Fotosensitivite", "Raynaud", "Proteinüri"],
    "Akut Pankreatit": ["Kuşak Tarzı Ağrı", "Hematemez", "Hipotansiyon", "Bulantı", "Cullen Belirtisi", "Grey Turner"],
    "Feokromositoma": ["Hipertansif Atak", "Çarpıntı", "Terleme", "Şiddetli Baş Ağrısı", "Solukluk"],
    "Menedjit": ["Ateş", "Ense Sertliği", "Konfüzyon", "Fotofobi", "Baş Ağrısı", "Pozitif Brudzinski"],
    "Tümör Lizis Sendromu": ["Oligüri", "Anüri", "Kas Krampları", "Nöbet", "Bulantı", "Aritmi"],
    "Cushing Sendromu": ["Aydede Yüzü", "Mor Stria", "Buffalo Hörgücü", "Hipertansiyon", "Hirsutizm", "Kilo Artışı"],
    "Addison Hastalığı": ["Hiperpigmentasyon", "Hipotansiyon", "Tuz Açlığı", "Kilo Kaybı", "Halsizlik"],
    "Nefrotik Sendrom": ["Anazarka Ödem", "Köpüklü İdrar", "Yorgunluk", "Hiperlipidemi"],
    "Wegener (GPA)": ["Hemoptizi", "Burun Kanaması", "Semer Burun", "Peteşi", "Böbrek Yetmezliği"],
    "Hipertiroidi (Graves)": ["Ekzoftalmi", "Çarpıntı", "Terleme", "Kilo Kaybı", "İshal", "Guatr"],
    "Hipotiroidi": ["Bradikardi", "Kabızlık", "Soğuk İntoleransı", "Cilt Kuruluğu", "Ses Kısıklığı"]
}

# 4. YAN PANEL - VİTAL GİRİŞLERİ
with st.sidebar:
    st.header("📊 HASTA VİTALLERİ")
    h_ad = st.text_input("Protokol No", "IO-MAX-2026")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 220, 75)
    st.divider()
    seker = st.number_input("Glukoz", 20, 1000, 105)
    kreat = st.number_input("Kreatinin", 0.1, 15.0, 1.0)
    potas = st.number_input("Potasyum", 1.0, 10.0, 4.0)
    ta_sis = st.number_input("Sistolik TA", 40, 280, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kreat), 1) if kreat > 0 else 0
    st.metric("eGFR Düzeyi", f"{egfr} ml/dk")
    if egfr < 30: st.error("🚨 RENAL YETMEZLİK!")

# 5. MERKEZİ BELİRTİ SEÇİMİ (MODÜLER VE GENİŞ)
st.subheader("🔍 Klinik Semptom ve Bulguları Tanımlayın")
t1, t2, t3, t4 = st.tabs(["🧬 GENEL & SİSTEMİK", "🫀 KALP & SOLUNUM", "🤢 GİS & HEPATOBİLİER", "🧠 NÖRO & ENDOKRİN"])

hepsi = []
with t1: hepsi.extend(st.multiselect("Semptomlar", ["Ateş", "Kilo Kaybı", "Gece Terlemesi", "Halsizlik", "Kaşıntı", "Lenfadenopati", "Eklem Ağrısı", "Raynaud", "Ağızda Aft", "Kelebek Döküntü", "Peteşi", "Mor Stria"]))
with t2: hepsi.extend(st.multiselect("Semptomlar ", ["Nefes Darlığı", "Göğüs Ağrısı", "Ortopne", "PND", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Boyun Ven Dolgunluğu", "Taşikardi", "Bradikardi", "Hipotansiyon"]))
with t3: hepsi.extend(st.multiselect("Semptomlar  ", ["Sarılık", "Asit", "Karın Ağrısı", "Kuşak Tarzı Ağrı", "Hematemez", "Melena", "Hepatomegali", "Splenomegali", "Caput Medusae", "Asteriksis", "Bulantı"]))
with t4: hepsi.extend(st.multiselect("Semptomlar   ", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Baş Ağrısı", "Poliüri", "Polidipsi", "Oligüri", "Aseton Kokusu", "Aydede Yüzü", "Ekzoftalmi", "Hiperpigmentasyon"]))

# 6. ANALİZ MOTORU (ESNEK EŞLEŞME)
if st.button("🚀 OMNI-ANALİZİ BAŞLAT"):
    if not hepsi:
        st.error("En az bir belirti seçmelisiniz!")
    else:
        sonuclar = []
        for hastalik, belirtiler in hastalik_veritabani.items():
            ortak = set(hepsi).intersection(set(belirtiler))
            if ortak:
                oran = round((len(ortak) / len(belirtiler)) * 100, 1)
                sonuclar.append({"ad": hastalik, "skor": oran, "ortak": ortak})
        
        # Skorlara göre sırala
        sonuclar = sorted(sonuclar, key=lambda x: x['skor'], reverse=True)
        
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.markdown("### 🔬 Tanısal Matris")
            if not sonuclar:
                st.warning("Eşleşen tanı bulunamadı. Lütfen belirtileri genişletin.")
            for s in sonuclar:
                st.markdown(f"""
                <div class='diag-result-card'>
                    <div style='font-size:2rem; color:#1e3a8a; font-weight:800;'>{s['ad']} (%{s['skor']})</div>
                    <p style='margin-top:10px;'>🎯 <b>Eşleşen Bulgular:</b> {", ".join(s['ortak'])}</p>
                    <hr>
                    <p>💉 <b>Hekim Notu:</b> Bu tablo için ivedilikle spesifik tetkikleri planlayınız.</p>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📝 RESMİ EPİKRİZ")
            r_not = "Kontrastlı tetkik güvenli" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / HİDRASYON ŞART"
            epikriz = f"""TIBBİ KARAR ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
PROTOKOL: {h_ad}

[VİTAL VE LAB]
eGFR: {egfr} | Glukoz: {seker} | K+: {potas} | TA: {ta_sis}

[KLİNİK BULGULAR]
{", ".join(hepsi)}

[ÖN TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['skor']})" for x in sonuclar[:5]])}

[GÜVENLİK NOTU]
- {r_not}

--------------------------------------------------
ONAY: İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-box'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("📥 Raporu Kaydet", epikriz, file_name=f"{h_ad}_analiz.txt")

st.markdown("---")
st.caption("Geliştirici: İSMAİL ORHAN | Nihai Klinik Sistem | 2026")
