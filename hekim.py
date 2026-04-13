import streamlit as st
from datetime import datetime

# 1. TASARIM: SİBERNETİK TIP ARAYÜZÜ
st.set_page_config(page_title="Medical Singularity v19", page_icon="♾️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #04070b; color: #e2e8f0; }
    .main-header {
        background: linear-gradient(90deg, #1e3a8a, #4338ca); padding: 40px;
        border-radius: 20px; text-align: center; border-bottom: 5px solid #6366f1;
    }
    .diagnosis-card { background: #111827; border: 1px solid #374151; padding: 20px; border-radius: 15px; margin-bottom: 10px; }
    .danger-text { color: #ef4444; font-weight: bold; }
    .success-text { color: #10b981; font-weight: bold; }
    .epikriz-paper { background: #f8fafc; color: #0f172a; padding: 30px; border-radius: 5px; font-family: 'Courier New', monospace; box-shadow: inset 0 0 10px rgba(0,0,0,0.1); }
    .stButton>button { background: #6366f1; color: white; border-radius: 10px; height: 4em; width: 100%; font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>♾️ THE MEDICAL SINGULARITY v19.0</h1><p>Tüm Tıbbi Branşlar | Dinamik Matris Analizi | İSMAİL ORHAN Global Edition</p></div>", unsafe_allow_html=True)

# 3. VERİ GİRİŞİ (VİTALLER)
with st.sidebar:
    st.header("📋 HASTA TERMİNALİ")
    h_ad = st.text_input("Hasta Tanımlayıcı", "H-2026")
    yas = st.number_input("Yaş", 0, 120, 45)
    st.divider()
    ates = st.number_input("Ateş (°C)", 30.0, 45.0, 36.6)
    ta_sis = st.number_input("Sistolik TA", 40, 280, 120)
    spo2 = st.slider("SpO2 (%)", 30, 100, 98)
    kreatinin = st.number_input("Kreatinin", 0.1, 15.0, 1.0)

# 4. DEVASA SEMPTOM HAVUZU (Branş Branş)
st.subheader("🧬 Multidisipliner Semptom Seçimi")
col1, col2, col3 = st.columns(3)

with col1:
    gastro = st.multiselect("GİS & Karaciğer", ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Melena", "Karın Ağrısı", "Hıçkırık", "Karahindiba Görünümü"])
    kardiyo = st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Ortopne", "PND", "Ödem (Bilateral)", "Ödem (Unilateral)", "Çarpıntı", "Üfürüm", "S3/S4 Sesi"])
with col2:
    solunum = st.multiselect("Solunum Sistemi", ["Öksürük", "Hemoptizi", "Wheezing", "Stridor", "Plevritik Ağrı", "Çomak Parmak"])
    noroloji = st.multiselect("Nöroloji & Psikiyatri", ["Konfüzyon", "Baş Ağrısı", "Ense Sertliği", "Nöbet", "Fokal Güç Kaybı", "Ataksi", "Tremor"])
with col3:
    endokrin = st.multiselect("Endokrin & Metabolizma", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Ekzoftalmi", "Hiperpigmentasyon", "Kilo Kaybı", "Kilo Artışı"])
    diger = st.multiselect("Hematoloji & Romatoloji", ["Peteşi/Purpura", "Lenfadenopati", "Kelebek Döküntü", "Oral Aft", "Eklem Ağrısı", "Sabah Sertliği"])

# Tüm seçilenleri birleştir
hepsi = gastro + kardiyo + solunum + noroloji + endokrin + diger

# 5. DİNAMİK TANI MATRİSİ (HİÇBİR ŞEYİ KAÇIRMAZ)
# Bu yapı, her bir belirtiyi ilgili olduğu tüm hastalıklarla eşleştirir.
hastalik_veritabanı = {
    "Siroz / Portal Hipertansiyon": ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Melena", "Karahindiba Görünümü"],
    "Konjesif Kalp Yetmezliği": ["Ödem (Bilateral)", "Ortopne", "PND", "Hepatomegali", "Asit", "S3/S4 Sesi"],
    "Akut Hepatit": ["Sarılık", "Hepatomegali", "Karın Ağrısı"],
    "Malignite (Primer/Metastatik)": ["Kilo Kaybı", "Hepatomegali", "Lenfadenopati", "Asit"],
    "Nefrotik Sendrom": ["Ödem (Bilateral)", "Asit", "Köpüklü İdrar"],
    "Pulmoner Emboli": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Ödem (Unilateral)"],
    "Diyabetik Ketoasidiz (DKA)": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon"],
    "Behçet Hastalığı": ["Oral Aft", "Eklem Ağrısı", "Genital Ülser"],
    "Sistemik Lupus (SLE)": ["Kelebek Döküntü", "Eklem Ağrısı", "Proteinüri", "Güneş Hassasiyeti"],
    "Bakteriyel Menenjit": ["Ense Sertliği", "Baş Ağrısı", "Ateş", "Konfüzyon"],
    "Organofosfat Zehirlenmesi": ["Miyozis", "Hipersalivasyon", "Karın Ağrısı", "Wheezing"]
}

# 6. ANALİZ VE RAPORLAMA
if st.button("🚀 MATRİS ANALİZİNİ ÇALIŞTIR"):
    if not hepsi:
        st.error("Lütfen en az bir belirti seçiniz!")
    else:
        st.divider()
        olasi_tanilar = []
        
        # Puanlama Sistemi: Seçilen belirtilerin kaç tanesi hastalıkla eşleşiyor?
        for hastalik, belirtiler in hastalik_veritabanı.items():
            eslesme = set(hepsi).intersection(set(belirtiler))
            if eslesme:
                skor = (len(eslesme) / len(belirtiler)) * 100
                olasi_tanilar.append({"isim": hastalik, "puan": round(skor, 1), "eslesen": list(eslesme)})

        # Puanı en yüksek olanı başa getir
        olasi_tanilar = sorted(olasi_tanilar, key=lambda x: x['puan'], reverse=True)

        res_col1, res_col2 = st.columns([1, 1.2])

        with res_col1:
            st.markdown("### 📊 Olasılık Bazlı Tanı Listesi")
            for t in olasi_tanilar:
                with st.container():
                    st.markdown(f"""
                    <div class='diagnosis-card'>
                        <span style='font-size:1.2em; color:#818cf8'><b>{t['isim']}</b></span><br>
                        <span class='success-text'>Uyumluluk: %{t['puan']}</span><br>
                        <small>Eşleşen Bulgular: {", ".join(t['eslesen'])}</small>
                    </div>
                    """, unsafe_allow_html=True)

        with res_col2:
            st.markdown("### 📝 Klinik Epikriz (Otomatik)")
            egfr = round(((140 - yas) * 75) / (72 * kreatinin), 1)
            epikriz_text = f"""KLİNİK RAPOR - {datetime.now().strftime('%d/%m/%Y')}
--------------------------------------------------
HASTA: {h_ad} | YAŞ: {yas} | eGFR: {egfr}

[VİTAL BULGULAR]
T: {ates}C | TA: {ta_sis}mmHg | SpO2: %{spo2}

[SEÇİLEN BULGULAR]
{", ".join(hepsi)}

[AYIRICI TANI ANALİZİ]
{chr(10).join([f"- {t['isim']} (%{t['puan']} uyum)" for t in olasi_tanilar[:5]])}

[RADYOLOJİ & LABORATUVAR ÖNERİSİ]
- Belirlenen ön tanılar doğrultusunda ileri tetkik planlanmıştır.
- eGFR {egfr} olduğundan {"kontrastlı tetkik uygundur" if egfr > 60 else "kontrastlı tetkikten kaçınılmalıdır"}.

--------------------------------------------------
Sistem: Medical Singularity v19 | Dr. İsmail Orhan
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz_text}</pre></div>", unsafe_allow_html=True)
            st.download_button("Raporu İndir", epikriz_text, file_name=f"{h_ad}_medical_report.txt")

st.markdown("---")
st.caption("v19.0 Medical Singularity | Tüm Tıp Branşları Aktif | Powered by Monster Tulpar")
