import streamlit as st
from datetime import datetime

# 1. ELİT & HAVALI KLİNİK ARAYÜZ (ULTRA-MODERN CRYSTAL WHITE)
st.set_page_config(page_title="İSMAİL ORHAN | Global Clinical Matrix", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    .stApp { background: linear-gradient(135deg, #FDFDFD 0%, #F0F4F8 100%); color: #1E293B; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Holografik Başlık */
    .main-header {
        background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(20px);
        padding: 50px; border-radius: 50px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 20px 50px rgba(37, 99, 235, 0.1);
    }
    .main-header h1 { 
        background: linear-gradient(90deg, #1E40AF, #7C3AED, #2563EB);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 4rem; letter-spacing: -2px;
    }
    
    /* Neumorphic Kartlar */
    .clinical-card { 
        background: #FFFFFF; padding: 35px; border-radius: 35px; margin-bottom: 30px;
        border: 1px solid #E2E8F0; box-shadow: 15px 15px 30px #E2E8F0, -15px -15px 30px #FFFFFF;
        border-left: 15px solid #2563EB; transition: all 0.4s ease;
    }
    .clinical-card:hover { transform: scale(1.01); border-left: 15px solid #7C3AED; }
    
    /* Mega Buton */
    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%); color: white; border-radius: 25px;
        height: 6em; width: 100%; font-weight: 800; font-size: 26px; border: none;
        box-shadow: 0 10px 40px rgba(37, 99, 235, 0.3); transition: 0.5s;
    }
    .stButton>button:hover { letter-spacing: 2px; box-shadow: 0 15px 50px rgba(124, 58, 237, 0.4); }
    
    /* Kritik Uyarı Modülü */
    .alert-banner { 
        background: #FFF1F2; border-radius: 20px; padding: 15px; border: 1px solid #FDA4AF;
        color: #E11D48; font-weight: 700; text-align: center; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown(f"""
    <div class='main-header'>
        <h1>KLİNİK OPERASYON VE ANALİZ SİSTEMİ</h1>
        <p>Geliştirici: <b>İSMAİL ORHAN</b> | Dahiliye Ansiklopedisi & Karar Destek Matrisi</p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL - HASTA TERMİNALİ
with st.sidebar:
    st.header("💎 HASTA PROFİLİ")
    p_no = st.text_input("Protokol", "IO-MASTER-V14")
    yas = st.number_input("Yaş", 0, 115, 45)
    kilo = st.number_input("Kilo (kg)", 3, 250, 75)
    st.divider()
    st.markdown("### 🧬 LABORATUVAR")
    glu = st.number_input("Glukoz (mg/dL)", 0, 1500, 105)
    kre = st.number_input("Kreatinin (mg/dL)", 0.1, 20.0, 1.0)
    k_plus = st.number_input("Potasyum (mEq/L)", 1.0, 12.0, 4.2)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 30, 300, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kre), 1) if kre > 0 else 0
    st.metric("Hastalık Evresi (eGFR)", f"{egfr} ml/dk")
    
    if egfr < 30: st.markdown("<div class='alert-banner'>🚨 RENAL KRİZ: DOZ REVİZYONU!</div>", unsafe_allow_html=True)
    if glu > 400: st.markdown("<div class='alert-banner'>🚨 HİPERGLİSEMİK ACİL!</div>", unsafe_allow_html=True)

# 4. SKORLAMA MERKEZİ (WELLS, GKS, CHA2DS2)
st.subheader("📊 Klinik Hesaplayıcılar & Skorlar")
s1, s2, s3 = st.columns(3)
with s1:
    w_puan = st.multiselect("Wells (PE) Kriterleri", ["DVT Bulgusu (+3)", "Alt. Tanı Az Olası (+3)", "Taşikardi (+1.5)", "İmmobilite (+1.5)", "Önceki PE/DVT (+1.5)", "Hemoptizi (+1)", "Malignite (+1)"])
    st.info(f"Wells Toplam: {len(w_puan)}")
with s2:
    gks = st.select_slider("Glasgow Koma Skalası", options=list(range(3, 16)), value=15)
    if gks <= 8: st.error("⚠️ HAVA YOLU KORUNMALI (ENTÜBASYON)")
with s3:
    st.markdown("**Sıvı Gereksinimi**")
    st.success(f"Bazal İdame: {kilo * 35} cc/gün")

# 5. DEVASA KLİNİK SORGU MATRİSİ (HİÇBİR ŞEY SİLİNMEDİ)
st.subheader("🔍 Klinik Bulguları Belirleyin")
tab_sys, tab_heart, tab_gis, tab_brain, tab_endo, tab_rheum = st.tabs(["🧬 SİSTEMİK", "🫀 KARDİYO-PULMONER", "🤢 GİS & KC", "🧠 NÖROLOJİ", "🧪 ENDOKRİN", "🩸 HEMATO-ROMATO"])

bulgular = []
with tab_sys: bulgular.extend(st.multiselect("Semptom", ["Ateş", "Kilo Kaybı", "Gece Terlemesi", "Halsizlik", "Lenfadenopati", "Kaşıntı", "Anemi Bulguları", "Yaygın Ağrı"]))
with tab_heart: bulgular.extend(st.multiselect("Semptom ", ["Göğüs Ağrısı", "Nefes Darlığı", "Ortopne", "PND", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Boyun Ven Dolgunluğu", "Çarpıntı", "Ral", "Ronküs", "S3/S4", "Üfürüm"]))
with tab_gis: bulgular.extend(st.multiselect("Semptom  ", ["Sarılık", "Asit", "Hematemez", "Melena", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae", "Kuşak Ağrı", "Karın Ağrısı", "Bulantı", "Hıçkırık"]))
with tab_brain: bulgular.extend(st.multiselect("Semptom   ", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Fokal Kayıp", "Ani Baş Ağrısı", "Tremor", "Ataksi", "Dizartri", "Fotofobi"]))
with tab_endo: bulgular.extend(st.multiselect("Semptom    ", ["Poliüri", "Polidipsi", "Oligüri", "Anüri", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Pretibial Miksödem", "Guatr"]))
with tab_rheum: bulgular.extend(st.multiselect("Semptom     ", ["Peteşi", "Purpura", "Kelebek Döküntü", "Raynaud", "Sabah Sertliği", "Eklem Ağrısı", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit"]))

# 6. DEVASA DAHİLİYE ANSİKLOPEDİSİ (TANI + TETKİK + TEDAVİ)
master_arsiv = {
    "Karaciğer Sirozu": {
        "bulgu": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"],
        "tetkik": "INR, Albümin, Bilirubin, Amonyak, Batın USG, Portal Doppler, Gastroskopi (Varis?)",
        "tedavi": "Spironolakton 100mg + Furosemid 40mg, Laktüloz, Tuz Kısıtlaması, Varis varsa Propranolol"
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgu": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Bulantı"],
        "tetkik": "Kan Gazı (pH < 7.3, HCO3 < 18), İdrar Ketoni, Anyon Açığı, K+, Glukoz > 250",
        "tedavi": f"İnsülin 0.1 Ü/kg/saat ({round(kilo*0.1,1)} Ü/sa), SF Hidrasyonu (İlk saat 1L), K+ replasmanı"
    },
    "Pulmoner Emboli": {
        "bulgu": ["Hemoptizi", "Unilateral Ödem", "Nefes Darlığı", "Göğüs Ağrısı", "Taşikardi"],
        "tetkik": "BT Anjiyo (Altın Standart), D-Dimer, Troponin, EKG (S1Q3T3), Alt Ekstremite RDUS",
        "tedavi": f"Düşük Molekül Ağırlıklı Heparin ({kilo}mg 2x1), Masifse Trombolitik (tPA)"
    },
    "Kalp Yetmezliği (KKY)": {
        "bulgu": ["Bilateral Ödem", "Ortopne", "PND", "Boyun Ven Dolgunluğu", "Ral"],
        "tetkik": "NT-proBNP, EKO (EF Ölçümü), EKG, PA Akciğer Grafisi",
        "tedavi": "Furosemid IV, ACE İnhibitörü (veya ARB), Beta Bloker, SGLT2 İnhibitörü, MRA"
    },
    "Sistemik Lupus (SLE)": {
        "bulgu": ["Kelebek Döküntü", "Eklem Ağrısı", "Ağızda Aft", "Peteşi", "Fotosensitivite"],
        "tetkik": "ANA, Anti-dsDNA, Anti-Smith, C3-C4, Tam İdrar (Proteinüri/Hematüri)",
        "tedavi": "Hidroksiklorokin (Plaquenil) 200mg, Steroid, Gerekirse Siklofosfamid/Rituksimab"
    },
    "Akut Pankreatit": {
        "bulgu": ["Kuşak Ağrı", "Bulantı", "Karın Ağrısı"],
        "tetkik": "Lipaz (Spesifik), Amilaz, Kontrastlı Üst Batın BT (48-72. saatte nekroz için)",
        "tedavi": "Agresif Ringer Laktat, NPO (Ağızdan beslenme kes), Analjezi (Meperidin)"
    },
    "Menedjit (Bakteriyel)": {
        "bulgu": ["Ateş", "Ense Sertliği", "Konfüzyon", "Ani Baş Ağrısı", "Fotofobi"],
        "tetkik": "Lomber Ponksiyon (BOS Analizi), Kan Kültürü, Kafa BT (KİBAS ekarte etmek için)",
        "tedavi": "Seftriakson 2x2g + Vankomisin + Deksametazon (Antibiyotikten 15 dk önce)"
    },
    "Feokromositoma": {
        "bulgu": ["Çarpıntı", "Ani Baş Ağrısı", "Terleme", "Taşikardi"],
        "tetkik": "24h İdrar Metanefrin/VMA, Plazma Serbest Metanefrinleri, Sürrenal BT/MR",
        "tedavi": "Önce Alfa Bloker (Doksazosin/Fenoksibenzamin), 10 gün sonra Beta Bloker"
    },
    "Addison Hastalığı/Krizi": {
        "bulgu": ["Hiperpigmentasyon", "Hipotansiyon", "Tuz Açlığı", "Halsizlik"],
        "tetkik": "Sabah 08:00 Kortizolü, ACTH Stimülasyon Testi, Na (Düşük), K (Yüksek)",
        "tedavi": "Hidrokortizon (IV/Oral) + Fludrokortizon (Mineralokortikoid)"
    },
    "Wegener (GPA)": {
        "bulgu": ["Hemoptizi", "Peteşi", "Nefes Darlığı", "Eklem Ağrısı"],
        "tetkik": "c-ANCA (PR3-ANCA), Akciğer BT (Kavitasyon?), Böbrek Biyopsisi",
        "tedavi": "Pulse Steroid (1g/gün), Siklofosfamid veya Rituksimab"
    },
    "Tirotoksikoz (Graves)": {
        "bulgu": ["Ekzoftalmi", "Çarpıntı", "Kilo Kaybı", "Terleme", "Guatr"],
        "tetkik": "TSH (Düşük), sT4/sT3 (Yüksek), TSH Reseptör Antikoru (TRAB), Tiroid USG/Sintigrafi",
        "tedavi": "Metimazol (Propilthiourasil), Propranolol (Semptomatik), Radyoaktif İyot"
    },
    "Nefrotik Sendrom": {
        "bulgu": ["Bilateral Ödem", "Asit", "Oligüri", "Halsizlik"],
        "tetkik": "24h İdrar Proteini (>3.5g), Serum Albümin (<3g), Kolesterol Yüksekliği",
        "tedavi": "Steroid (Prednizolon), ACEi, Diüretik, Tuz Kısıtlaması, Statiler"
    }
}

# 7. ANALİZ MOTORU VE EPİKRİZ JENERATÖRÜ
if st.button("🚀 MASTER ANALİZİ ÇALIŞTIR"):
    if not bulgular:
        st.error("En az bir klinik bulgu seçmelisiniz!")
    else:
        sonuclar = []
        for ad, veri in master_database.items():
            eslesme = set(bulgular).intersection(set(veri["bulgu"]))
            if eslesme:
                puan = round((len(eslesme) / len(veri["bulgu"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": veri, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        col_res1, col_res2 = st.columns([1.6, 1])
        with col_res1:
            st.markdown("### 🧬 Tanısal Algoritma Sonuçları")
            for s in sonuclar:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2rem; color:#2563EB; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p>🎯 <b>Tespit Edilen Belirtiler:</b> {", ".join(s['esles'])}</p>
                    <p>🧪 <b>İstenmesi Gereken Tetkikler:</b> {s['veri']['tetkik']}</p>
                    <p>💊 <b>Modern Tedavi Protokolü:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)

        with col_res2:
            st.markdown("### 📝 RESMİ EPİKRİZ")
            r_not = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / ÖN HİDRASYON"
            epikriz = f"""TIBBİ KARAR ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
PROTOKOL: {p_no}

[VİTAL PARAMETRELER]
Yaş: {yas} | Kilo: {kilo}kg | eGFR: {egfr}
Glukoz: {glu} | K+: {k_plus} | TA: {ta_sis}

[KLİNİK BULGULAR]
{", ".join(bulgular)}

[DİFERANSİYEL TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[KLİNİK NOTLAR]
- Radyoloji: {r_not}
- GKS: {gks} | Günlük Sıvı: {kilo*35}cc
--------------------------------------------------
ONAY VE İMZA: İSMAİL ORHAN
"""
            st.markdown(f"<pre style='background:white; padding:30px; border-radius:20px; border:1px solid #E2E8F0;'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Raporu PDF Arşivine Gönder", epikriz, file_name=f"{p_no}_final.txt")

st.markdown("---")
st.caption("Geliştirici: İSMAİL ORHAN | Unified Medical OS V14 | 2026")
