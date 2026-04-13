import streamlit as st
from datetime import datetime

# 1. TASARIM: ULTRA MODERN KLİNİK KOMUTA MERKEZİ
st.set_page_config(page_title="Medical Omniscience v20", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #020617; color: #f1f5f9; }
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding: 50px;
        border-radius: 30px; text-align: center; border: 1px solid #4338ca;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6); margin-bottom: 30px;
    }
    .diag-card { 
        background: rgba(30, 41, 59, 0.7); border: 1px solid #4338ca; 
        padding: 25px; border-radius: 20px; margin-bottom: 15px;
    }
    .section-title { color: #818cf8; font-weight: 800; font-size: 1.2em; border-bottom: 2px solid #312e81; margin-bottom: 10px; }
    .epikriz-paper { 
        background: #ffffff; color: #1e293b; padding: 35px; border-radius: 5px; 
        font-family: 'Courier New', monospace; line-height: 1.2; border: 5px double #475569;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4338ca, #6d28d9, #be185d);
        color: white; border-radius: 20px; height: 5.5em; font-weight: 900; font-size: 22px;
        transition: 0.3s; border: none;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 30px #6366f1; }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>🏥 MEDICAL OMNISCIENCE v20.0</h1><p>Tanı | Tetkik | Tedavi | Radyoloji | Epikriz | İSMAİL ORHAN Full Stack Medicine</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL (VİTAL TERMİNAL)
with st.sidebar:
    st.header("📊 VİTAL PARAMETRELER")
    h_ad = st.text_input("Hasta ID", "PROTOKOL_2026")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 250, 75)
    st.divider()
    ates = st.number_input("Ateş (°C)", 30.0, 45.0, 36.6, format="%.1f")
    ta_sis = st.number_input("Sistolik TA", 40, 280, 120)
    spo2 = st.slider("SpO2 (%)", 30, 100, 98)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    st.info(f"eGFR: {round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0}")

# 4. TÜM TIP SEMPTOM VE BULGU HAVUZU
st.subheader("🧬 Klinik Bulgular (Multidisipliner Giriş)")
c1, c2, c3 = st.columns(3)
with c1:
    b1 = st.multiselect("Gastro & Hepato", ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Melena", "Karahindiba Görünümü", "Murphy (+)", "Karın Ağrısı"])
    b2 = st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Ortopne/PND", "Bilateral Ödem", "Unilateral Ödem", "Üfürüm", "S3/S4 Sesi", "Boyun Ven Dolgunluğu"])
with c2:
    b3 = st.multiselect("Nöro & Toksiko", ["Konfüzyon", "Ense Sertliği", "Fokal Defisit", "Miyozis", "Midriyazis", "Hipersalivasyon", "Ani Baş Ağrısı", "Nöbet"])
    b4 = st.multiselect("Solunum & KBB", ["Hemoptizi", "Wheezing", "Stridor", "Plevritik Ağrı", "Çomak Parmak", "Öksürük"])
with c3:
    b5 = st.multiselect("Hematolo & Romato", ["Peteşi/Purpura", "Lenfadenopati", "Kelebek Döküntü", "Oral/Genital Ülser", "Eklem Ağrısı", "Sabah Sertliği"])
    b6 = st.multiselect("Endokrin & Renal", ["Aseton Kokusu", "Poliüri", "Polidipsi", "Oligüri", "Kilo Kaybı", "Ekzoftalmi", "Hiperpigmentasyon"])

hepsi = b1 + b2 + b3 + b4 + b5 + b6

# 5. DEVASA TIP VERİTABANI (TANI + TETKİK + TEDAVİ)
# Her hastalık için en güncel protokoller burada.
tıp_arsivi = {
    "Siroz ve Portal Hipertansiyon": {
        "bulgular": ["Asit", "Hepatomegali", "Splenomegali", "Sarılık", "Hematemez", "Karahindiba Görünümü"],
        "tetkik": "Batın USG (Portal ven çapı), Karaciğer Fonksiyon Testleri, PT/INR, Amonyak, Endoskopi (Varis tarama).",
        "tedavi": "Sodyum kısıtlaması, Spironolakton/Furosemid, Varis varsa Propranolol, Laktüloz (Ensefalopati önlemi).",
        "radyoloji": "Kontrastsız Batın BT veya Doppler USG."
    },
    "Konjesif Kalp Yetmezliği (KKY)": {
        "bulgular": ["Bilateral Ödem", "Ortopne/PND", "Hepatomegali", "Asit", "S3/S4 Sesi", "Boyun Ven Dolgunluğu"],
        "tetkik": "EKO (EF ölçümü), NT-proBNP, Akciğer Grafisi (Kerley B çizgileri), EKG.",
        "tedavi": "IV Furosemid, ACE İnhibitörü/ARNI, Beta-Bloker, SGLT2 İnhibitörü.",
        "radyoloji": "PA Akciğer Grafisi (Kardiyomegali kontrolü)."
    },
    "Diyabetik Ketoasidiz (DKA)": {
        "bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon", "Karın Ağrısı"],
        "tetkik": "Kan Şekeri (>250), Kan Gazı (pH <7.3), Ketonyüri, Anyon Açığı Hesabı.",
        "tedavi": "IV Hidrasyon (SF), IV İnsülin İnfüzyonu (0.1 u/kg/sa), Potasyum Replasmanı.",
        "radyology": "Genelde gerekmez; presipite eden faktör için PA AC Grafisi."
    },
    "Organofosfat Zehirlenmesi": {
        "bulgular": ["Miyozis", "Hipersalivasyon", "Wheezing", "Karın Ağrısı"],
        "tetkik": "Plazma Kolinesteraz Düzeyi.",
        "tedavi": "ACİL ATROPİN (Yanıt alana kadar), Pralidoksim (PAM), Dekontaminasyon.",
        "radyoloji": "Sekonder pnömoni şüphesinde PA AC Grafisi."
    },
    "Sistemik Lupus (SLE)": {
        "bulgular": ["Kelebek Döküntü", "Eklem Ağrısı", "Sabah Sertliği", "Plevritik Ağrı"],
        "tetkik": "ANA (Tarama), Anti-dsDNA, Anti-Smith, Kompleman (C3, C4) düzeyleri, Tam İdrar (Proteinüri).",
        "tedavi": "Hidroksiklorokin, Glukokortikoidler, İmmünsupresifler.",
        "radyoloji": "Efüzyon şüphesinde USG veya Grafi."
    }
}

# 6. ANALİZ MOTORU VE ÇIKTI PANELİ
if st.button("🚀 OMNISCIENCE SİSTEMİNİ ÇALIŞTIR"):
    if not hepsi:
        st.warning("Analiz için klinik bulgu seçmelisiniz.")
    else:
        egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1)
        st.divider()
        
        # Analiz Başlat
        col_res1, col_res2 = st.columns([1.2, 1])
        
        with col_res1:
            st.markdown("### 🧬 Multidisipliner Analiz Sonuçları")
            bulunan_hastaliklar = []
            for isim, veri in tıp_arsivi.items():
                eslesme = set(hepsi).intersection(set(veri["bulgular"]))
                if eslesme:
                    skor = round((len(eslesme) / len(veri["bulgular"])) * 100, 1)
                    bulunan_hastaliklar.append({"isim": isim, "puan": skor, "veri": veri, "eslesen": eslesme})
            
            # Skora göre sırala
            bulunan_hastaliklar = sorted(bulunan_hastaliklar, key=lambda x: x['puan'], reverse=True)

            for item in bulunan_hastaliklar:
                with st.container():
                    st.markdown(f"""
                    <div class='diag-card'>
                        <div class='section-title'>{item['isim']} (%{item['puan']} Uyum)</div>
                        <p><b>Eşleşen Bulgular:</b> {", ".join(item['eslesen'])}</p>
                        <p><b style='color:#10b981'>🔬 Önerilen Tetkikler:</b> {item['veri']['tetkik']}</p>
                        <p><b style='color:#ef4444'>💊 Tedavi Protokolü:</b> {item['veri']['tedavi']}</p>
                        <p><b style='color:#8b5cf6'>📡 Radyoloji Rehberi:</b> {item['veri']['radyoloji']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        with col_res2:
            st.markdown("### 📝 RESMİ KLİNİK EPİKRİZ")
            # Radyoloji Güvenlik Notu
            rad_not = "Kontrastlı tetkik uygundur." if egfr > 60 else "⚠️ DİKKAT: eGFR düşük, kontrastsız tetkik tercih edilmeli!"
            
            epikriz = f"""KLİNİK DURUM VE TEDAVİ ÖZETİ
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
HASTA ID: {h_ad} | YAŞ: {yas} | KİLO: {kilo}kg
VİTALLER: Ateş {ates}C | TA {ta_sis}mmHg | SpO2 %{spo2}

[BÖBREK FONKSİYONU VE RADYOLOJİ GÜVENLİĞİ]
- eGFR: {egfr} mL/dk
- {rad_not}

[GÖZLEMLENEN KLİNİK BULGULAR]
{", ".join(hepsi)}

[OLASI TANILAR VE AYIRICI TANI]
{chr(10).join([f"- {h['isim']} (Uyum: %{h['puan']})" for h in bulunan_hastaliklar[:3]])}

[PLANLANAN TETKİK VE TEDAVİ]
{chr(10).join([f"* {h['isim']} için: {h['veri']['tedavi'][:100]}..." for h in bulunan_hastaliklar[:2]])}

--------------------------------------------------
Onay: Medical Omniscience v20 | Dr. İsmail Orhan
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("📥 Epikrizi PDF/TXT Olarak Al", epikriz, file_name=f"{h_ad}_medical_final.txt")

st.markdown("---")
st.caption("v20.0 Omniscience | Tüm Tıp Branşları, Tetkikler ve Tedaviler | İsmail Orhan Özel Sürüm")
