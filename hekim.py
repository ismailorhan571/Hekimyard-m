import streamlit as st
from datetime import datetime

# 1. SAYFA KONFİGÜRASYONU VE ULTRA PREMİUM TASARIM
st.set_page_config(page_title="Dahiliye CDSS The Absolute v17", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
    .main-header {
        background: rgba(30, 41, 59, 0.8); padding: 50px; border-radius: 35px;
        border: 2px solid #6366f1; text-align: center; margin-bottom: 40px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .panel-red { background: rgba(239, 68, 68, 0.1); padding: 25px; border-radius: 20px; border-left: 8px solid #ef4444; margin-bottom: 15px; }
    .panel-blue { background: rgba(59, 130, 246, 0.1); padding: 25px; border-radius: 20px; border-left: 8px solid #3b82f6; margin-bottom: 15px; }
    .panel-orange { background: rgba(245, 158, 11, 0.1); padding: 25px; border-radius: 20px; border-left: 8px solid #f59e0b; margin-bottom: 15px; }
    .epikriz-box { background: #ffffff; color: #1e293b; padding: 30px; border-radius: 15px; font-family: monospace; border: 3px solid #94a3b8; line-height: 1.4; }
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5, #9333ea, #db2777); color: white;
        border-radius: 20px; height: 5.5em; width: 100%; font-weight: 900; font-size: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST BAŞLIK
st.markdown("<div class='main-header'><h1>⚕️ DAHİLİYE CDSS - THE ABSOLUTE v17.0</h1><p>Maksimum Veri Hacmi | Ayırıcı Tanı | Otomatik Epikriz | İSMAİL ORHAN Ultimate Edition</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL (VİTAL VE DEMOGRAFİK)
with st.sidebar:
    st.header("📊 HASTA TERMİNALİ")
    h_ad = st.text_input("Hasta ID / Protokol", "HASTA_99")
    yas = st.number_input("Yaş", 18, 115, 45)
    kilo = st.number_input("Kilo (kg)", 40, 200, 75)
    st.divider()
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik Tansiyon", 50, 250, 120)
    solunum = st.number_input("Solunum Sayısı (dk)", 8, 50, 16)
    spo2 = st.slider("Oksijen Satürasyonu (SpO2)", 40, 100, 98)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    bun = st.number_input("BUN (mg/dL)", 5, 200, 18)
    gks = st.selectbox("GKS (Bilinç)", [15, 14, 13, 12, 11, 10, 9, 8, 7])

# 4. DEVAŞA SEMPTOM VE KLİNİK BULGU PANELİ (TÜM SÜRÜMLERİN TOPLAMI)
st.subheader("🔍 Kapsamlı Klinik Parametre Girişi")
t1, t2, t3, t4, t5 = st.tabs(["🩺 GİS & HEPATO", "❤️ KARDİYO & SOLUNUM", "🧠 NÖRO & PSİK", "🦋 ROMATO & HEMATO", "🍭 ENDOKRİN & NEFRO"])

secilen = []
with t1:
    secilen.extend(st.multiselect("Gastrointestinal Bulgular", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Asteriksis", "Grey Turner", "Cullen", "Disfaji", "Odinofaji", "Murphy (+)", "Caput Medusae"]))
with t2:
    secilen.extend(st.multiselect("Kardiyopulmoner Bulgular", ["Baskı Tarzı Göğüs Ağrısı", "Nefes Darlığı", "Hemoptizi", "Tek Taraflı Bacak Şişliği", "PND/Ortopne", "Boyun Ven Dolgunluğu", "Janeway Lezyonları", "Osler Nodülleri"]))
with t3:
    secilen.extend(st.multiselect("Nörolojik Bulgular", ["Ani Baş Ağrısı", "Ense Sertliği", "Fokal Güç Kaybı", "Konfüzyon", "Ataksi", "Dizartri", "Miyozis", "Midriyazis"]))
with t4:
    secilen.extend(st.multiselect("Sistemik & Romatolojik", ["Kelebek Döküntü", "Oral Aft", "Genital Ülser", "Peteşi/Purpura", "Lenfadenopati", "Splenomegali", "Raynaud", "Gece Terlemesi", "Kilo Kaybı"]))
with t5:
    secilen.extend(st.multiselect("Metabolik & Renal", ["Aseton Kokusu", "Poliüri", "Polidipsi", "Oligüri", "Üremik Koku", "Hiperpigmentasyon", "Ekzoftalmi", "Buffalo Hörgücü", "Mor Stria"]))

# 5. DEV ANALİZ MOTORU (FONKSİYONSUZ, SATIR SATIR AÇIK MANTIK)
if st.button("🚀 TÜM SİSTEMLERİ ANALİZ ET VE EPİKRİZ OLUŞTUR"):
    
    # Yerel Hesaplamalar
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1)
    qsofa = 0
    if ta_sis <= 100: qsofa += 1
    if solunum >= 22: qsofa += 1
    if gks < 15: qsofa += 1
    
    curb = 0
    if bun > 19: curb += 1
    if solunum >= 30: curb += 1
    if ta_sis < 90: curb += 1
    if yas >= 65: curb += 1

    # Tanı, Ayırıcı Tanı ve Tedavi Listeleri (Her şey burada açıkça işleniyor)
    tanilar, ayiricilar, tedaviler = [], [], ["Hızlı Klinik Değerlendirme ve Vital Takibi"]
    b = set(secilen)

    # --- KRİTİK ALGORİTMALAR ---
    
    # Üst GİS Kanama Protokolü
    if "Hematemez" in b or "Melena" in b:
        tanilar.append("AKTİF ÜST GİS KANAMA (Peptik Ülser / Varis?)")
        ayiricilar.append("Ayırıcı Tanı: Özofagus Varisi, Mallory-Weiss, Gastrik Malignite, Dieulafoy Lezyonu")
        tedaviler.append("IV PPI Bolus 80mg + 8mg/saat İnfüzyon")
        tedaviler.append("Varis Şüphesinde Somatostatin/Oktreotid")
        tedaviler.append("Acil Endoskopi Planlaması")

    # Koroner Sendrom Protokolü
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        tanilar.append("AKUT KORONER SENDROM (STEMI/NSTEMI)")
        ayiricilar.append("Ayırıcı Tanı: Aort Diseksiyonu, Pulmoner Emboli, Perikardit, GÖRH")
        tedaviler.append("ASA 300mg Çiğnetme + Klopidogrel 300mg")
        tedaviler.append("Seri Troponin ve EKG Takibi")

    # Sepsis ve Enfeksiyon
    if qsofa >= 2:
        tanilar.append("OLASI SEPSİS TABLOSU (qSOFA Pozitif)")
        tedaviler.append("IV Kristaloid Replasmanı (30ml/kg)")
        tedaviler.append("Geniş Spektrumlu Antibiyoterapi (İlk 1 saatte)")

    # DKA / Metabolik
    if "Aseton Kokusu" in b or ("Poliüri" in b and "Konfüzyon" in b):
        tanilar.append("DİYABETİK KETOASİDOZ (DKA)")
        tedaviler.append("IV İnsülin İnfüzyonu (0.1 u/kg/saat)")
        tedaviler.append("SF İnfüzyonu ve K+ Takibi")

    # Behçet / Romato
    if "Oral Aft" in b and "Genital Ülser" in b:
        tanilar.append("BEHÇET HASTALIĞI (Vaskülit Şüphesi)")
        ayiricilar.append("Ayırıcı Tanı: HSV, Crohn Hastalığı, SLE")
        tedaviler.append("Kolşisin ve Topikal Steroid")

    # Böbrek Yetmezliği ve İlaç Ayarı
    if egfr < 30:
        tanilar.append("İLERİ DERECE BÖBREK YETMEZLİĞİ (eGFR < 30)")
        tedaviler.append("DİKKAT: Renal Doz Ayarlaması Gereken İlaçlar Gözden Geçirilmeli!")

    # 6. SONUÇ EKRANI VE EPİKRİZ
    st.divider()
    c1, c2 = st.columns([1, 1.2])

    with c1:
        st.markdown("<div class='panel-red'><h3>🚨 TANI VE AYIRICI TANI</h3>", unsafe_allow_html=True)
        for t in tanilar: st.write(f"🚩 **{t}**")
        for a in ayiricilar: st.write(f"🔍 *{a}*")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='panel-blue'><h3>💊 TEDAVİ VE YAKLAŞIM</h3>", unsafe_allow_html=True)
        for ted in tedaviler: st.write(f"✅ {ted}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("### 📝 OTOMATİK EPİKRİZ (HBYS UYUMLU)")
        epikriz = f"""HASTA KLİNİK ÖZETİ - {datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
HASTA ID: {h_ad} | YAŞ: {yas} | KİLO: {kilo}kg
VİTALLER: Ateş {ates}C | TA {ta_sis}mmHg | SpO2 %{spo2} | Solunum {solunum}/dk

KLİNİK ANALİZ:
- Hesaplanan eGFR: {egfr} mL/dk (Böbrek Fonksiyonu)
- qSOFA Skoru: {qsofa} (Sepsis Riski)
- CURB-65 Skoru: {curb} (Pnömoni Şiddeti)

TESPİT EDİLEN BULGULAR: {", ".join(secilen)}

ÖN TANILAR VE PLANI:
{chr(10).join(['- ' + t for t in tanilar])}
{chr(10).join(['- ' + a for a in ayiricilar])}

TEDAVİ NOTLARI:
{chr(10).join(['* ' + ted for ted in tedaviler])}

--------------------------------------------------
Hazırlayan: Dahiliye CDSS v17 (İsmail Orhan)"""
        st.markdown(f"<div class='epikriz-box'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
        st.download_button("📥 Epikrizi Kaydet (.txt)", epikriz, file_name=f"{h_ad}_epikriz.txt")

st.markdown("---")
st.caption("Dahiliye Absolute v17.0 | Monster Tulpar Optimized | İSMAİL ORHAN")
