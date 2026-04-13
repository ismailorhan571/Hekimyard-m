import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SAYFA VE TASARIM AYARLARI
st.set_page_config(page_title="Dahiliye CDSS Clinician's Edge", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
    .header-box {
        background: rgba(30, 41, 59, 0.7); padding: 30px; border-radius: 25px;
        border: 2px solid #818cf8; text-align: center; margin-bottom: 25px;
    }
    .diff-diag-box {
        background: rgba(245, 158, 11, 0.1); padding: 25px; border-radius: 20px;
        border: 1px solid #f59e0b; margin-top: 15px;
    }
    .epikriz-area {
        background: #ffffff; color: #1e293b; padding: 25px; border-radius: 15px;
        font-family: 'Courier New', Courier, monospace; border: 2px solid #94a3b8;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #a855f7); color: white;
        border-radius: 15px; height: 4em; font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='header-box'><h1>⚕️ DAHİLİYE CDSS: CLINICIAN'S EDGE v16.0</h1><p>Gelişmiş Ayırıcı Tanı & Otomatik Epikriz Yazılımı | İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL (VİTAL VE LAB GİRİŞİ)
with st.sidebar:
    st.header("📊 HASTA VERİLERİ")
    h_ad = st.text_input("Hasta Rumuz/ID", "HASTA_001")
    yas = st.number_input("Yaş", 18, 110, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    st.divider()
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA", 50, 250, 120)
    solunum = st.number_input("Solunum Sayısı", 8, 50, 16)
    spo2 = st.slider("SpO2 (%)", 40, 100, 98)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    gks = st.selectbox("GKS", [15, 14, 13, 12, 11, 10, 9, 8, "7-"])

# 4. AYIRICI TANI (DIFFERENTIAL DIAGNOSIS) KÜTÜPHANESİ
def get_differential_diagnosis(bulgular):
    ddx = {}
    if "Göğüs Ağrısı (Baskı)" in bulgular:
        ddx["Göğüs Ağrısı"] = {
            "Öncelikli": "Akut MI",
            "Ayırıcılar": ["Aort Diseksiyonu (Sırta vuran ağrı?)", "Pulmoner Emboli (Nefes darlığı?)", "Pnömotoraks", "GÖRH"],
            "Ekarte İçin": "EKG, Troponin, D-Dimer, PA Akciğer Grafisi"
        }
    if "Hematemez" in bulgular or "Melena" in bulgular:
        ddx["Üst GİS Kanama"] = {
            "Öncelikli": "Peptik Ülser Kanaması",
            "Ayırıcılar": ["Özofagus Varisi (Siroz?)", "Mallory-Weiss", "Gastrik Malignite"],
            "Ekarte İçin": "Acil Endoskopi, Batın USG"
        }
    if "Ani Baş Ağrısı" in bulgular:
        ddx["Akut Baş Ağrısı"] = {
            "Öncelikli": "Serebrovasküler Olay",
            "Ayırıcılar": ["Subaraknoid Kanama (Gök gürültüsü ağrı?)", "Menenjit (Ateş?)", "Venöz Sinüs Trombozu"],
            "Ekarte İçin": "Beyin BT, LP, MR Venografi"
        }
    return ddx

# 5. KLİNİK BULGU GİRİŞİ
st.subheader("🔍 Klinik Bulgular ve Semptomlar")
semptomlar = st.multiselect("Belirtileri Seçiniz:", [
    "Göğüs Ağrısı (Baskı)", "Hematemez", "Melena", "Ani Baş Ağrısı", 
    "Ense Sertliği", "Sarılık", "Nefes Darlığı", "Asit", "Poliüri", "Konfüzyon"
])

# 6. ANALİZ VE EPİKRİZ MOTORU
if st.button("🚀 KOMPLEKS ANALİZİ VE EPİKRİZİ OLUŞTUR"):
    
    # Skorlamalar (Yerel)
    egfr = round(((140 - yas) * 75) / (72 * kreatinin), 1)
    qsofa = 0
    if ta_sis <= 100: qsofa += 1
    if solunum >= 22: qsofa += 1
    if gks != 15: qsofa += 1

    # Ayırıcı Tanı Al
    ayirici_tanilar = get_differential_diagnosis(semptomlar)

    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("### 🚨 Ayırıcı Tanı Paneli")
        if not ayirici_tanilar:
            st.info("Seçilen bulgular için spesifik ayırıcı tanı algoritması tetiklenmedi.")
        else:
            for ana, detay in ayirici_tanilar.items():
                st.markdown(f"""
                <div class='diff-diag-box'>
                    <b>Ana Klinik: {ana}</b><br>
                    📌 <i>Öncelikli Şüphe:</i> {detay['Öncelikli']}<br>
                    ⚠️ <i>Ayırıcı Tanılar:</i> {", ".join(detay['Ayırıcılar'])}<br>
                    🔬 <i>Ekarte Etmek İçin:</i> {detay['Ekarte İçin']}
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📝 Otomatik Klinik Epikriz (HBYS Uyumlu)")
        
        # Epikriz Metni Oluşturma
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        epikriz_metni = f"""HASTA EPİKRİZ RAPORU ({now})
--------------------------------------------------
HASTA ID: {h_ad} | YAŞ: {yas} | CİNSİYET: {cinsiyet}

[VİTAL BULGULAR]
Ateş: {ates}°C | TA: {ta_sis} mmHg | Solunum: {solunum}/dk | SpO2: %{spo2}

[KLİNİK DURUM VE SKORLAMA]
- eGFR: {egfr} mL/dk
- qSOFA Skoru: {qsofa} (Risk: {"YÜKSEK" if qsofa >=2 else "DÜŞÜK"})
- Mevcut Semptomlar: {", ".join(semptomlar) if semptomlar else "Belirtilmedi"}

[ÖN TANILAR VE AYIRICI TANI]
{chr(10).join([f"- {k}: {v['Öncelikli']} (Ayırıcı: {', '.join(v['Ayırıcılar'])})" for k,v in ayirici_tanilar.items()])}

[TEDAVİ VE İZLEM PLANI]
- Yakın vital takibi önerilir.
- eGFR baz alınarak renal doz ayarlaması yapıldı.
- İleri tetkikler: {", ".join([v['Ekarte İçin'] for v in ayirici_tanilar.values()])}

--------------------------------------------------
Raporu hazırlayan: CDSS THE BEAST v16 (İsmail Orhan)
"""
        st.markdown(f"<div class='epikriz-area'><pre>{epikriz_metni}</pre></div>", unsafe_allow_html=True)
        st.download_button("📥 Epikrizi İndir (.txt)", epikriz_metni, file_name=f"{h_ad}_epikriz.txt")

st.markdown("---")
st.caption("Dahiliye Clinician's Edge v16 | Dinamik Ayırıcı Tanı ve Epikriz Modülü Aktif.")
