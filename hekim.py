import streamlit as st
from datetime import datetime

# 1. TASARIM: PREMİUM KLİNİK TERMİNAL (TÜRKÇE ARAYÜZ)
st.set_page_config(page_title="İSMAİL ORHAN | Tıbbi Komuta Merkezi", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010409; color: #e2e8f0; }
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 50px;
        border-radius: 20px; text-align: center; border: 2px solid #334155; margin-bottom: 30px;
    }
    .diag-card { 
        background: #0d1117; border: 1px solid #30363d; padding: 25px; border-radius: 15px; 
        margin-bottom: 20px; border-left: 12px solid #238636;
    }
    .critical-alert { 
        background: rgba(220, 38, 38, 0.2); border: 2px solid #dc2626; 
        color: #ef4444; padding: 20px; border-radius: 12px; font-weight: bold; margin-bottom: 15px;
    }
    .epikriz-paper { 
        background: #ffffff; color: #000; padding: 45px; border-radius: 5px; 
        font-family: 'Courier New', monospace; border: 4px solid #000; line-height: 1.4;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e40af, #3b82f6); color: white; border-radius: 15px; 
        height: 5.5em; width: 100%; font-weight: 900; font-size: 26px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>⚖️ TIBBİ ALTYAPI VE KLİNİK ANALİZ SİSTEMİ</h1><p>Dahiliye Karar Destek Üssü | Dozaj ve Skorlama | İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 3. AKILLI VİTAL VE LABORATUVAR PANELİ (YAN PANEL)
with st.sidebar:
    st.header("📋 HASTA PARAMETRELERİ")
    h_ad = st.text_input("Protokol / Arşiv No", "ARCH-2026-V5")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 220, 75)
    st.divider()
    seker = st.number_input("Kan Şekeri (mg/dL)", 20, 1000, 105)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    potasyum = st.number_input("Potasyum (mEq/L)", 1.0, 10.0, 4.0, 0.1)
    ta_sis = st.number_input("Sistolik Tansiyon", 40, 280, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.metric("eGFR (Böbrek Fonksiyonu)", f"{egfr} ml/dk")
    
    # GERÇEK ZAMANLI KLİNİK FRENLER VE UYARILAR
    if egfr < 30: st.markdown("<div class='critical-alert'>🚨 RENAL YETMEZLİK: İlaç dozlarını revize et!</div>", unsafe_allow_html=True)
    if seker > 300: st.markdown("<div class='critical-alert'>🚨 HİPERGLİSEMİ: Ketonyüri kontrolü!</div>", unsafe_allow_html=True)
    if potasyum > 5.5: st.markdown("<div class='critical-alert'>🚨 HİPERPOTASEMİ: EKG ve K-Bağlayıcı!</div>", unsafe_allow_html=True)
    if ta_sis > 180: st.markdown("<div class='critical-alert'>🚨 HİPERTANSİF KRİZ: Hedef organ hasarı?</div>", unsafe_allow_html=True)

# 4. KLİNİK SKORLAMA MODÜLLERİ (GELİŞTİRİLMİŞ)
st.subheader("🧮 Otomatik Klinik Skorlama Sistemi")
s_col1, s_col2, s_col3 = st.columns(3)
with s_col1:
    st.markdown("**Wells (Pulmoner Emboli Skoru)**")
    wells = sum([st.toggle("DVT Bulgusu (+3)"), st.toggle("Alternatif Tanı Az Olası (+3)"), st.toggle("Taşikardi >100 (+1.5)"), st.toggle("3 Günden Fazla İmmobilite (+1.5)")])
    st.info(f"Wells Puanı: {wells}")
with s_col2:
    st.markdown("**Gastrointestinal Risk (Blatchford)**")
    blatch = st.slider("Blatchford Skoru (Kanama Riski)", 0, 20, 0)
    if blatch > 0: st.warning("Acil Endoskopi İhtiyacı?")
with s_col3:
    gks = st.select_slider("Glasgow Koma Skalası (GKS)", options=range(3, 16), value=15)
    if gks <= 8: st.error("⚠️ HASTAYI ENTÜBE ET!")

# 5. MAKSİMUM SİSTEMİK SORGULAMA (KATEGORİZE EDİLMİŞ)
st.subheader("🔍 Klinik Bulguları ve Semptomları Tanımlayın")
t1, t2, t3, t4, t5 = st.tabs(["MİDE-BARSAK-KC", "KALP-SOLUNUM", "NÖRO-TOKSİKO", "HEMATO-ROMATO", "ENDOKRİN-RENAL"])

hepsi = []
with t1: hepsi.extend(st.multiselect("Bulgular (GİS)", ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Hematemez", "Melena", "Caput Medusae", "Asteriksis", "Murphy (+)", "Karın Ağrısı (Kuşak Şeklinde)"]))
with t2: hepsi.extend(st.multiselect("Bulgular (CVP)", ["Göğüs Ağrısı (Baskı)", "Nefes Darlığı", "Ortopne", "PND", "Bilateral Ödem", "Unilateral Ödem", "Hemoptizi", "Boyun Ven Dolgunluğu", "Ral/Ronküs"]))
with t3: hepsi.extend(st.multiselect("Bulgular (Nöro)", ["Ense Sertliği", "Konfüzyon", "Miyozis", "Midriyazis", "Hipersalivasyon", "Nöbet", "Fokal Nörolojik Kayıp", "Tremor", "Ataksi"]))
with t4: hepsi.extend(st.multiselect("Bulgular (R/H)", ["Peteşi/Purpura", "Lenfadenopati", "Kelebek Döküntü", "Sabah Sertliği", "Oral Aft", "Eklem Ağrısı", "Raynaud Fenomeni", "B Semptomları (Ateş/Terleme)"]))
with t5: hepsi.extend(st.multiselect("Bulgular (E/R)", ["Aseton Kokusu", "Poliüri", "Polidipsi", "Oligüri", "Anüri", "Hiperpigmentasyon", "Ekzoftalmi", "Mor Stria", "Aydede Yüzü"]))

# 6. DEVASA VERİ KÜTÜPHANESİ (YENİ HASTALIKLAR VE BULGULAR EKLENDİ)
arsiv = {
    "Siroz ve Portal Hipertansiyon": {
        "bulgular": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"],
        "tetkik": "AST/ALT, INR (Mavi), Albümin (Sarı), Amonyak (Buzda), Batın USG.",
        "doz": "Spironolakton 100mg, Furosemid 40mg.",
        "not": "SBP şüphesinde parasentez yap! eGFR düşükse diüretik dozuna dikkat."
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon"],
        "tetkik": "Kan Gazı, Kan Şekeri, Ketonyüri (Mor tüp/enjektör).",
        "doz": f"İnsülin İnfüzyon: {round(kilo*0.1, 1)} Ü/saat. Hidrasyon: %0.9 SF 1000cc/saat.",
        "not": "Potasyum < 3.3 ise insülini kes, önce K+ replasmanı yap!"
    },
    "Pulmoner Emboli (Masif/Submasif)": {
        "bulgular": ["Hemoptizi", "Unilateral Ödem", "Taşikardi", "Nefes Darlığı"],
        "tetkik": "BT Pulmoner Anjiyo, D-Dimer (Mavi), Troponin (Sarı).",
        "doz": f"Enoksaparin {kilo}mg 2x1 S.C. (eGFR <30 ise Heparin infüzyonu).",
        "not": "Wells skoru yüksekse direkt BT Anjiyo planla."
    },
    "Miksödem Koması (Hipotiroidi Krizi)": {
        "bulgular": ["Konfüzyon", "Bradikardi", "Hipotansiyon", "Hipotermi"],
        "tetkik": "TSH, sT4, Kortizol düzeyi.",
        "doz": "IV Levotiroksin + IV Hidrokortizon (Adrenal yetmezliği ekarte edene kadar).",
        "not": "Önce steroid verilmeli, sonra tiroid hormonu (Kriz tetiklememek için)."
    },
    "Wegener Granülomatozu (GPA)": {
        "bulgular": ["Hemoptizi", "Peteşi/Purpura", "Eklem Ağrısı", "Nefes Darlığı"],
        "tetkik": "c-ANCA, Akciğer BT, Böbrek Biyopsisi.",
        "doz": "Pulse Steroid (1g/gün) + Siklofosfamid/Rituksimab.",
        "not": "Renal yetmezlik hızlı gelişebilir, kreatinin takibi kritik."
    },
    "Tümör Lizis Sendromu (Onkolojik Acil)": {
        "bulgular": ["Oligüri", "Nöbet", "Bulantı", "Kramplar"],
        "tetkik": "Ürik Asit, Potasyum, Fosfor, Kalsiyum (Sarı).",
        "doz": "Agresif Hidrasyon + Rasburikaz / Allopurinol.",
        "not": "Hiperpotasemi ve Akut Böbrek Hasarı açısından izle."
    }
}

# 7. ANALİZ VE EPİKRİZ MOTORU
if st.button("🚀 OMNI-ARŞİV ANALİZİNİ BAŞLAT"):
    if not hepsi:
        st.error("Lütfen klinik bulguları seçiniz.")
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
            st.markdown("### 📊 Klinik Analiz & Tedavi Planı")
            for s in sonuclar:
                st.markdown(f"""
                <div class='diag-card'>
                    <div style='font-size:1.6em; color:#58a6ff; font-weight:bold;'>{s['ad']} (Eşleşme: %{s['puan']})</div>
                    <p>🧪 <b>Tetkik Rehberi:</b> {s['veri']['tetkik']}</p>
                    <p>💉 <b>Hastaya Özel Doz ({kilo}kg):</b> {s['veri']['doz']}</p>
                    <p style='color:#ff7b72;'>⚠️ <b>Hayati Not:</b> {s['veri']['not']}</p>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📝 RESMİ KLİNİK EPİKRİZ")
            radyo = "Kontrastlı uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / ÖN HİDRASYON"
            epikriz = f"""TIBBİ KARAR VE ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
HASTA ID: {h_ad} | YAŞ: {yas} | KİLO: {kilo}kg
eGFR: {egfr} | ŞEKER: {seker} | K+: {potasyum}

[KLİNİK BULGULAR]
{", ".join(hepsi)}

[AYIRICI TANI ANALİZİ]
{chr(10).join([f"- {x['ad']} (%{x['puan']} uyum)" for x in sonuclar[:5]])}

[YÖNETİM VE GÜVENLİK NOTU]
- eGFR {egfr} nedeniyle {radyo}.
- Wells Skoru: {wells} {"(Emboli Olası)" if wells >= 4 else "(Emboli Düşük Olasılık)"}.
- {"DİKKAT: Kritik Potasyum düzeyi!" if potasyum > 5.5 else "Elektrolitler stabil."}

--------------------------------------------------
ONAY: SİSTEM GELİŞTİRİCİSİ : İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("📥 Raporu Arşivle (TXT)", epikriz, file_name=f"{h_ad}_rapor.txt")

st.markdown("---")
st.caption("İSMAİL ORHAN | The Ultimate Medical Infrastructure | Version: 2026.04")
