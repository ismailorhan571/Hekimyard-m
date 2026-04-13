import streamlit as st
from datetime import datetime

# 1. LUXURY BEIGE & GOLD INTERFACE (ULTRA-MODERN NEUMORPHIC)
st.set_page_config(page_title="İSMAİL ORHAN | Global Medical Matrix V15", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    /* Bej ve Lüks Arka Plan */
    .stApp { background: linear-gradient(135deg, #F5F5DC 0%, #E8E2D2 100%); color: #2C2C2C; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Premium Header */
    .main-header {
        background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px);
        padding: 60px; border-radius: 45px; text-align: center; margin-bottom: 40px;
        border: 2px solid #D4AF37; box-shadow: 0 30px 60px rgba(0,0,0,0.05);
    }
    .main-header h1 { 
        color: #1A1A1A; font-weight: 800; font-size: 4.2rem; letter-spacing: -3px; margin: 0;
    }
    .main-header p { color: #D4AF37; font-size: 1.5rem; font-weight: 600; margin-top: 10px; }
    
    /* Gösterişli Kartlar */
    .diag-card { 
        background: #FFFFFF; padding: 40px; border-radius: 40px; margin-bottom: 30px;
        border: 1px solid #E2E2E2; box-shadow: 20px 20px 60px #D9D9D9, -20px -20px 60px #FFFFFF;
        border-top: 12px solid #D4AF37; transition: 0.4s ease;
    }
    
    /* Devasa Analiz Butonu */
    .stButton>button {
        background: linear-gradient(135deg, #1A1A1A 0%, #4A4A4A 100%); color: #D4AF37; border-radius: 30px;
        height: 6.5em; width: 100%; font-weight: 800; font-size: 28px; border: 2px solid #D4AF37;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2); cursor: pointer;
    }
    .stButton>button:hover { transform: scale(1.02); background: #000000; color: #FFD700; }
    
    /* Kritik Uyarı Paneli */
    .alert-box { 
        background: #B91C1C; color: white; padding: 20px; border-radius: 25px;
        font-weight: 800; text-align: center; margin-bottom: 15px; border: 3px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST KOMUTA PANELİ
st.markdown(f"""
    <div class='main-header'>
        <h1>TIBBİ KARAR Analiz ROBOTU</h1>
        <p>Geliştirici: İSMAİL ORHAN</p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL - VİTAL & HESAPLAMALAR
with st.sidebar:
    st.markdown("### 🏛️ HASTA TERMİNALİ")
    p_no = st.text_input("Protokol", "IO-GOLD-V15")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 250, 75)
    st.divider()
    glu = st.number_input("Glukoz", 0, 1500, 105)
    kre = st.number_input("Kreatinin", 0.1, 20.0, 1.0)
    k_plus = st.number_input("Potasyum", 1.0, 12.0, 4.2)
    ta_sis = st.number_input("Sistolik TA", 30, 300, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kre), 1) if kre > 0 else 0
    st.metric("Böbrek Rezervi (eGFR)", f"{egfr} ml/dk")
    
    if egfr < 30: st.markdown("<div class='alert-box'>🚨 DİKKAT: RENAL DOZ!</div>", unsafe_allow_html=True)
    if k_plus > 5.5: st.markdown("<div class='alert-box'>🚨 K+ KRİTİK SEVİYE!</div>", unsafe_allow_html=True)

# 4. SKORLAMA ÜSSÜ
st.subheader("🧮 Gelişmiş Skorlama ve Klinik Metrikler")
c1, c2, c3 = st.columns(3)
with c1:
    wells = st.multiselect("Wells PE Kriterleri", ["DVT (+3)", "Alt. Tanı Az (+3)", "Nabız >100 (+1.5)", "İmmobilite (+1.5)", "Önceki DVT/PE (+1.5)", "Hemoptizi (+1)", "Kanser (+1)"])
    st.info(f"Wells Puanı: {len(wells)}")
with c2:
    gks = st.select_slider("Glasgow Koma Skalası", options=list(range(3, 16)), value=15)
    if gks <= 8: st.error("⚠️ ACİL ENTÜBASYON ENDİKASYONU")
with c3:
    st.markdown("**Sıvı Hesaplayıcı**")
    st.success(f"Günlük İdame: {kilo * 35} cc/24s")

# 5. DEVASA KLİNİK SORGU MATRİSİ (HİÇBİR ŞEY SİLİNMEDİ - YENİLER EKLENDİ)
st.subheader("🔍 Klinik Bulguları Eksiksiz Tanımlayın")
t_gen, t_cp, t_gis, t_endo, t_rheum, t_tox = st.tabs(["🧬 SİSTEMİK", "🫀 KALP-AKCİĞER", "🤢 GİS-KC", "🧪 ENDOKRİN-RENAL", "🩸 ROMATO-HEMATO", "⚠️ TOKSİKO-ONKO"])

bulgular = []
with t_gen: bulgular.extend(st.multiselect("Genel Bulgular", ["Ateş", "Kilo Kaybı", "Gece Terlemesi", "Halsizlik", "Kaşıntı", "Lenfadenopati", "Anemi Bulguları", "Ödem (Yaygın)"]))
with t_cp: bulgular.extend(st.multiselect("Kardiyo-Pulmoner", ["Göğüs Ağrısı", "Nefes Darlığı", "Ortopne", "PND", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Boyun Ven Dolgunluğu", "Çarpıntı", "Ral", "Ronküs", "S3/S4 Sesleri", "Taşikardi"]))
with t_gis: bulgular.extend(st.multiselect("Gastro-Hepatobilier", ["Sarılık", "Asit", "Hematemez", "Melena", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae", "Kuşak Ağrısı", "Karın Ağrısı", "Bulantı-Kusma"]))
with t_endo: bulgular.extend(st.multiselect("Endokrin-Renal", ["Poliüri", "Polidipsi", "Oligüri", "Anüri", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Pretibial Miksödem", "Köpüklü İdrar"]))
with t_rheum: bulgular.extend(st.multiselect("Romatoloji-Hemato", ["Peteşi", "Purpura", "Kelebek Döküntü", "Raynaud Belirtisi", "Sabah Sertliği", "Eklem Ağrısı", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "B Semptomları"]))
with t_tox: bulgular.extend(st.multiselect("Toksikoloji-Onkoloji", ["Miyozis", "Midriyazis", "Bradikardi", "Hipotoni", "Karakteristik Koku", "Kemik Ağrısı", "Paraneoplastik Bulgular"]))

# 6. DEVASA MASTER VERİ TABANI (TANI + TETKİK + TEDAVİ)
# İSİMLENDİRME HATASI DÜZELTİLDİ: master_database
master_database = {
    "Karaciğer Sirozu": {
        "bulgu": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"],
        "tetkik": "INR, Albümin, Bilirubin, Amonyak, Batın USG, Portal Doppler",
        "tedavi": "Spironolakton 100mg + Furosemid 40mg, Laktüloz, Tuz Kısıtlaması"
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgu": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Bulantı-Kusma", "Karın Ağrısı"],
        "tetkik": "Kan Gazı (pH < 7.3), İdrar Ketoni, Glukoz > 250, Anyon Açığı",
        "tedavi": f"İnsülin 0.1 Ü/kg/saat ({round(kilo*0.1,1)} Ü/saat), Agresif SF Hidrasyonu, K+ Takibi"
    },
    "Pulmoner Emboli": {
        "bulgu": ["Hemoptizi", "Unilateral Ödem", "Nefes Darlığı", "Göğüs Ağrısı", "Taşikardi"],
        "tetkik": "BT Anjiyo, D-Dimer, Troponin, EKG (S1Q3T3)",
        "tedavi": f"Enoksaparin {kilo}mg 2x1 S.C., Masifse Trombolitik"
    },
    "Sistemik Lupus (SLE)": {
        "bulgu": ["Kelebek Döküntü", "Eklem Ağrısı", "Ağızda Aft", "Peteşi", "Fotosensitivite"],
        "tetkik": "ANA, Anti-dsDNA, Anti-Smith, C3-C4, Tam İdrar (Proteinüri)",
        "tedavi": "Hidroksiklorokin 200mg, Steroid, Gerekirse İmmünsupresif"
    },
    "Menedjit (Bakteriyel)": {
        "bulgu": ["Ateş", "Ense Sertliği", "Ani Baş Ağrısı", "Bulantı-Kusma"],
        "tetkik": "Lomber Ponksiyon (BOS Analizi), Kan Kültürü, Kafa BT",
        "tedavi": "Seftriakson 2x2g + Vankomisin + Deksametazon"
    },
    "Akut Pankreatit": {
        "bulgu": ["Kuşak Ağrısı", "Bulantı-Kusma", "Hipotoni", "Karın Ağrısı"],
        "tetkik": "Lipaz, Amilaz, Kontrastlı Batın BT",
        "tedavi": "NPO (Ağızdan beslenme kes), Agresif Ringer Laktat Hidrasyonu"
    },
    "Addison Krizi": {
        "bulgu": ["Hiperpigmentasyon", "Halsizlik", "Kilo Kaybı", "Tuz Açlığı"],
        "tetkik": "ACTH Stimülasyon, Na (Düşük), K (Yüksek), Kortizol",
        "tedavi": "IV Hidrokortizon 100mg + Agresif Sıvı Rezidansı"
    },
    "Feokromositoma": {
        "bulgu": ["Çarpıntı", "Ani Baş Ağrısı", "Terleme", "Taşikardi"],
        "tetkik": "Plazma Metanefrinleri, Sürrenal BT",
        "tedavi": "Önce Alfa Bloker (Doksazosin), Sonra Beta Bloker"
    },
    "Nefrotik Sendrom": {
        "bulgu": ["Bilateral Ödem", "Asit", "Oligüri", "Köpüklü İdrar"],
        "tetkik": "24h İdrar Proteini (>3.5g), Serum Albümin, Lipid Paneli",
        "tedavi": "Steroid (Prednizolon), ACE İnhibitörü, Diüretik"
    },
    "Wegener (GPA)": {
        "bulgu": ["Hemoptizi", "Peteşi", "Purpura", "Nefes Darlığı"],
        "tetkik": "c-ANCA (PR3-ANCA), Akciğer BT, Renal Biyopsi",
        "tedavi": "Pulse Steroid (1g) + Siklofosfamid/Rituksimab"
    }
}

# 7. ANALİZ MOTORU
if st.button("🚀 MASTER ANALİZİ ÇALIŞTIR"):
    if not bulgular:
        st.error("En az bir klinik bulgu seçilmelidir!")
    else:
        st.divider()
        sonuclar = []
        # Hatanın düzeltildiği nokta: master_database.items()
        for ad, veri in master_database.items():
            eslesme = set(bulgular).intersection(set(veri["bulgu"]))
            if eslesme:
                skor = round((len(eslesme) / len(veri["bulgu"])) * 100, 1)
                sonuclar.append({"ad": ad, "skor": skor, "veri": veri, "ortak": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['skor'], reverse=True)
        
        res_c1, res_c2 = st.columns([1.6, 1])
        with res_c1:
            st.markdown("### 🏛️ Teşhis, Tetkik ve Tedavi Matrisi")
            for s in sonuclar:
                st.markdown(f"""
                <div class='diag-card'>
                    <div style='font-size:2.2rem; color:#1A1A1A; font-weight:800;'>{s['ad']} (%{s['skor']})</div>
                    <p style='color:#D4AF37; font-weight:700;'>🎯 Eşleşen Bulgular: {", ".join(s['ortak'])}</p>
                    <hr style='border: 0.5px solid #E2E2E2;'>
                    <p>🧪 <b>Gerekli Tetkikler:</b> {s['veri']['tetkik']}</p>
                    <p>💊 <b>Altın Standart Tedavi:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with res_c2:
            st.markdown("### 📝 RESMİ EPİKRİZ")
            r_not = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / HİDRASYON"
            epikriz = f"""KLİNİK ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
PROTOKOL: {p_no}

[VİTAL PARAMETRELER]
Yaş: {yas} | Kilo: {kilo}kg | eGFR: {egfr}
Glukoz: {glu} | Potasyum: {k_plus} | TA: {ta_sis}

[SEÇİLEN KLİNİK BULGULAR]
{", ".join(bulgular)}

[ÖN TANILAR VE UYUM]
{chr(10).join([f"- {x['ad']} (%{x['skor']})" for x in sonuclar[:5]])}

[GÜVENLİK VE NOTLAR]
- Radyoloji: {r_not}
- GKS: {gks} | Günlük Sıvı: {kilo*35}cc
--------------------------------------------------
ONAY: İSMAİL ORHAN
"""
            st.markdown(f"<pre style='background:white; padding:40px; border-radius:30px; border:2px solid #D4AF37; font-size:14px; box-shadow: 10px 10px 30px rgba(0,0,0,0.05);'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Raporu PDF Olarak Arşivle", epikriz, file_name=f"{p_no}_io_final.txt")

st.markdown("---")
st.caption("Geliştirici: İSMAİL ORHAN | Global Integrated Medical System V15 | 2026")
