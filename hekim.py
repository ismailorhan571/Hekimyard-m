import streamlit as st
from datetime import datetime

# 1. ULTRA MODERN & AÇIK RENK TASARIM (APPLE CLINICAL STYLE)
st.set_page_config(page_title="İSMAİL ORHAN | Klinik Karar Destek", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp { background-color: #F8FAFC; color: #1E293B; font-family: 'Inter', sans-serif; }
    
    /* Üst Başlık Alanı */
    .main-header {
        background: white; padding: 60px; border-radius: 30px; text-align: center; margin-bottom: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.05); border: 1px solid #E2E8F0;
    }
    .main-header h1 { color: #2563EB; font-weight: 800; font-size: 3rem; margin-bottom: 10px; }
    .main-header p { color: #64748B; font-size: 1.2rem; }
    
    /* Kart Yapıları */
    .diag-card { 
        background: white; border: 1px solid #E2E8F0; padding: 35px; border-radius: 25px; 
        margin-bottom: 25px; border-top: 8px solid #3B82F6;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03); transition: 0.3s;
    }
    .diag-card:hover { transform: translateY(-5px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); }
    
    /* Kritik Uyarılar */
    .critical-alert { 
        background: #FEF2F2; border: 1px solid #FECACA; 
        color: #B91C1C; padding: 20px; border-radius: 15px; font-weight: 700;
        margin-bottom: 20px; text-align: center;
    }
    
    /* Epikriz Kağıdı */
    .epikriz-paper { 
        background: white; color: #1E293B; padding: 50px; border-radius: 20px; 
        font-family: 'Inter', sans-serif; border: 1px solid #E2E8F0; line-height: 1.6;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.01);
    }
    
    /* Buton Tasarımı */
    .stButton>button {
        background: #2563EB; color: white; border-radius: 15px; 
        height: 5em; width: 100%; font-weight: 700; font-size: 22px; border: none;
        transition: 0.3s; box-shadow: 0 10px 25px rgba(37, 99, 235, 0.2);
    }
    .stButton>button:hover { background: #1D4ED8; box-shadow: 0 15px 35px rgba(37, 99, 235, 0.4); }
    
    /* Sidebar Düzenlemesi */
    [data-testid="stSidebar"] { background-color: white; border-right: 1px solid #E2E8F0; }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown(f"""
    <div class='main-header'>
        <h1>TIBBİ ALTYAPI VE ANALİZ ÜSSÜ</h1>
        <p>Dijital Sağlık Arşivi ve Karar Destek Sistemi | <b>İSMAİL ORHAN</b></p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL - AKILLI VİTAL GİRİŞİ
with st.sidebar:
    st.markdown("### 🏥 HASTA KARTI")
    h_no = st.text_input("Protokol Numarası", "İO-2026-V7")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Vücut Ağırlığı (kg)", 3, 220, 75)
    st.divider()
    st.markdown("### 🩸 LABORATUAR VERİLERİ")
    seker = st.number_input("Açlık Glukozu (mg/dL)", 20, 1000, 105)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    potasyum = st.number_input("Potasyum (mEq/L)", 1.0, 10.0, 4.0, 0.1)
    ta_sis = st.number_input("Sistolik Tansiyon (mmHg)", 40, 280, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.metric("Böbrek Rezervi (eGFR)", f"{egfr} ml/dk")
    
    if egfr < 30: st.markdown("<div class='critical-alert'>🚨 RENAL YETMEZLİK: DOZ REVİZYONU ŞART!</div>", unsafe_allow_html=True)
    if potasyum > 5.5: st.markdown("<div class='critical-alert'>🚨 HİPERPOTASEMİ RİSKİ</div>", unsafe_allow_html=True)

# 4. GENİŞLETİLMİŞ SİSTEMİK SORGULAMA
st.subheader("🩺 Klinik Bulguları Belirleyin")
col_1, col_2, col_3 = st.columns(3)

hepsi = []
with col_1:
    with st.container(border=True):
        st.markdown("**GENEL & ROMATOLOJİ**")
        hepsi.extend(st.multiselect("Bulgular", ["Ateş", "Kilo Kaybı", "Gece Terlemesi", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Eklem Ağrısı", "Peteşi/Purpura", "Lenfadenopati", "Ağızda Aft"]))
    with st.container(border=True):
        st.markdown("**GASTROENTEROLOJİ & KC**")
        hepsi.extend(st.multiselect("Bulgular ", ["Asit", "Sarılık", "Karın Ağrısı", "Hematemez", "Melena", "Hepatomegali", "Splenomegali", "Caput Medusae", "Asteriksis", "Murphy (+)"]))

with col_2:
    with st.container(border=True):
        st.markdown("**KARDİYOLOJİ & DAMAR**")
        hepsi.extend(st.multiselect("Bulgular  ", ["Göğüs Ağrısı", "Çarpıntı", "PND / Ortopne", "Bilateral Ödem", "Unilateral Ödem", "Boyun Ven Dolgunluğu", "Hipotansiyon", "S3/S4 Sesi"]))
    with st.container(border=True):
        st.markdown("**GÖĞÜS HASTALIKLARI**")
        hepsi.extend(st.multiselect("Bulgular   ", ["Nefes Darlığı", "Öksürük", "Hemoptizi", "Plevritik Ağrı", "Ral / Ronküs", "Wheezing / Stridor"]))

with col_3:
    with st.container(border=True):
        st.markdown("**NÖROLOJİ & TOKSİKOLOJİ**")
        hepsi.extend(st.multiselect("Bulgular    ", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Güç Kaybı", "Ani Baş Ağrısı", "Tremor", "Miyozis / Midriyazis", "Ataksi"]))
    with st.container(border=True):
        st.markdown("**ENDOKRİN & RENAL**")
        hepsi.extend(st.multiselect("Bulgular     ", ["Aseton Kokusu", "Poliüri", "Polidipsi", "Oligüri", "Anüri", "Hiperpigmentasyon", "Mor Stria", "Aydede Yüzü"]))

# 5. DEVASA TANI KÜTÜPHANESİ (MAX İLİŞKİ)
arsiv = {
    "Siroz / Portal Hipertansiyon": {"bulgular": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"], "tetkik": "INR, Albümin, USG (Mavi/Sarı Tüp)", "doz": "Spironolakton 100mg, Laktüloz 3x1", "not": "GİS Kanama varsa Terlipressin!"},
    "Diyabetik Ketoasidoz (DKA)": {"bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Karın Ağrısı"], "tetkik": "Kan Gazı, Ketonyüri (Mor Tüp)", "doz": f"İnsülin: {round(kilo*0.1, 1)} Ünite/Saat", "not": "Potasyum <3.3 ise İnsülini KES!"},
    "Pulmoner Emboli": {"bulgular": ["Hemoptizi", "Unilateral Ödem", "Taşikardi", "Nefes Darlığı", "Plevritik Ağrı"], "tetkik": "BT Anjiyo, D-Dimer (Mavi Tüp)", "doz": f"Enoksaparin {kilo}mg 2x1", "not": "Wells Skoru bakılmalı!"},
    "Akut Pankreatit": {"bulgular": ["Karın Ağrısı", "Bulantı", "Hipotansiyon", "Kuşak Şeklinde Ağrı"], "tetkik": "Amilaz/Lipaz (Sarı Tüp)", "doz": "Agresif SF Hidrasyonu", "not": "Oral alımı durdur!"},
    "Sistemik Lupus (SLE)": {"bulgular": ["Kelebek Döküntü", "Eklem Ağrısı", "Ateş", "Ağızda Aft", "Peteşi/Purpura"], "tetkik": "ANA, Anti-dsDNA (Sarı Tüp)", "doz": "Hidroksiklorokin + Steroid", "not": "Renal tutulumu izle."},
    "Cushing Sendromu": {"bulgular": ["Mor Stria", "Aydede Yüzü", "Hipertansiyon", "Kilo Kaybı"], "tetkik": "24h İdrar Kortizolü", "doz": "Cerrahi / Ketokonazol", "not": "Kemik mineral yoğunluğu bak."},
    "Nefrotik Sendrom": {"bulgular": ["Bilateral Ödem", "Asit", "Poliüri", "Yorgunluk"], "tetkik": "Spot İdrar Protein/Kreatinin", "doz": "ACEi + Diüretik", "not": "Hiperlipidemiye dikkat."},
    "Kalp Yetmezliği (KKY)": {"bulgular": ["Bilateral Ödem", "Ortopne", "Boyun Ven Dolgunluğu", "Ral / Ronküs", "Çarpıntı"], "tetkik": "NT-proBNP, EKO", "doz": "Furosemid + ACEi", "not": "Tuz kısıtlaması şart."}
}

# 6. ANALİZ VE EPİKRİZ MOTORU
if st.button("🚀 SİSTEM ANALİZİNİ ÇALIŞTIR"):
    if not hepsi:
        st.error("Lütfen klinik bulgu seçiniz.")
    else:
        st.divider()
        sonuclar = []
        for ad, d in arsiv.items():
            eslesme = set(hepsi).intersection(set(d["bulgular"]))
            if eslesme:
                puan = round((len(eslesme) / len(d["bulgular"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": d, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        c_res1, c_res2 = st.columns([1.6, 1])
        with c_res1:
            st.markdown("### 🔬 Tanısal Matris ve Tedavi")
            for s in sonuclar:
                st.markdown(f"""
                <div class='diag-card'>
                    <div style='font-size:1.8em; color:#2563EB; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p style='margin-top:10px;'>🎯 <b>Eşleşenler:</b> {", ".join(s['esles'])}</p>
                    <p>🧪 <b>Tetkik Planı:</b> {s['veri']['tetkik']}</p>
                    <p>💉 <b>Hekim Reçetesi ({kilo}kg):</b> {s['veri']['doz']}</p>
                    <p style='color:#B91C1C;'>⚠️ <b>Hayati Not:</b> {s['veri']['not']}</p>
                </div>
                """, unsafe_allow_html=True)

        with c_res2:
            st.markdown("### 📝 RESMİ EPİKRİZ")
            radyo = "Kontrastlı uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / HİDRASYON"
            epikriz = f"""TIBBİ ANALİZ VE KARAR RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
SORUMLU HEKİM: İSMAİL ORHAN
PROTOKOL: {h_no}

[VİTAL BULGULAR]
Yaş: {yas} | Kilo: {kilo}kg | eGFR: {egfr}
Şeker: {seker} | TA: {ta_sis} | K+: {potasyum}

[KLİNİK BULGULAR]
{", ".join(hepsi)}

[ÖN TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[RADYOLOJİK GÜVENLİK]
- {radyo}

--------------------------------------------------
ONAY: SİSTEM GELİŞTİRİCİ:İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("📤 Raporu PDF Olarak Arşivle", epikriz, file_name=f"{h_no}_epikriz.txt")

st.markdown("---")
st.caption("İSMAİL ORHAN | Modern Clinical Decision Support | Version 7.0")
