import streamlit as st
from datetime import datetime

# 1. SAYFA KONFİGÜRASYONU VE SİBER KLİNİK TEMA
st.set_page_config(page_title="Tıbbi Karar Destek Sistemi - İsmail Orhan", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010409; color: #c9d1d9; }
    .main-header {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); padding: 40px;
        border-radius: 20px; text-align: center; border: 2px solid #30363d;
        box-shadow: 0 4px 25px rgba(0,0,0,1); margin-bottom: 30px;
    }
    .diag-card { 
        background: #0d1117; border: 1px solid #30363d; 
        padding: 25px; border-radius: 15px; margin-bottom: 20px;
        border-left: 10px solid #238636;
    }
    .section-title { color: #58a6ff; font-weight: 900; font-size: 1.4em; margin-bottom: 12px; }
    .epikriz-paper { 
        background: #ffffff; color: #000; padding: 40px; border-radius: 5px; 
        font-family: 'Courier New', monospace; border: 3px solid #000;
    }
    .stButton>button {
        background: #238636; color: white; border-radius: 15px; height: 6em; width: 100%; 
        font-weight: 900; font-size: 24px; border: 2px solid #3fb950;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>⚖️ TIBBİ ANALİZ VE KLİNİK ARŞİV SİSTEMİ</h1><p>En Kapsamlı Tanı, Tetkik, Tedavi ve Epikriz Terminali | İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL - HASTA TERMİNALİ
with st.sidebar:
    st.header("📋 HASTA PROFİLİ")
    h_ad = st.text_input("Hasta Tanımlayıcı / Protokol", "PROTOKOL-2026")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 220, 75)
    st.divider()
    ates = st.number_input("Ateş (°C)", 32.0, 45.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 40, 300, 120)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    # Cockcroft-Gault
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.subheader(f"eGFR: {egfr} ml/dk")
    if egfr < 30: st.error("DİKKAT: İleri Derece Renal Yetmezlik")

# 4. DEVAŞA SEMPTOM VE KLİNİK BULGU PANELİ (TÜM BRANŞLAR)
st.subheader("🔍 Klinik Bulguları Eksiksiz ve Detaylı Seçiniz")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("**Gastroenteroloji & Hepatoloji**")
    g1 = st.multiselect("Sindirim Sistemi", ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Melena", "Murphy (+)", "Karahindiba Görünümü", "Caput Medusae", "Disfaji", "Karın Ağrısı"])
with c2:
    st.markdown("**Kardiyoloji & Pulmoner**")
    g2 = st.multiselect("Dolaşım & Solunum", ["Göğüs Ağrısı (Baskı)", "Bilateral Ödem", "Unilateral Ödem", "Ortopne", "PND", "Hemoptizi", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Plevritik Ağrı", "Ral/Ronküs"])
with c3:
    st.markdown("**Nöroloji & Toksikoloji**")
    g3 = st.multiselect("Bilinç & Sinir", ["Konfüzyon", "Ense Sertliği", "Fokal Defisit", "Nöbet", "Miyozis", "Midriyazis", "Hipersalivasyon", "Ani Şiddetli Baş Ağrısı", "Tremor", "Ataksi"])
with c4:
    st.markdown("**Hematoloji & Romatoloji**")
    g4 = st.multiselect("Sistemik & Bağ Dokusu", ["Peteşi/Purpura", "Lenfadenopati", "Kelebek Döküntü", "Oral Aft", "Genital Ülser", "Eklem Ağrısı", "Poliüri", "Polidipsi", "Aseton Kokusu", "Gece Terlemesi", "Kilo Kaybı"])

hepsi = g1 + g2 + g3 + g4

# 5. TÜM TIP ARŞİVİ (EN DETAYLI MATRİS)
# Her hastalık için; bulgu, ayırıcı tanı, tetkik, tedavi ve radyoloji bilgileri eklendi.
tıp_arsivi = {
    "Siroz ve Portal Hipertansiyon": {
        "bulgular": ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Melena", "Caput Medusae"],
        "tetkik": "AST/ALT, Albümin, PT/INR, Amonyak, Batın Doppler USG, Endoskopi (Varis tarama).",
        "tedavi": "Sodyum kısıtlaması, Spironolakton/Furosemid, IV Albümin (LVP sonrası), Laktüloz (Ensefalopati önlemi).",
        "radyoloji": "Kontrastsız Batın BT (HCC tarama için), Doppler USG (Hepatik ven akımı)."
    },
    "Akut Koroner Sendrom (STEMI/NSTEMI)": {
        "bulgular": ["Göğüs Ağrısı (Baskı)", "Bulantı", "Nefes Darlığı", "Terleme"],
        "tetkik": "12 Derivasyonlu EKG, Seri Troponin T/I, CK-MB, EKO.",
        "tedavi": "ASA 300mg (çiğnetme), Klopidogrel 300-600mg yükleme, Heparin/Deltaparin, IV Nitroglicerin.",
        "radyoloji": "Koroner Anjiyografi (Altın Standart)."
    },
    "Konjesif Kalp Yetmezliği": {
        "bulgular": ["Bilateral Ödem", "Hepatomegali", "Asit", "Ortopne", "PND", "Boyun Ven Dolgunluğu", "S3/S4 Sesi"],
        "tetkik": "NT-proBNP, Transtorasik EKO (EF tayini), Akciğer Grafisi, EKG.",
        "tedavi": "IV Furosemid, ACE İnhibitörü/ARNI, Beta-Bloker, SGLT2 İnhibitörü.",
        "radyoloji": "Telekardiyografi (Kardiyomegali, Kerley B çizgileri)."
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Karın Ağrısı"],
        "tetkik": "Kan Şekeri (>250 mg/dl), Kan Gazı (Metabolik Asidoz, pH < 7.3), Ketonyüri.",
        "tedavi": "IV %0.9 SF Hidrasyon, IV İnsülin İnfüzyonu (0.1 U/kg/sa), Potasyum Replasmanı.",
        "radyoloji": "Presipite eden faktör taraması için PA Akciğer Grafisi."
    },
    "Sistemik Lupus Eritematozus (SLE)": {
        "bulgular": ["Kelebek Döküntü", "Eklem Ağrısı", "Plevritik Ağrı", "Peteşi/Purpura", "Oral Aft"],
        "tetkik": "ANA, Anti-dsDNA, Anti-Smith, C3/C4, Tam İdrar (Proteinüri takibi).",
        "tedavi": "Hidroksiklorokin, Glukokortikoidler, Azatiyoprin/Mikofenolat Mofetil.",
        "radyoloji": "Gerektiğinde Toraks BT veya Renal USG."
    },
    "Organofosfat Zehirlenmesi": {
        "bulgular": ["Miyozis", "Hipersalivasyon", "Ral/Ronküs", "Karın Ağrısı", "Konfüzyon"],
        "tetkik": "Plazma ve Eritrosit Kolinesteraz Düzeyleri.",
        "tedavi": "ACİL ATROPİN (Yanıt alana kadar), Pralidoksim (PAM), IV Hidrasyon.",
        "radyoloji": "Aspirasyon Pnömonisi şüphesinde AC Grafisi."
    },
    "Budd-Chiari Sendromu": {
        "bulgular": ["Asit", "Hepatomegali", "Karın Ağrısı", "Sarılık"],
        "tetkik": "Batın Doppler USG, Protein C/S, Antitrombin III, Faktör V Leiden.",
        "tedavi": "Antikoagülasyon (Heparin/Varfarin), Trombolitik Tedavi, TIPS İşlemi.",
        "radyoloji": "Kontrastlı Batın BT (Hepatik venlerin doluşu)."
    },
    "Malignite / Lenfoma": {
        "bulgular": ["Lenfadenopati", "Splenomegali", "Gece Terlemesi", "Kilo Kaybı", "Hepatomegali"],
        "tetkik": "Eksizyonel LN Biyopsisi, Periferik Yayma, LDH, Sedimantasyon.",
        "tedavi": "Onkoloji Konsültasyonu, Kemoterapi (CHOP vb.), Radyoterapi.",
        "radyoloji": "Tüm Vücut PET-CT, Kontrastlı Boyun/Toraks/Batın BT."
    },
    "Pulmoner Emboli": {
        "bulgular": ["Nefes Darlığı", "Plevritik Ağrı", "Hemoptizi", "Unilateral Ödem", "Taşikardi"],
        "tetkik": "D-Dimer, Kan Gazı (Hipoksi/Hipokapni), EKO (Sağ yüklenme).",
        "tedavi": "Antikoagülasyon (Düşük molekül ağırlıklı heparin), Trombolitik (Şiddetliyse).",
        "radyoloji": "BT Pulmoner Anjiyografi (Altın Standart)."
    }
}

# 6. ANALİZ MOTORU VE ÇIKTI PANELİ
if st.button("🚀 OMNI-ARŞİV ANALİZİNİ VE EPİKRİZİ BAŞLAT"):
    if not hepsi:
        st.error("Lütfen klinik bulguları seçiniz! Analiz için veri gereklidir.")
    else:
        st.divider()
        olasiliklar = []
        
        # Matematiksel Matris Eşleşmesi
        for hastalik, veri in tıp_arsivi.items():
            eslesme = set(hepsi).intersection(set(veri["bulgular"]))
            if eslesme:
                puan = round((len(eslesme) / len(veri["bulgular"])) * 100, 1)
                olasiliklar.append({"ad": hastalik, "skor": puan, "detay": veri, "eslesen": list(eslesme)})
        
        # Skora göre sırala
        olasiliklar = sorted(olasiliklar, key=lambda x: x['skor'], reverse=True)

        if not olasiliklar:
            st.warning("Seçilen bulgulara uyan spesifik bir tanı bulunamadı. Lütfen daha fazla bulgu ekleyiniz.")
        else:
            col_a, col_b = st.columns([1.3, 1])
            
            with col_a:
                st.markdown("### 🧬 Klinik Eşleşme ve Tanı Raporu")
                for o in olasiliklar:
                    with st.container():
                        st.markdown(f"""
                        <div class='diag-card'>
                            <div class='section-title'>{o['ad']} (Uyum: %{o['skor']})</div>
                            <p><b>🔍 Eşleşen Bulgular:</b> {", ".join(o['eslesen'])}</p>
                            <p style='color:#a5d6ff'><b>🔬 Altın Standart Tetkikler:</b> {o['detay']['tetkik']}</p>
                            <p style='color:#aff5b4'><b>💊 İlk Basamak Tedavi:</b> {o['detay']['tedavi']}</p>
                            <p style='color:#ffadad'><b>📡 Radyoloji Rehberi:</b> {o['detay']['radyoloji']}</p>
                        </div>
                        """, unsafe_allow_html=True)

            with col_b:
                st.markdown("### 📝 RESMİ KLİNİK EPİKRİZ")
                radyo_guvenlik = "KONTRASTLI TETKİK UYGUNDUR" if egfr > 60 else "⚠️ DİKKAT: KONTRASSIZ TETKİK / HİDRASYON ÖNERİLİR!"
                
                epikriz_text = f"""KLİNİK DURUM RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
HASTA ID: {h_ad} | YAŞ: {yas} | KİLO: {kilo}kg
eGFR: {egfr} ml/dk | DURUM: {radyo_guvenlik}

[GÖZLEMLENEN BULGULAR]
{", ".join(hepsi)}

[AYIRICI TANI ANALİZİ]
{chr(10).join([f"- {i['ad']} (%{i['skor']} uyum)" for i in olasiliklar[:5]])}

[ÖNERİLEN TETKİK VE TEDAVİ PLANI]
{chr(10).join([f"* {i['ad']} Şüphesi İçin: {i['detay']['tetkik']}" for i in olasiliklar[:2]])}

--------------------------------------------------
SİSTEM SORUMLUSU: İSMAİL ORHAN
"""
                st.markdown(f"<div class='epikriz-paper'><pre>{epikriz_text}</pre></div>", unsafe_allow_html=True)
                st.download_button("📤 Raporu PDF Olarak Kaydet", epikriz_text, file_name=f"{h_ad}_klinik_arsiv.txt")

st.markdown("---")
st.caption("Medical Archive Ultimate Edition | Tüm Branşlar ve Matris Analizi | İSMAİL ORHAN")
