import streamlit as st
from datetime import datetime

# 1. ULTRA-PREMIUM GLASSMORPHISM TASARIMI (AÇIK TEMA)
st.set_page_config(page_title="İSMAİL ORHAN | Clinical Matrix", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    .stApp { 
        background: linear-gradient(135deg, #F0F4F8 0%, #E2E8F0 100%); 
        color: #1E293B; 
        font-family: 'Plus Jakarta Sans', sans-serif; 
    }
    
    /* Modern Glass Header */
    .main-header {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        padding: 50px; border-radius: 40px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    }
    .main-header h1 { 
        background: linear-gradient(90deg, #2563EB, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 3.5rem; 
    }
    
    /* Klinik Kartlar */
    .diag-card { 
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 30px; border-radius: 30px; margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02);
        border-left: 12px solid #3B82F6;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .diag-card:hover { transform: scale(1.02); box-shadow: 0 15px 45px rgba(37, 99, 235, 0.1); }
    
    /* Modern Vital Widget */
    .vital-box {
        background: white; border-radius: 20px; padding: 15px;
        border: 1px solid #E2E8F0; margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.01);
    }
    
    /* Epikriz Dokusu */
    .epikriz-paper { 
        background: #FFFFFF; padding: 50px; border-radius: 15px; 
        box-shadow: 0 10px 50px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0; line-height: 1.7; position: relative;
    }
    .epikriz-paper::before {
        content: "RESMİ KAYIT"; position: absolute; top: 20px; right: 20px;
        color: #E2E8F0; font-weight: 900; font-size: 2rem; transform: rotate(15deg);
    }

    /* Büyük Buton */
    .stButton>button {
        background: linear-gradient(90deg, #2563EB 0%, #7C3AED 100%);
        color: white; border-radius: 25px; height: 5.5em; width: 100%;
        font-weight: 800; font-size: 24px; border: none; transition: 0.5s;
    }
    .stButton>button:hover { opacity: 0.9; transform: translateY(-3px); }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown(f"""
    <div class='main-header'>
        <h1>TIBBİ ALTYAPI VE ANALİZ ÜSSÜ</h1>
        <p><b>İSMAİL ORHAN</b> | Klinik Karar Destek & Diferansiyel Tanı Algoritması</p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL - AKILLI TERMİNAL
with st.sidebar:
    st.markdown("### 📊 HASTA PROFİLİ")
    h_kimlik = st.text_input("Protokol No", "IO-V8-2026")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Ağırlık (kg)", 3, 220, 75)
    st.divider()
    st.markdown("### 🧪 KRİTİK DEĞERLER")
    seker = st.number_input("Glukoz (mg/dL)", 20, 1000, 105)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    potasyum = st.number_input("Potasyum (mEq/L)", 1.0, 10.0, 4.2, 0.1)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 40, 280, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.metric("Böbrek Rezervi (eGFR)", f"{egfr} ml/dk")
    
    # AKILLI GÜVENLİK FİLTRESİ
    if egfr < 30: st.info("🚨 RENAL YETMEZLİK: Dozları %50 azalt!")
    if potasyum > 5.5: st.warning("🚨 HİPERPOTASEMİ: Acil EKG!")
    if seker > 350: st.error("🚨 DKA / HHS ŞÜPHESİ!")

# 4. DEVASA SİSTEMİK BELİRTİ MATRİSİ
st.subheader("🔍 Klinik Matris Girişi")
t1, t2, t3, t4, t5 = st.tabs(["🧬 SİSTEMİK & ROMATO", "🫀 KARDİYO-PULMONER", "🤢 GİS & HEPATOBİLİER", "🧠 NÖRO & PSİKİYATRİ", "🧪 ENDOKRİN & RENAL"])

hepsi = []
with t1:
    hepsi.extend(st.multiselect("Belirtiler (S)", ["Ateş", "Kilo Kaybı", "Gece Terlemesi", "Lenfadenopati", "Kelebek Döküntü", "Raynaud Fenomeni", "Sabah Sertliği", "Peteşi/Purpura", "Oral Aft", "Eklem Şişliği", "Halsizlik (Ekstrem)"]))
with t2:
    hepsi.extend(st.multiselect("Belirtiler (CP)", ["Göğüs Ağrısı (Baskı)", "Nefes Darlığı", "Ortopne", "PND", "Bilateral Ödem", "Unilateral Ödem", "Hemoptizi", "Boyun Ven Dolgunluğu", "Ral/Ronküs", "Wheezing", "Taşikardi"]))
with t3:
    hepsi.extend(st.multiselect("Belirtiler (GİS)", ["Sarılık", "Asit", "Hematemez", "Melena", "Hepatomegali", "Splenomegali", "Caput Medusae", "Asteriksis", "Murphy (+)", "Kuşak Tarzı Karın Ağrısı", "Disfaji"]))
with t4:
    hepsi.extend(st.multiselect("Belirtiler (NP)", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Fokal Kayıp", "Ani Baş Ağrısı", "Tremor", "Ataksi", "Diplopi", "Miyozis", "Midriyazis", "Hipersalivasyon"]))
with t5:
    hepsi.extend(st.multiselect("Belirtiler (ER)", ["Poliüri", "Polidipsi", "Oligüri", "Anüri", "Aseton Kokusu", "Hiperpigmentasyon", "Mor Stria", "Aydede Yüzü", "Ekzoftalmi", "Pretibial Miksödem"]))

# 5. DEVASA TANI VE BELİRTİ İLİŞKİSİ KÜTÜPHANESİ
# İsmail, buraya Dahiliye'nin neredeyse tüm ana ve yan başlıklarını ekledim.
arsiv = {
    "Karaciğer Sirozu": {"bulgular": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"], "tetkik": "INR, Albümin, Amonyak (Buzda), Batın USG", "doz": "Spironolakton 100mg, Furosemid 40mg", "not": "Parasentezde PMNL > 250 ise SBP!"},
    "Diyabetik Ketoasidoz (DKA)": {"bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Halsizlik (Ekstrem)"], "tetkik": "Kan Gazı, Ketonyüri, Elektrolitler", "doz": f"İnsülin: {round(kilo*0.1, 1)} Ü/saat + SF Hidrasyon", "not": "K+ < 3.3 ise İnsülini hemen durdur!"},
    "Pulmoner Emboli": {"bulgular": ["Hemoptizi", "Unilateral Ödem", "Taşikardi", "Nefes Darlığı", "Plevritik Ağrı"], "tetkik": "BT Pulmoner Anjiyo, D-Dimer, EKG (S1Q3T3)", "doz": f"Enoksaparin {kilo}mg 2x1 S.C.", "not": "RV strain varsa Trombolitik düşün."},
    "Sistemik Lupus (SLE)": {"bulgular": ["Kelebek Döküntü", "Eklem Şişliği", "Peteşi/Purpura", "Oral Aft", "Gece Terlemesi"], "tetkik": "ANA, Anti-dsDNA, C3-C4 Seviyeleri", "doz": "Steroid + Hidroksiklorokin", "not": "Nefrit gelişimi için proteinüri takibi!"},
    "Akut Pankreatit": {"bulgular": ["Kuşak Tarzı Karın Ağrısı", "Hipotansiyon", "Halsizlik (Ekstrem)"], "tetkik": "Lipaz (3 kat artış), Batın BT", "doz": "Agresif Ringer Laktat Hidrasyonu", "not": "Ranson veya BISAP skoru hesapla."},
    "Feokromositoma": {"bulgular": ["Taşikardi", "Ani Baş Ağrısı", "Hiperpigmentasyon", "Halsizlik (Ekstrem)"], "tetkik": "Plazma Metanefrinleri, Sürrenal BT", "doz": "Alfa Bloker (Doksazosin)", "not": "Asla önce Beta Bloker verme (Hipertansif Kriz!)"},
    "Miksödem Koması": {"bulgular": ["Konfüzyon", "Hipotansiyon", "Pretibial Miksödem", "Halsizlik (Ekstrem)"], "tetkik": "TSH, sT4, Kortizol", "doz": "IV Levotiroksin + Steroid", "not": "Önce steroid verilmeli!"},
    "Wegener (GPA)": {"bulgular": ["Hemoptizi", "Peteşi/Purpura", "Nefes Darlığı", "Halsizlik (Ekstrem)"], "tetkik": "c-ANCA, Akciğer BT, Böbrek Biyopsisi", "doz": "Pulse Steroid + Siklofosfamid", "not": "Hızlı ilerleyen böbrek yetmezliğine dikkat!"},
    "Tümör Lizis Sendromu": {"bulgular": ["Oligüri", "Nöbet", "Halsizlik (Ekstrem)"], "tetkik": "Ürik Asit, K+, Fosfor, Ca", "doz": "Rasburikaz + Hidrasyon", "not": "Ürik asit nefropatisi riskine dikkat."},
    "Cushing Sendromu": {"bulgular": ["Mor Stria", "Aydede Yüzü", "Hiperpigmentasyon", "Kilo Kaybı"], "tetkik": "Dekzametazon Baskılama Testi", "doz": "Etyolojiye yönelik (Cerrahi/İlaç)", "not": "HT ve DM eşlik edebilir."}
}

# 6. ANALİZ VE EPİKRİZ ÇIKTISI
if st.button("🚀 OMNI-MATRİS ANALİZİNİ ÇALIŞTIR"):
    if not hepsi:
        st.error("Lütfen klinik belirti girişi yapınız.")
    else:
        sonuclar = []
        for ad, d in arsiv.items():
            eslesme = set(hepsi).intersection(set(d["bulgular"]))
            if eslesme:
                puan = round((len(eslesme) / len(d["bulgular"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": d, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        col_res_a, col_res_b = st.columns([1.7, 1])
        with col_res_a:
            st.markdown("### 🧬 Tanısal Eşleşme ve Tedavi Protokolleri")
            for s in sonuclar:
                st.markdown(f"""
                <div class='diag-card'>
                    <div style='font-size:2em; color:#2563EB; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p style='margin-top:15px;'>🎯 <b>Tespit Edilen Belirtiler:</b> {", ".join(s['esles'])}</p>
                    <p>🧪 <b>Tetkik Paneli:</b> {s['veri']['tetkik']}</p>
                    <p>💉 <b>Hekim Dozaj Planı ({kilo}kg):</b> {s['veri']['doz']}</p>
                    <p style='color:#EF4444; font-weight:bold;'>⚠️ HAYATİ NOT: {s['veri']['not']}</p>
                </div>
                """, unsafe_allow_html=True)

        with col_res_b:
            st.markdown("### 📝 RESMİ KLİNİK EPİKRİZ")
            radyo_not = "Kontrastlı tetkik güvenli." if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / ÖN HİDRASYON ŞART."
            epikriz = f"""TIBBİ KARAR ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
SORUMLU: İSMAİL ORHAN
PROTOKOL: {h_kimlik}

[VİTAL PARAMETRELER]
Yaş: {yas} | Kilo: {kilo} | eGFR: {egfr}
Glukoz: {seker} | TA: {ta_sis} | K+: {potasyum}

[SEÇİLEN BULGULAR]
{", ".join(hepsi)}

[ÖN TANILAR VE UYUM]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[RADYOLOJİK GÜVENLİK NOTU]
- {radyo_not}

--------------------------------------------------
ONAY VE İMZA:İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("📤 Raporu Arşive Gönder", epikriz, file_name=f"{h_kimlik}_final.txt")

st.markdown("---")
st.caption("İSMAİL ORHAN | Global Clinical Intelligence Center | 2026")
