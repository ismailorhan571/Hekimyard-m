import streamlit as st
from datetime import datetime

# 1. ULTRA-MODERN PREMİUM ARAYÜZ (VISIONARY WHITE)
st.set_page_config(page_title="İSMAİL ORHAN | Nihai Klinik Sistem", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp { background: #F8FAFC; color: #1E293B; font-family: 'Inter', sans-serif; }
    
    .header-box {
        background: white; padding: 50px; border-radius: 30px; text-align: center;
        border: 1px solid #E2E8F0; box-shadow: 0 10px 40px rgba(0,0,0,0.03); margin-bottom: 30px;
    }
    .header-box h1 { color: #2563EB; font-weight: 800; font-size: 3.2rem; }
    
    .clinical-card {
        background: white; border: 1px solid #E2E8F0; padding: 25px; border-radius: 20px;
        margin-bottom: 20px; border-left: 10px solid #3B82F6; box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    
    .stButton>button {
        background: #2563EB; color: white; border-radius: 12px; height: 4em; width: 100%;
        font-weight: 700; font-size: 20px; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background: #1D4ED8; transform: translateY(-2px); }
    
    .status-badge { padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown(f"""
    <div class='header-box'>
        <h1>TIBBİ OPERASYON VE KARAR MERKEZİ</h1>
        <p>Geliştirici: <b>İSMAİL ORHAN</b> | Dahiliye / Acil / Yoğun Bakım Entegre Sistemi</p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL (VİTAL & LAB)
with st.sidebar:
    st.header("📊 HASTA PROFİLİ")
    h_no = st.text_input("Protokol", "İO-PRO-2026")
    yas = st.number_input("Yaş", 0, 110, 45)
    kilo = st.number_input("Kilo (kg)", 3, 200, 75)
    st.divider()
    st.markdown("### 🩸 LABORATUVAR")
    glu = st.number_input("Glukoz", 20, 1000, 105)
    kre = st.number_input("Kreatinin", 0.1, 15.0, 1.0)
    k_plus = st.number_input("Potasyum", 1.0, 10.0, 4.0, 0.1)
    ta_sis = st.number_input("Sistolik Tansiyon", 40, 250, 120)
    
    egfr = round(((140 - yas) * kilo) / (72 * kre), 1) if kre > 0 else 0
    st.metric("eGFR", f"{egfr} ml/dk")
    if egfr < 30: st.error("🚨 RENAL YETMEZLİK")

# 4. EN GENİŞ TIBBİ VERİ KÜTÜPHANESİ (Hastalık + Belirti + Tetkik + Tedavi)
# Hiçbir veri silinmedi, hepsi tek sözlükte birleştirildi.
klinik_arsiv = {
    "Karaciğer Sirozu": {
        "belirtiler": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae", "Palmar Eritem"],
        "tetkik": "INR, Albümin, Amonyak, Batın USG, Portal Ven Doppler",
        "tedavi": "Spironolakton 100mg + Furosemid 40mg, Laktüloz, Ensefalopati varsa Neomisin"
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "belirtiler": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Kussmaul Solunumu", "Karın Ağrısı"],
        "tetkik": "Venöz Kan Gazı (pH < 7.3), İdrar Ketoni, Kan Şekeri > 250",
        "tedavi": f"İnsülin Perfüzyon (0.1 Ü/kg/saat = {round(kilo*0.1,1)} Ü/sa), Agresif SF Hidrasyonu"
    },
    "Pulmoner Emboli": {
        "belirtiler": ["Hemoptizi", "Unilateral Ödem", "Taşikardi", "Nefes Darlığı", "Plevritik Ağrı"],
        "tetkik": "BT Anjiyo (Altın Standart), D-Dimer, EKG (S1Q3T3), Ekokardiyografi",
        "tedavi": f"Enoksaparin {kilo}mg 2x1 S.C. veya IV Heparin, Stabil değilse Trombolitik"
    },
    "Kalp Yetmezliği (KKY)": {
        "belirtiler": ["Bilateral Ödem", "Ortopne", "PND", "Boyun Ven Dolgunluğu", "Ral/Ronküs", "S3 Sesi"],
        "tetkik": "NT-proBNP, EKG, PA Akciğer Grafisi, EKO (EF Ölçümü)",
        "tedavi": "Furosemid (Lasilix) 2x1, ACE İnhibitörü, Beta Bloker, Tuz Kısıtlaması"
    },
    "Sistemik Lupus (SLE)": {
        "belirtiler": ["Kelebek Döküntü", "Eklem Ağrısı", "Peteşi", "Oral Aft", "Fotosensitivite"],
        "tetkik": "ANA, Anti-dsDNA, C3-C4, Tam İdrar (Proteinüri takibi)",
        "tedavi": "Hidroksiklorokin (Plaquenil), Sistemik Steroid, İmmünsupresifler"
    },
    "Akut Pankreatit": {
        "belirtiler": ["Kuşak Tarzı Ağrı", "Bulantı", "Hipotansiyon", "Epigastrik Hassasiyet"],
        "tetkik": "Amilaz/Lipaz (3 kat artış), Kontrastlı Batın BT",
        "tedavi": "NPO (Oral Stop), Agresif Sıvı Resüsitasyonu, Analjezi (Meperidin)"
    },
    "Feokromositoma": {
        "belirtiler": ["Aralıklı Hipertansiyon", "Terleme", "Çarpıntı", "Baş Ağrısı"],
        "tetkik": "24h İdrar Metanefrinleri, Sürrenal BT/MR",
        "tedavi": "Alfa Bloker (Doksazosin) ardından Beta Bloker, Cerrahi"
    },
    "Menedjit (Bakteriyel)": {
        "belirtiler": ["Ateş", "Ense Sertliği", "Konfüzyon", "Ani Baş Ağrısı", "Pozitif Kerning"],
        "tetkik": "Lomber Ponksiyon (BOS Analizi), Kan Kültürü, Kafa BT",
        "tedavi": "Seftriakson 2x2g + Vankomisin + Deksametazon (LP öncesi)"
    },
    "Nefrotik Sendrom": {
        "belirtiler": ["Anazarka Ödem", "Köpüklü İdrar", "Yorgunluk", "Hipertansiyon"],
        "tetkik": "24h İdrar Proteini (>3.5g), Albümin düşüklüğü, Lipid Paneli",
        "tedavi": "Steroid Tedavisi, ACEi (Proteinüri azaltmak için), Diüretik"
    },
    "Addison Hastalığı": {
        "belirtiler": ["Hiperpigmentasyon", "Hipotansiyon", "Tuz Açlığı", "Halsizlik"],
        "tetkik": "ACTH Stimülasyon Testi, Sabah Kortizolü, Elektrolit (Na düşük, K yüksek)",
        "tedavi": "Hidrokortizon + Fludrokortizon"
    }
}

# 5. MERKEZİ BELİRTİ GİRİŞİ (ÇOKLU SEÇİM)
st.subheader("🩺 Klinik Tabloyu Tanımlayın")
col_a, col_b = st.columns(2)

hepsi = []
with col_a:
    with st.expander("🧬 SİSTEMİK VE DAHİLİ BULGULAR", expanded=True):
        hepsi.extend(st.multiselect("Seçiniz", ["Ateş", "Kilo Kaybı", "Gece Terlemesi", "Halsizlik", "Sarılık", "Kelebek Döküntü", "Oral Aft", "Peteşi", "Mor Stria", "Aydede Yüzü", "Hiperpigmentasyon", "Tuz Açlığı"]))
    with st.expander("🫀 KARDİYO-PULMONER"):
        hepsi.extend(st.multiselect("Seçiniz ", ["Nefes Darlığı", "Göğüs Ağrısı", "Taşikardi", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Boyun Ven Dolgunluğu", "Ortopne", "PND", "Ral/Ronküs"]))

with col_b:
    with st.expander("🤢 GASTRO VE HEPATOBİLİER", expanded=True):
        hepsi.extend(st.multiselect("Seçiniz  ", ["Asit", "Karın Ağrısı", "Kuşak Tarzı Ağrı", "Hematemez", "Melena", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae", "Bulantı"]))
    with st.expander("🧠 NÖROLOJİ VE RENAL"):
        hepsi.extend(st.multiselect("Seçiniz   ", ["Ense Sertliği", "Konfüzyon", "Nöbet", "Ani Baş Ağrısı", "Poliüri", "Polidipsi", "Oligüri", "Anüri", "Aseton Kokusu", "Köpüklü İdrar"]))

# 6. ANALİZ VE NİHAİ ÇIKTI
if st.button("🚀 SİSTEM ANALİZİNİ GERÇEKLEŞTİR"):
    if not hepsi:
        st.error("Lütfen klinik bulgu seçimi yapınız.")
    else:
        st.divider()
        sonuclar = []
        for ad, veri in klinik_arsiv.items():
            eslesme = set(hepsi).intersection(set(veri["belirtiler"]))
            if eslesme:
                puan = round((len(eslesme) / len(veri["belirtiler"])) * 100, 1)
                sonuclar.append({"ad": ad, "skor": puan, "veri": veri, "ortak": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['skor'], reverse=True)
        
        c1, c2 = st.columns([1.7, 1])
        with c1:
            st.markdown("### 🔬 Klinik Tanı Matrisi")
            for s in sonuclar:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:1.8rem; color:#2563EB; font-weight:800;'>{s['ad']} (%{s['skor']})</div>
                    <p style='margin-top:10px;'>🎯 <b>Eşleşen Belirtiler:</b> {", ".join(s['ortak'])}</p>
                    <p>🧪 <b>Gerekli Tetkikler:</b> {s['veri']['tetkik']}</p>
                    <p>💊 <b>Tedavi Protokolü:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📝 RESMİ EPİKRİZ")
            r_not = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK ŞART"
            epikriz = f"""TIBBİ KARAR ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
PROTOKOL: {h_no}

[VİTAL PARAMETRELER]
Yaş: {yas} | Kilo: {kilo}kg | eGFR: {egfr}
Glukoz: {glu} | K+: {k_plus} | TA: {ta_sis}

[SEÇİLEN KLİNİK BULGULAR]
{", ".join(hepsi)}

[OLASI TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['skor']})" for x in sonuclar[:5]])}

[GÜVENLİK NOTU]
- {r_not}

--------------------------------------------------
ONAY: İSMAİL ORHAN
"""
            st.markdown(f"<pre style='background:white; padding:30px; border:1px solid #E2E8F0; border-radius:15px;'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Raporu TXT Olarak İndir", epikriz, file_name=f"{h_no}_final.txt")

st.markdown("---")
st.caption("Geliştirici: İSMAİL ORHAN | Nihai Klinik Veri Tabanı V12 | 2026")
