import streamlit as st
from datetime import datetime

# 1. TASARIM: ELİT KLİNİK KOMUTA MERKEZİ
st.set_page_config(page_title="Medical Archive v21 - İsmail Orhan", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010409; color: #c9d1d9; }
    .main-header {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); padding: 50px;
        border-radius: 20px; text-align: center; border: 1px solid #30363d;
        box-shadow: 0 4px 20px rgba(0,0,0,0.8); margin-bottom: 30px;
    }
    .diag-card { 
        background: #0d1117; border: 1px solid #30363d; 
        padding: 25px; border-radius: 15px; margin-bottom: 15px;
    }
    .section-title { color: #58a6ff; font-weight: 800; font-size: 1.3em; margin-bottom: 10px; border-left: 5px solid #238636; padding-left: 10px; }
    .epikriz-paper { 
        background: #ffffff; color: #1e293b; padding: 35px; border-radius: 8px; 
        font-family: 'Courier New', monospace; line-height: 1.1; border: 2px solid #30363d;
    }
    .stButton>button {
        background: #238636; color: white; border-radius: 12px; height: 5em; width: 100%; 
        font-weight: 800; font-size: 22px; transition: 0.3s; border: none;
    }
    .stButton>button:hover { background: #2ea043; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>🧬 MEDICAL ARCHIVE v21.0: THE ULTIMATE</h1><p>En Detaylı Tanı, Tetkik ve Tedavi Matrisi | İSMAİL ORHAN Edition</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL
with st.sidebar:
    st.header("👤 HASTA TERMİNALİ")
    h_ad = st.text_input("Hasta Tanımlayıcı", "H-2026-X")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 250, 75)
    st.divider()
    ates = st.number_input("Ateş (°C)", 30.0, 45.0, 36.6, format="%.1f")
    ta_sis = st.number_input("Sistolik TA", 40, 280, 120)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.success(f"Hesaplanan eGFR: {egfr}")

# 4. EN DETAYLI SEMPTOM LİSTESİ
st.subheader("🔍 Klinik Bulguları Eksiksiz Seçiniz")
c1, c2, c3, c4 = st.columns(4)

with c1:
    b1 = st.multiselect("Gastro / Hepato", ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Melena", "Murphy (+)", "Karın Ağrısı", "Disfaji", "Karahindiba Görünümü", "Caput Medusae"])
with c2:
    b2 = st.multiselect("Kardiyo / Pulmoner", ["Göğüs Ağrısı", "Nefes Darlığı", "Ortopne", "PND", "Bilateral Ödem", "Unilateral Ödem", "Hemoptizi", "Üfürüm", "S3/S4 Sesi", "Boyun Ven Dolgunluğu"])
with c3:
    b3 = st.multiselect("Nöro / Toksiko", ["Konfüzyon", "Ense Sertliği", "Fokal Defisit", "Ani Baş Ağrısı", "Nöbet", "Miyozis", "Midriyazis", "Hipersalivasyon", "Tremor", "Ataksi"])
with c4:
    b4 = st.multiselect("Sistemik / Diğer", ["Peteşi/Purpura", "Lenfadenopati", "Kelebek Döküntü", "Oral Aft", "Genital Ülser", "Eklem Ağrısı", "Poliüri", "Polidipsi", "Aseton Kokusu", "Gece Terlemesi"])

hepsi = b1 + b2 + b3 + b4

# 5. DEVASA TIP ARŞİVİ (MATRİS YAPISI)
tıp_arsivi = {
    "Siroz / Karaciğer Yetmezliği": {
        "bulgular": ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Melena", "Caput Medusae"],
        "tetkik": "AST/ALT, Albümin, PT/INR, Amonyak, Batın Doppler USG, Endoskopi.",
        "tedavi": "Sıvı/Tuz kısıtlaması, IV Albümin (parasentez sonrası), Laktüloz, Beta-bloker (Varis için)."
    },
    "Sağ Kalp Yetmezliği": {
        "bulgular": ["Bilateral Ödem", "Hepatomegali", "Asit", "Boyun Ven Dolgunluğu", "S3/S4 Sesi"],
        "tetkik": "EKO (Sağ ventrikül genişliği), NT-proBNP, EKG, Akciğer Grafisi.",
        "tedavi": "IV Diüretik (Furosemid), Kısıtlı sıvı alımı, Altta yatan akciğer hastalığı tedavisi."
    },
    "Malignite / Lenfoma": {
        "bulgular": ["Lenfadenopati", "Splenomegali", "Hepatomegali", "Gece Terlemesi", "Kilo Kaybı"],
        "tetkik": "LN Biyopsisi (Altın standart), Tam Kan Sayımı, LDH, Periferik Yayma, PET-CT.",
        "tedavi": "Onkoloji konsültasyonu, Kemoterapi/Radyoterapi protokolleri."
    },
    "Budd-Chiari Sendromu": {
        "bulgular": ["Asit", "Hepatomegali", "Karın Ağrısı"],
        "tetkik": "Doppler USG (Hepatik ven trombozu), Batın BT/MR anjiyo.",
        "tedavi": "Antikoagülasyon, Trombolitik tedavi, TIPS veya Cerrahi dekompresyon."
    },
    "Enfektif Endokardit": {
        "bulgular": ["Ateş", "Üfürüm", "Peteşi/Purpura", "Splenomegali"],
        "tetkik": "3 set Kan Kültürü, TEE (Transözofageal EKO), CRP/Sedim, EKG.",
        "tedavi": "IV Uzun süreli antibiyoterapi (Kültür duyarlılığına göre), Cerrahi kapak değişimi."
    },
    "Diyabetik Ketoasidoz": {
        "bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Karın Ağrısı"],
        "tetkik": "Glukoz, Kan Gazı (Metabolik Asidoz), Ketonyüri, Elektrolit (K+).",
        "tedavi": "IV İzotonik, IV İnsülin İnfüzyonu, Potasyum takviyesi."
    },
    "Sistemik Lupus (SLE)": {
        "bulgular": ["Kelebek Döküntü", "Eklem Ağrısı", "Plevritik Ağrı", "Peteşi/Purpura"],
        "tetkik": "ANA, Anti-dsDNA, Anti-Smith, C3/C4, Tam İdrar Tetkiki.",
        "tedavi": "Hidroksiklorokin, Steroidler, İmmünsupresif tedavi."
    }
}

# 6. ANALİZ VE RAPORLAMA
if st.button("🚀 OMNI-ARŞİV ANALİZİNİ BAŞLAT"):
    if not hepsi:
        st.error("Lütfen klinik bulgu seçiniz.")
    else:
        st.divider()
        bulunanlar = []
        for h, v in tıp_arsivi.items():
            eslesme = set(hepsi).intersection(set(v["bulgular"]))
            if eslesme:
                puan = round((len(eslesme) / len(v["bulgular"])) * 100, 1)
                bulunanlar.append({"isim": h, "puan": puan, "veri": v, "eslesen": list(eslesme)})
        
        bulunanlar = sorted(bulunanlar, key=lambda x: x['puan'], reverse=True)
        
        col_res1, col_res2 = st.columns([1.3, 1])
        
        with col_res1:
            st.markdown("### 🧬 Klinik Eşleşme Sonuçları")
            for b in bulunanlar:
                with st.container():
                    st.markdown(f"""
                    <div class='diag-card'>
                        <div class='section-title'>{b['isim']} (Uyum: %{b['puan']})</div>
                        <p>✅ <b>Tespit Edilen:</b> {", ".join(b['eslesen'])}</p>
                        <p style='color:#a5d6ff'>🔬 <b>Tetkik:</b> {b['veri']['tetkik']}</p>
                        <p style='color:#aff5b4'>💊 <b>Tedavi:</b> {b['veri']['tedavi']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        with col_res2:
            st.markdown("### 📝 RESMİ EPİKRİZ ÇIKTISI")
            epikriz_metni = f"""KLİNİK RAPOR ÖZETİ
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
HASTA ID: {h_ad} | YAŞ: {yas} | KİLO: {kilo}kg
eGFR: {egfr} mL/dk | RADYOLOJİ: {"Kontrast Uygundur" if egfr > 60 else "Kontrastsız Tercih Edilmeli"}

[SEÇİLEN BULGULAR]
{", ".join(hepsi)}

[AYIRICI TANI VE OLASILIKLAR]
{chr(10).join([f"- {i['isim']} (%{i['puan']} uyum)" for i in bulunanlar[:5]])}

[TEDAVİ VE TETKİK PLANI]
{chr(10).join([f"* {i['isim']} için: {i['veri']['tetkik']}" for i in bulunanlar[:2]])}

--------------------------------------------------
Sistem Sorumlusu: İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz_metni}</pre></div>", unsafe_allow_html=True)
            st.download_button("Raporu İndir", epikriz_metni, file_name=f"{h_ad}_medical_archive.txt")

st.markdown("---")
st.caption("v21.0 | The Medical Archive | İsmail Orhan")
