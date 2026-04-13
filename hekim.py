import streamlit as st
from datetime import datetime

# 1. ULTRA MODERN & ELİT KLİNİK TASARIM (APPLE PRO STYLE)
st.set_page_config(page_title="İSMAİL ORHAN | Klinik Komuta Merkezi", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;600;800&display=swap');
    
    .stApp { background-color: #FBFBFD; color: #1D1D1F; font-family: 'SF Pro Display', sans-serif; }
    
    /* Ana Panel */
    .main-header {
        background: white; padding: 50px; border-radius: 35px; text-align: center; margin-bottom: 40px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04); border: 1px solid #D2D2D7;
    }
    .main-header h1 { color: #0071E3; font-weight: 800; font-size: 3.5rem; letter-spacing: -1px; }
    .main-header p { color: #86868B; font-size: 1.3rem; margin-top: 10px; }
    
    /* Glassmorphism Kartlar */
    .diag-card { 
        background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);
        border: 1px solid #D2D2D7; padding: 35px; border-radius: 28px; 
        margin-bottom: 30px; border-left: 12px solid #0071E3;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03);
    }
    
    /* Kritik Durum Uyarıları */
    .critical-alert { 
        background: #FFF2F2; border: 1px solid #FFD2D2; 
        color: #D70015; padding: 20px; border-radius: 18px; font-weight: 700;
        margin-bottom: 20px; text-align: center;
    }
    
    /* Profesyonel Epikriz Dokusu */
    .epikriz-paper { 
        background: white; color: #1D1D1F; padding: 60px; border-radius: 5px; 
        font-family: 'Courier New', monospace; border: 1px solid #D2D2D7; line-height: 1.6;
        box-shadow: 0 20px 60px rgba(0,0,0,0.05);
    }
    
    /* Modern Butonlar */
    .stButton>button {
        background: linear-gradient(180deg, #0077ED 0%, #006EDF 100%);
        color: white; border-radius: 16px; height: 5em; width: 100%;
        font-weight: 700; font-size: 24px; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0 10px 30px rgba(0,113,227,0.3); }
    
    /* Tab ve Sidebar */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #F5F5F7; border-radius: 12px; padding: 10px 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown(f"""
    <div class='main-header'>
        <h1>TIBBİ ALTYAPI VE ANALİZ SİSTEMİ</h1>
        <p>Geliştirici: <b>İSMAİL ORHAN</b> | Dahiliye Karar Destek Matrisi V10</p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL - TAM KONTROL TERMİNALİ
with st.sidebar:
    st.markdown("### 🖥️ HASTA PARAMETRELERİ")
    h_protokol = st.text_input("Protokol No", "FINAL-UNIT-2026")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Vücut Ağırlığı (kg)", 3, 220, 75)
    
    st.divider()
    st.markdown("### 🧬 LABORATUVAR & VİTAL")
    seker = st.number_input("Glukoz (mg/dL)", 20, 1000, 105)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    potasyum = st.number_input("Potasyum (mEq/L)", 1.0, 10.0, 4.2, 0.1)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 40, 280, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.metric("Böbrek Rezervi (eGFR)", f"{egfr} ml/dk")
    
    # GERÇEK ZAMANLI GÜVENLİK FİLTRELERİ (SİLİNMEDİ!)
    if egfr < 30: st.markdown("<div class='critical-alert'>🚨 RENAL FREN: Metformin/NSAİİ Kesilmeli!</div>", unsafe_allow_html=True)
    if seker > 350: st.markdown("<div class='critical-alert'>🚨 KRİTİK ŞEKER: DKA/HHS Protokolü!</div>", unsafe_allow_html=True)
    if potasyum > 5.5: st.markdown("<div class='critical-alert'>🚨 HİPERPOTASEMİ: EKG & K-Bağlayıcı!</div>", unsafe_allow_html=True)

# 4. GELİŞTİRİLMİŞ KLİNİK SKORLAMA MODÜLLERİ
st.subheader("🧮 Klinik Risk Analiz Modülleri")
sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown("**Wells (Pulmoner Emboli)**")
    w1 = st.toggle("DVT Bulgusu (+3)")
    w2 = st.toggle("Alternatif Tanı Az Olası (+3)")
    w3 = st.toggle("Taşikardi >100 (+1.5)")
    w4 = st.toggle("3 Günden Fazla İmmobilite (+1.5)")
    wells_score = sum([3 if w1 else 0, 3 if w2 else 0, 1.5 if w3 else 0, 1.5 if w4 else 0])
    st.info(f"Wells Puanı: {wells_score}")
with sc2:
    st.markdown("**CHA2DS2-VASc (AF Risk)**")
    cv1 = st.toggle("KKY (+1)")
    cv2 = st.toggle("HT (+1)")
    cv3 = st.toggle("Yaş >= 75 (+2)")
    cv_score = sum([1 if cv1 else 0, 1 if cv2 else 0, 2 if cv3 else 0])
    st.info(f"İnme Riski Skoru: {cv_score}")
with sc3:
    gks = st.select_slider("Glasgow Koma Skalası (GKS)", options=range(3, 16), value=15)
    if gks <= 8: st.error("⚠️ ACİL ENTÜBASYON ENDİKASYONU!")

# 5. DEVASA SİSTEMİK SORGULAMA (EKSİKSİZ KATMANLAR)
st.subheader("🔍 Klinik Bulguları ve Semptomları Giriniz")
tabs = st.tabs(["🧬 SİSTEMİK", "🫀 KARDİYO-PULMONER", "🤢 GASTRO-HEPATOBİLİER", "🧠 NÖRO-TOKSİKO", "🧪 ENDOKRİN-RENAL", "🩸 HEMATO-ROMATOLOJİ"])

hepsi = []
with tabs[0]: hepsi.extend(st.multiselect("Bulgular (S)", ["Ateş", "Gece Terlemesi", "Kilo Kaybı (>%10)", "Halsizlik (Ekstrem)", "Lenfadenopati", "Kaşıntı", "Ağızda Aft"]))
with tabs[1]: hepsi.extend(st.multiselect("Bulgular (CP)", ["Göğüs Ağrısı", "Nefes Darlığı", "Ortopne", "PND", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Boyun Ven Dolgunluğu", "Ral/Ronküs", "Wheezing"]))
with tabs[2]: hepsi.extend(st.multiselect("Bulgular (GİS)", ["Sarılık", "Asit", "Hematemez", "Melena", "Hepatomegali", "Splenomegali", "Caput Medusae", "Asteriksis", "Murphy (+)", "Kuşak Tarzı Ağrı"]))
with tabs[3]: hepsi.extend(st.multiselect("Bulgular (N)", ["Ense Sertliği", "Konfüzyon", "Nöbet", "Fokal Güç Kaybı", "Ani Baş Ağrısı", "Miyozis", "Midriyazis", "Ataksi", "Tremor"]))
with tabs[4]: hepsi.extend(st.multiselect("Bulgular (ER)", ["Poliüri", "Polidipsi", "Oligüri", "Anüri", "Aseton Kokusu", "Hiperpigmentasyon", "Mor Stria", "Aydede Yüzü", "Ekzoftalmi"]))
with tabs[5]: hepsi.extend(st.multiselect("Bulgular (HR)", ["Peteşi/Purpura", "Kelebek Döküntü", "Raynaud", "Sabah Sertliği", "Eklem Ağrısı", "B Semptomları"]))

# 6. EN GENİŞ TIBBİ VERİ SÖZLÜĞÜ (HİÇBİR ŞEY SİLİNMEDİ + YENİLER EKLENDİ)
arsiv = {
    "Karaciğer Sirozu": {"bulgular": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"], "tetkik": "INR, Albümin, Amonyak, Batın USG", "doz": "Spironolakton 100mg, Furosemid 40mg", "not": "SBP şüphesinde parasentez!"},
    "Diyabetik Ketoasidoz (DKA)": {"bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon"], "tetkik": "Kan Gazı, Ketonyüri, Elektrolitler", "doz": f"İnsülin: {round(kilo*0.1, 1)} Ü/saat", "not": "K+ < 3.3 ise İnsülini KES!"},
    "Pulmoner Emboli": {"bulgular": ["Hemoptizi", "Unilateral Ödem", "Taşikardi", "Nefes Darlığı"], "tetkik": "BT Anjiyo, D-Dimer, Troponin", "doz": f"Enoksaparin {kilo}mg 2x1 S.C.", "not": "Wells skoru yüksekse direkt BT!"},
    "Sistemik Lupus (SLE)": {"bulgular": ["Kelebek Döküntü", "Eklem Ağrısı", "Peteşi/Purpura", "Ağızda Aft"], "tetkik": "ANA, Anti-dsDNA, C3-C4", "doz": "Hidroksiklorokin + Steroid", "not": "Proteinüri takibi yap!"},
    "Wegener (GPA)": {"bulgular": ["Hemoptizi", "Peteşi/Purpura", "Nefes Darlığı", "Halsizlik (Ekstrem)"], "tetkik": "c-ANCA, Akciğer BT, Renal Biyopsi", "doz": "Pulse Steroid + Siklofosfamid", "not": "Hızlı ilerleyen böbrek yetmezliği!"},
    "Tümör Lizis Sendromu": {"bulgular": ["Oligüri", "Nöbet", "Halsizlik (Ekstrem)"], "tetkik": "Ürik Asit, K+, Fosfor, Ca", "doz": "Rasburikaz + Hidrasyon", "not": "Hiperpotasemi riskine dikkat!"},
    "Menedjit (Bakteriyel)": {"bulgular": ["Ateş", "Ense Sertliği", "Konfüzyon", "Ani Baş Ağrısı"], "tetkik": "LP, BOS Kültürü, Kan Kültürü", "doz": "Seftriakson 2x2g + Vankomisin", "not": "LP öncesi BT ile KİBAS ekarte et!"},
    "Akut Pankreatit": {"bulgular": ["Kuşak Tarzı Ağrı", "Hipotansiyon", "Halsizlik (Ekstrem)"], "tetkik": "Lipaz, Amilaz, Batın BT", "doz": "Agresif SF Hidrasyonu", "not": "Oral alımı durdur!"},
    "Feokromositoma": {"bulgular": ["Taşikardi", "Ani Baş Ağrısı", "Terleme"], "tetkik": "Plazma Metanefrinleri", "doz": "Alfa Bloker (Doksazosin)", "not": "Asla önce Beta Bloker verme!"}
}

# 7. ANALİZ VE AKILLI RAPORLAMA
if st.button("🚀 OMNI-HEAL ANALİZİNİ ÇALIŞTIR"):
    if not hepsi:
        st.error("Lütfen belirti girişi yapınız.")
    else:
        sonuclar = []
        for ad, d in arsiv.items():
            eslesme = set(hepsi).intersection(set(d["bulgular"]))
            if eslesme:
                puan = round((len(eslesme) / len(d["bulgular"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": d, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        c1, c2 = st.columns([1.6, 1])
        with c1:
            st.markdown("### 🔬 Tanısal Matris & Tedavi Planı")
            for s in sonuclar:
                st.markdown(f"""
                <div class='diag-card'>
                    <div style='font-size:1.8em; color:#0071E3; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p>🎯 <b>Eşleşenler:</b> {", ".join(s['esles'])}</p>
                    <p>🧪 <b>Planlanan Tetkikler:</b> {s['veri']['tetkik']}</p>
                    <p>💉 <b>Hekim Dozu ({kilo}kg):</b> {s['veri']['doz']}</p>
                    <p style='color:#D70015; font-weight:bold;'>⚠️ KRİTİK NOT: {s['veri']['not']}</p>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📝 RESMİ EPİKRİZ RAPORU")
            radyo = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK ŞART"
            epikriz = f"""TIBBİ KARAR ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
PROTOKOL: {h_protokol} | GELİŞTİRİCİ: İSMAİL ORHAN

[VİTALLER]
Yaş: {yas} | Kilo: {kilo} | eGFR: {egfr}
Glukoz: {seker} | Potasyum: {potasyum} | TA: {ta_sis}

[KLİNİK BULGULAR]
{", ".join(hepsi)}

[AYIRICI TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[RADYOLOJİ VE GÜVENLİK]
- {radyo}
- Wells Skoru: {wells_score}
- GKS: {gks}

--------------------------------------------------
ONAY VE İMZA: İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("📥 Raporu PDF Arşivine Kaydet", epikriz, file_name=f"{h_protokol}_io.txt")

st.markdown("---")
st.caption("Geliştirici: İSMAİL ORHAN | Clinical Matrix Final Engine | 2026")
