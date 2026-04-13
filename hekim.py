import streamlit as st
from datetime import datetime

# 1. SAYFA KONFİGÜRASYONU VE ULTRA PREMİUM KLİNİK TEMA
st.set_page_config(page_title="Tıbbi Karar Destek Sistemi - İsmail Orhan", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010409; color: #c9d1d9; }
    .main-header {
        background: linear-gradient(135deg, #0d1117 0%, #1c2128 100%); padding: 50px;
        border-radius: 20px; text-align: center; border: 1px solid #30363d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 30px;
    }
    .diag-card { 
        background: #0d1117; border: 1px solid #30363d; 
        padding: 25px; border-radius: 15px; margin-bottom: 20px;
        border-left: 12px solid #238636;
    }
    .section-title { color: #58a6ff; font-weight: 900; font-size: 1.5em; margin-bottom: 12px; text-transform: uppercase; }
    .epikriz-paper { 
        background: #ffffff; color: #000; padding: 45px; border-radius: 5px; 
        font-family: 'Courier New', monospace; border: 4px solid #000; line-height: 1.3;
    }
    .stButton>button {
        background: linear-gradient(90deg, #238636, #2ea043); color: white; border-radius: 15px; 
        height: 6em; width: 100%; font-weight: 900; font-size: 26px; border: none;
        box-shadow: 0 8px 15px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>🌐 TIBBİ ANALİZ VE KLİNİK ARŞİV TERMİNALİ</h1><p>Maksimum Veri Havuzu | Tüm Branşlar | Dinamik Tanı Matrisi | İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL - GENİŞLETİLMİŞ VİTAL TERMİNAL
with st.sidebar:
    st.header("📋 VİTAL PARAMETRELER")
    h_ad = st.text_input("Hasta Protokol No", "P-2026-FINAL")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 220, 75)
    st.divider()
    ates = st.number_input("Ateş (°C)", 32.0, 45.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 40, 300, 120)
    seker = st.number_input("Kan Şekeri (mg/dL)", 20, 1000, 100) # İsteğin üzerine eklendi
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    
    # Gelişmiş Hesaplamalar
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.subheader(f"eGFR: {egfr} ml/dk")
    if seker > 250: st.warning("⚠️ HİPERGLİSEMİ (DKA Riski)")
    if seker < 70: st.error("🚨 HİPOGLİSEMİ ALARMI")

# 4. EN GENİŞ SEMPTOM VE KLİNİK BULGU HAVUZU (MAX KATEGORİ)
st.subheader("🔍 Klinik Bulguları ve Sistem Sorgusunu Eksiksiz Seçiniz")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🩺 DAHİLİ SİSTEMLER", "🧠 NÖRO & PSİKO", "🧬 HEMATO & ROMATO", "☣️ TOKSİKO & ENFEKSİYON", "🧪 ENDOKRİN & RENAL"])

hepsi = []
with tab1:
    col_a, col_b = st.columns(2)
    hepsi.extend(col_a.multiselect("Gastroenteroloji", ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Melena", "Caput Medusae", "Murphy (+)", "Karahindiba Görünümü", "Disfaji", "Karın Ağrısı"]))
    hepsi.extend(col_b.multiselect("Kardiyo & Solunum", ["Göğüs Ağrısı (Baskı)", "Bilateral Ödem", "Unilateral Ödem", "Ortopne", "PND", "Hemoptizi", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Plevritik Ağrı", "Ral/Ronküs", "Stridor"]))
with tab2:
    hepsi.extend(st.multiselect("Nörolojik Bulgular", ["Konfüzyon", "Ense Sertliği", "Fokal Güç Kaybı", "Nöbet", "Ani Şiddetli Baş Ağrısı", "Tremor", "Ataksi", "Afazi", "Diplopi"]))
with tab3:
    hepsi.extend(st.multiselect("Hematoloji & Romatoloji", ["Peteşi/Purpura", "Lenfadenopati", "Kelebek Döküntü", "Oral Aft", "Genital Ülser", "Eklem Ağrısı", "Sabah Sertliği", "Splenomegali (Masif)", "Raynaud Fenomeni"]))
with tab4:
    hepsi.extend(st.multiselect("Enfeksiyon & Toksikoloji", ["Miyozis", "Midriyazis", "Hipersalivasyon", "Gece Terlemesi", "Kilo Kaybı (İstemsiz)", "Lenfadenopati (Ağrılı)", "Bradikardi", "Taşikardi"]))
with tab5:
    hepsi.extend(st.multiselect("Endokrin & Renal", ["Aseton Kokusu", "Poliüri", "Polidipsi", "Oligüri", "Anüri", "Ekzoftalmi", "Hiperpigmentasyon", "Aydede Yüzü", "Mor Stria"]))

# 5. DEVASA TIP ARŞİVİ (ULTIMATE MATRIX)
tıp_arsivi = {
    "Siroz ve Portal Hipertansiyon": {
        "bulgular": ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Melena", "Caput Medusae", "Karahindiba Görünümü"],
        "tetkik": "ALT/AST, Albümin, PT/INR, Amonyak, Batın Doppler USG, Gastroskopi.",
        "tedavi": "Sodyum kısıtlaması, Spironolakton, Laktüloz, IV Albümin.",
        "radyoloji": "Kontrastsız Batın BT, Portal Ven Doppleri."
    },
    "Akut Koroner Sendrom": {
        "bulgular": ["Göğüs Ağrısı (Baskı)", "Taşikardi", "Terleme"],
        "tetkik": "EKG, Seri Troponin, EKO, CK-MB.",
        "tedavi": "ASA 300mg, Klopidogrel 600mg, Heparin, Nitrat.",
        "radyoloji": "Koroner Anjiyografi."
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Karın Ağrısı", "Konfüzyon"],
        "tetkik": "Kan Şekeri (>250), Kan Gazı (pH <7.3), Ketonyüri, Anyon Açığı.",
        "tedavi": "IV %0.9 SF (Agresif Hidrasyon), IV İnsülin İnfüzyonu, K+ Replasmanı.",
        "radyoloji": "PA AC Grafisi (Enfeksiyon odağı tarama)."
    },
    "Konjesif Kalp Yetmezliği": {
        "bulgular": ["Bilateral Ödem", "Ortopne", "PND", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Hepatomegali"],
        "tetkik": "NT-proBNP, Transtorasik EKO, Akciğer Grafisi, EKG.",
        "tedavi": "IV Furosemid, ACE İnhibitörü/ARNI, Beta-Bloker.",
        "radyoloji": "Telekardiyografi (Kardiyomegali, Vasküler Belirginleşme)."
    },
    "Pulmoner Emboli": {
        "bulgular": ["Hemoptizi", "Plevritik Ağrı", "Unilateral Ödem", "Taşikardi", "Ani Nefes Darlığı"],
        "tetkik": "D-Dimer, Kan Gazı, EKG (S1Q3T3), EKO.",
        "tedavi": "Antikoagülasyon (DMAH), Trombolitik Tedavi (Masifse).",
        "radyoloji": "BT Pulmoner Anjiyografi (Altın Standart)."
    },
    "Organofosfat Zehirlenmesi": {
        "bulgular": ["Miyozis", "Hipersalivasyon", "Ral/Ronküs", "Karın Ağrısı", "Bradikardi"],
        "tetkik": "Plazma Kolinesteraz Düzeyi.",
        "tedavi": "ACİL ATROPİN (Yanıt alana kadar), PAM (Pralidoksim).",
        "radyoloji": "PA AC Grafisi."
    },
    "Malignite / Lenfoma": {
        "bulgular": ["Lenfadenopati", "Splenomegali", "Gece Terlemesi", "Kilo Kaybı (İstemsiz)"],
        "tetkik": "LN Biyopsisi, LDH, Periferik Yayma, Sedim.",
        "tedavi": "Onkoloji Konsültasyonu, Kemoterapi.",
        "radyoloji": "PET-CT, Kontrastlı Tüm Batın/Toraks BT."
    },
    "Sistemik Lupus (SLE)": {
        "bulgular": ["Kelebek Döküntü", "Eklem Ağrısı", "Oral Aft", "Plevritik Ağrı"],
        "tetkik": "ANA, Anti-dsDNA, C3/C4, Tam İdrar Tetkiki.",
        "tedavi": "Hidroksiklorokin, Steroidler, İmmünsupresifler.",
        "radyoloji": "Renal USG, Eklem USG."
    },
    "Bakteriyel Menenjit": {
        "bulgular": ["Ense Sertliği", "Ani Şiddetli Baş Ağrısı", "Konfüzyon", "Ateş"],
        "tetkik": "Lomber Ponksiyon (LP), BOS Kültürü, Kan Kültürü.",
        "tedavi": "IV Sefotaksim/Seftriakson + Vankomisin + Deksametazon.",
        "radyoloji": "LP Öncesi KİBAS ekarte etmek için Beyin BT."
    }
}

# 6. ANALİZ VE EPİKRİZ MOTORU
if st.button("🚀 MAKSİMUM ANALİZİ BAŞLAT VE ARŞİVLE"):
    if not hepsi:
        st.error("Hata: Herhangi bir klinik bulgu seçilmedi. Lütfen sistem sorgusunu tamamlayın.")
    else:
        st.divider()
        sonuclar = []
        
        # Matematiksel Eşleşme Analizi
        for hastalik, data in tıp_arsivi.items():
            eslesme = set(hepsi).intersection(set(data["bulgular"]))
            if eslesme:
                puan = round((len(eslesme) / len(data["bulgular"])) * 100, 1)
                sonuclar.append({"ad": hastalik, "skor": puan, "detay": data, "eslesen": list(eslesme)})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['skor'], reverse=True)

        col_1, col_2 = st.columns([1.4, 1])

        with col_1:
            st.markdown("### 🧬 Klinik Matris Analizi")
            if not sonuclar:
                st.info("Seçilen bulgular spesifik bir tanıya %100 uymuyor. Ayırıcı tanılar üzerinden ilerleyiniz.")
            else:
                for s in sonuclar:
                    with st.container():
                        st.markdown(f"""
                        <div class='diag-card'>
                            <div class='section-title'>{s['ad']} (Uyumluluk: %{s['skor']})</div>
                            <p><b>🔍 Eşleşen Bulgular:</b> {", ".join(s['eslesen'])}</p>
                            <p style='color:#a5d6ff'><b>🔬 Tetkik Rehberi:</b> {s['detay']['tetkik']}</p>
                            <p style='color:#aff5b4'><b>💊 Tedavi Protokolü:</b> {s['detay']['tedavi']}</p>
                            <p style='color:#ffa8a8'><b>📡 Radyoloji Planı:</b> {s['detay']['radyoloji']}</p>
                        </div>
                        """, unsafe_allow_html=True)

        with col_2:
            st.markdown("### 📝 RESMİ KLİNİK EPİKRİZ")
            radyo_not = "Kontrastlı tetkik uygundur." if egfr > 60 else "⚠️ DİKKAT: eGFR < 60, Kontrastsız tetkik veya hidrasyon zorunludur!"
            
            epikriz_final = f"""KLİNİK RAPOR VE TEDAVİ ÖZETİ
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
HASTA ID: {h_ad} | YAŞ: {yas} | KİLO: {kilo}kg
KAN ŞEKERİ: {seker} mg/dL | eGFR: {egfr} ml/dk

[VİTAL ANALİZ VE RADYOLOJİ GÜVENLİĞİ]
- {radyo_not}
- {"Diyabetik acil açısından dikkat!" if seker > 250 or seker < 70 else "Kan şekeri stabil."}

[SİSTEMİK BULGULAR]
{", ".join(hepsi)}

[OLASI TANILAR VE AYIRICI TANI]
{chr(10).join([f"- {res['ad']} (Skor: %{res['skor']})" for res in sonuclar[:5]])}

[İLK BASAMAK PLAN]
{chr(10).join([f"* {res['ad']} için: {res['detay']['tetkik'][:120]}..." for res in sonuclar[:2]])}

--------------------------------------------------
ONAY: SİSTEM SORUMLUSU İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz_final}</pre></div>", unsafe_allow_html=True)
            st.download_button("📥 Raporu Arşivle (.txt)", epikriz_final, file_name=f"{h_ad}_final_report.txt")

st.markdown("---")
st.caption("The Medical Archive Ultimate | Tüm Branşlar & Dinamik Matris | İSMAİL ORHAN")
