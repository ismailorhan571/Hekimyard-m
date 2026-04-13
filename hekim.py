import streamlit as st
from datetime import datetime

# 1. TASARIM: TIBBİ OPERASYON MERKEZİ
st.set_page_config(page_title="İSMAİL ORHAN | Omni-Medical Command", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010409; color: #e2e8f0; }
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%); padding: 40px;
        border-radius: 15px; text-align: center; border: 2px solid #312e81; margin-bottom: 25px;
    }
    .diag-card { 
        background: #0d1117; border: 1px solid #30363d; padding: 25px; border-radius: 12px; 
        margin-bottom: 15px; border-left: 10px solid #238636;
    }
    .critical-alert { 
        background: rgba(215, 58, 73, 0.25); border: 2px solid #f85149; 
        color: #ff7b72; padding: 15px; border-radius: 10px; font-weight: bold; margin-bottom: 10px;
    }
    .epikriz-paper { 
        background: #ffffff; color: #0f172a; padding: 40px; border-radius: 5px; 
        font-family: 'Courier New', monospace; border: 2px solid #000; line-height: 1.4;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1d4ed8, #1e40af); color: white; border-radius: 12px; 
        height: 5em; width: 100%; font-weight: 800; font-size: 24px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>🏛️ OMNI-MEDICAL COMMAND CENTER</h1><p>Full-Scale Dahiliye Kütüphanesi & Karar Destek Üssü | İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 3. AKILLI TERMİNAL (YAN PANEL)
with st.sidebar:
    st.header("📋 HASTA PARAMETRELERİ")
    h_ad = st.text_input("Protokol No", "FINAL-2026")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 220, 75)
    st.divider()
    seker = st.number_input("Glukoz (mg/dL)", 20, 1000, 110)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    potasyum = st.number_input("Potasyum (mEq/L)", 1.0, 10.0, 4.2, 0.1)
    ta_sis = st.number_input("Sistolik TA", 40, 280, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.metric("eGFR", f"{egfr} ml/dk")
    
    # GERÇEK ZAMANLI KLİNİK FRENLER
    if egfr < 30: st.markdown("<div class='critical-alert'>🚨 RENAL FREN: Metformin/NSAİİ Kesilmeli!</div>", unsafe_allow_html=True)
    if seker > 350: st.markdown("<div class='critical-alert'>🚨 HİPERGLİSEMİ: DKA Protokolü!</div>", unsafe_allow_html=True)
    if potasyum > 5.5: st.markdown("<div class='critical-alert'>🚨 KRİTİK K+: Kayexalate/Diyaliz Planla!</div>", unsafe_allow_html=True)

# 4. GELİŞMİŞ KLİNİK SKORLAMA (WELLS & CHADS)
st.subheader("🧮 Akıllı Klinik Skorlama Modülleri")
sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown("**Wells (Pulmoner Emboli)**")
    w1 = st.toggle("DVT Bulgusu (+3)")
    w2 = st.toggle("Alternatif Tanı Az Olası (+3)")
    w3 = st.toggle("Taşikardi >100 (+1.5)")
    wells_score = (3 if w1 else 0) + (3 if w2 else 0) + (1.5 if w3 else 0)
    st.info(f"Wells Puanı: {wells_score}")
with sc2:
    st.markdown("**CHA2DS2-VASc (AF Risk)**")
    cv1 = st.toggle("KKY (+1)")
    cv2 = st.toggle("HT (+1)")
    cv3 = st.toggle("Yaş >= 75 (+2)")
    cv_score = (1 if cv1 else 0) + (1 if cv2 else 0) + (2 if cv3 else 0)
    st.info(f"İnme Riski: {cv_score}")
with sc3:
    gks = st.select_slider("Glasgow (GKS)", options=range(3, 16), value=15)
    if gks <= 8: st.error("⚠️ ENTÜBASYON!")

# 5. MAKSİMUM SİSTEMİK SORGULAMA (MULTİDİSİPLİNER)
st.subheader("🔍 Klinik Bulguları Eksiksiz İşleyiniz")
tabs = st.tabs(["Gastro-Hepato", "Kardiyo-Pulmoner", "Nöro-Toksiko", "Hemato-Romatoloji", "Endokrin-Renal"])

hepsi = []
with tabs[0]: hepsi.extend(st.multiselect("Bulgular (G)", ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Hematemez", "Caput Medusae", "Asteriksis"]))
with tabs[1]: hepsi.extend(st.multiselect("Bulgular (C)", ["Göğüs Ağrısı", "Ortopne", "Bilateral Ödem", "Unilateral Ödem", "Hemoptizi", "Boyun Ven Dolgunluğu"]))
with tabs[2]: hepsi.extend(st.multiselect("Bulgular (N)", ["Ense Sertliği", "Konfüzyon", "Miyozis", "Midriyazis", "Hipersalivasyon", "Nöbet", "Ataksi"]))
with tabs[3]: hepsi.extend(st.multiselect("Bulgular (H)", ["Peteşi/Purpura", "Lenfadenopati", "Kelebek Döküntü", "Sabah Sertliği", "Eklem Ağrısı", "Raynaud"]))
with tabs[4]: hepsi.extend(st.multiselect("Bulgular (E)", ["Aseton Kokusu", "Poliüri", "Polidipsi", "Oligüri", "Hiperpigmentasyon", "Mor Stria"]))

# 6. DEVASA VERİ KÜTÜPHANESİ (HİÇBİR ŞEY SİLİNMEDİ)
arsiv = {
    "Siroz / Portal Hipertansiyon": {
        "bulgular": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis"],
        "tetkik": "INR, Albümin, Amonyak, Batın USG (Sarı, Mor, Mavi Tüpler)",
        "doz": "Spironolakton 100mg, Furosemid 40mg.",
        "not": "GİS Kanama varsa Terlipressin + Seftriakson başla."
    },
    "Diyabetik Ketoasidoz": {
        "bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon"],
        "tetkik": "Kan Gazı, Ketonyüri, Elektrolit.",
        "doz": f"İnsülin: {round(kilo*0.1, 1)} Ünite/Saat. Hidrasyon: %0.9 SF 1L/saat.",
        "not": "K+ < 3.3 ise İnsülini stop!"
    },
    "Pulmoner Emboli": {
        "bulgular": ["Hemoptizi", "Unilateral Ödem", "Taşikardi"],
        "tetkik": "BT Anjiyo, D-Dimer (Mavi Tüp).",
        "doz": f"Enoksaparin {kilo}mg 2x1 (S.C).",
        "not": "eGFR <30 ise Heparin infüzyonuna geç."
    },
    "Sistemik Vaskülit (GPA/Wegener)": {
        "bulgular": ["Hemoptizi", "Purpura", "Eklem Ağrısı"],
        "tetkik": "c-ANCA, Renal Biyopsi, Akciğer BT.",
        "doz": "Pulse Steroid (1g/gün) + Siklofosfamid.",
        "not": "Renal ve Akciğer tutulumunu yakından izle."
    }
}

# 7. ANALİZ MOTORU VE EPİKRİZ
if st.button("🚀 OMNI-KOMUTU ÇALIŞTIR"):
    if not hepsi:
        st.error("Lütfen belirti giriniz.")
    else:
        st.divider()
        sonuclar = []
        for ad, d in arsiv.items():
            eslesme = set(hepsi).intersection(set(d["bulgular"]))
            if eslesme:
                puan = round((len(eslesme) / len(d["bulgular"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": d, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.markdown("### 📊 Klinik Analiz & Dozaj Rehberi")
            for s in sonuclar:
                st.markdown(f"""
                <div class='diag-card'>
                    <div style='font-size:1.6em; color:#58a6ff; font-weight:bold;'>{s['ad']} (%{s['puan']})</div>
                    <p>🧪 <b>Tetkik Planı:</b> {s['veri']['tetkik']}</p>
                    <p>💉 <b>Kişiselleştirilmiş Doz ({kilo}kg):</b> {s['veri']['doz']}</p>
                    <p style='color:#ff7b72;'>⚠️ <b>Kritik Klinik Not:</b> {s['veri']['not']}</p>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📝 RESMİ EPİKRİZ")
            radyo = "Kontrastlı uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK ŞART"
            epikriz = f"""TIBBİ KARAR ANALİZİ
--------------------------------------------------
HASTA: {yas}Y | {kilo}KG | eGFR: {egfr}
GLİKOZ: {seker} | POTASYUM: {potasyum} | TA: {ta_sis}
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}

[TESPİT EDİLEN BULGULAR]
{", ".join(hepsi)}

[OLASI TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[HEKİM YÖNETİM PLANI]
- eGFR {egfr} nedeniyle {radyo}.
- {"DİKKAT: Diyabetik acil riski!" if seker > 350 else "Glisemi stabil."}
- {"DİKKAT: Wells Skoru Emboli destekliyor!" if wells_score >= 4 else "Düşük olasılıklı klinik."}

--------------------------------------------------
SİSTEM GELŞTİRİCİSİ: İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("📤 Raporu Arşivle", epikriz, file_name=f"klinik_kayit_{h_ad}.txt")

st.markdown("---")
st.caption("İSMAİL ORHAN | The Ultimate Medical Infrastructure | 2026")
