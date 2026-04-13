import streamlit as st
from datetime import datetime

# 1. TASARIM: ELİT KLİNİK KOMUTA MERKEZİ
st.set_page_config(page_title="Omni-Clinical Archive - İsmail Orhan", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010409; color: #c9d1d9; }
    .main-header {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%); padding: 40px;
        border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 25px;
    }
    .diag-card { 
        background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 15px;
        border-left: 8px solid #238636; box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    .warning-card { border-left: 8px solid #d73a49; background: rgba(215, 58, 73, 0.1); }
    .section-title { color: #58a6ff; font-weight: 800; font-size: 1.3em; margin-bottom: 8px; }
    .stButton>button {
        background: #238636; color: white; border-radius: 8px; height: 4em; width: 100%; 
        font-weight: 700; font-size: 20px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>🧪 OMNI-CLINICAL ARCHIVE & CDSS</h1><p>En Geniş Dahiliye Kütüphanesi | İSMAİL ORHAN | 2026</p></div>", unsafe_allow_html=True)

# 3. VİTAL VE SKORLAMA PANELİ
with st.sidebar:
    st.header("📊 HASTA VERİ TERMİNALİ")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 220, 75)
    st.divider()
    ates = st.number_input("Ateş (°C)", 32.0, 43.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA", 40, 300, 120)
    seker = st.number_input("Glukoz (mg/dL)", 20, 1000, 100)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    
    st.metric("eGFR", f"{egfr} ml/dk")
    if egfr < 15: st.error("DİKKAT: EVRE 5 KRY (DİYALİZ?)")
    if seker > 300: st.warning("KETONYÜRİ BAKILMALI!")

# 4. SİSTEMİK SORGULAMA (MAKSİMUM DETAY)
st.subheader("🔍 Klinik Bulgular (Tüm Branşlar Senkronize)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    s1 = st.multiselect("GİS / HEPATO", ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Hematemez", "Melena", "Caput Medusae", "Murphy (+)", "Karahindiba Görünümü", "Karın Ağrısı (Kuşak)", "Asteriksis"])
with col2:
    s2 = st.multiselect("KARDİYO / GÖĞÜS", ["Göğüs Ağrısı", "Ortopne", "PND", "Bilateral Ödem", "Unilateral Ödem", "Hemoptizi", "Boyun Ven Dolgunluğu", "Ral/Ronküs", "Wheezing", "Öksürük (Gece)"])
with col3:
    s3 = st.multiselect("NÖRO / TOKSİKO", ["Konfüzyon", "Ense Sertliği", "Miyozis", "Midriyazis", "Hipersalivasyon", "Tremor", "Nöbet", "Fokal Kayıp", "Ani Baş Ağrısı"])
with col4:
    s4 = st.multiselect("DİĞER / NADİR", ["Peteşi/Purpura", "Lenfadenopati", "Kelebek Döküntü", "Oral/Genital Ülser", "Poliüri", "Aseton Kokusu", "Gece Terlemesi", "Hiperpigmentasyon", "Kilo Kaybı"])

hepsi = s1 + s2 + s3 + s4

# 5. MAKSİMUM VERİ KÜTÜPHANESİ
# Buraya her branştan en detaylı hastalıkları ekledim.
arsiv = {
    "Karaciğer Sirozu": {
        "bulgular": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"],
        "tetkik": "INR, Albümin, Amonyak, Batın USG, Endoskopi.",
        "tedavi": "Laktüloz, Spironolakton, Tuz kısıtlı diyet."
    },
    "Akut Pankreatit": {
        "bulgular": ["Karın Ağrısı (Kuşak)", "Bulantı", "Hipotansiyon"],
        "tetkik": "Serum Amilaz/Lipaz (3 kat artış), Üst Batın BT.",
        "tedavi": "IV Hidrasyon (Agresif), Analjezi, Oral alım stop."
    },
    "Feokromositoma": {
        "bulgular": ["Ani Baş Ağrısı", "Terleme", "Çarpıntı", "Hipertansiyon"],
        "tetkik": "24 saatlik idrarda Metanefrin/Normetanefrin, Sürrenal BT.",
        "tedavi": "Alfa-Bloker sonrası Beta-Bloker, Cerrahi."
    },
    "Tüberküloz (AC)": {
        "bulgular": ["Gece Terlemesi", "Kilo Kaybı", "Hemoptizi", "Öksürük (Gece)"],
        "tetkik": "Balgamda ARB, Akciğer Grafisi (Kavite), PPD/IGRA.",
        "tedavi": "Dörtlü Anti-TBC (EİRP) protokolü."
    },
    "Nefrotik Sendrom": {
        "bulgular": ["Bilateral Ödem", "Asit", "Poliüri"],
        "tetkik": "24 saatlik idrarda protein (>3.5g), Albümin düşüklüğü.",
        "tedavi": "Steroid, ACE İnhibitörü, Diüretik."
    },
    "Enfektif Endokardit": {
        "bulgular": ["Ateş", "Peteşi/Purpura", "Splenomegali", "Üfürüm"],
        "tetkik": "Kan Kültürü, EKO (Vejetasyon), Duke Kriterleri.",
        "tedavi": "Uzun süreli IV Antibiyoterapi."
    }
}

# 6. ANALİZ VE ÇIKTI
if st.button("🚀 OMNI-ARŞİV SORGUSUNU BAŞLAT"):
    if not hepsi:
        st.error("Lütfen belirti giriniz.")
    else:
        sonuclar = []
        for ad, data in arsiv.items():
            eslesme = set(hepsi).intersection(set(data["bulgular"]))
            if eslesme:
                puan = round((len(eslesme) / len(data["bulgular"])) * 100, 1)
                sonuclar.append({"ad": ad, "skor": puan, "veri": data, "eslesen": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['skor'], reverse=True)

        res1, res2 = st.columns([1.2, 1])
        with res1:
            st.markdown("### 🧬 Klinik Matris Sonuçları")
            for s in sonuclar:
                is_danger = s['skor'] > 70
                card_class = "diag-card warning-card" if is_danger else "diag-card"
                st.markdown(f"""
                <div class='{card_class}'>
                    <div class='section-title'>{s['ad']} (%{s['skor']} Uyum)</div>
                    <p><b>Eşleşen:</b> {", ".join(s['eslesen'])}</p>
                    <p style='color:#a5d6ff'><b>Tetkik:</b> {s['veri']['tetkik']}</p>
                    <p style='color:#aff5b4'><b>Tedavi:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)

        with res2:
            st.markdown("### 📝 RESMİ EPİKRİZ")
            rad = "Kontrastlı uygundur" if egfr > 60 else "KONTRASSIZ TETKİK ÖNERİLİR"
            epikriz = f"""TIBBİ DURUM ÖZETİ
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y')}
Glikoz: {seker} mg/dL | eGFR: {egfr} ml/dk
Radyoloji Notu: {rad}

[BELİRTİLER]
{", ".join(hepsi)}

[AYIRICI TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['skor']})" for x in sonuclar[:3]])}

[PLAN]
- Hastanın vital bulguları ve belirtileri ışığında ileri tetkik planlanmıştır.

--------------------------------------------------
SİSTEM SORUMLUSU: İSMAİL ORHAN
"""
            st.markdown(f"<div style='background:white; color:black; padding:20px; font-family:monospace; border:2px solid black;'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("Dosyayı Kaydet", epikriz, "hasta_rapor.txt")

st.markdown("---")
st.caption("İSMAİL ORHAN | Medical CDSS Final Edition")
