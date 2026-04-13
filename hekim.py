import streamlit as st
from datetime import datetime

# 1. ULTRA PREMİUM SAYFA TASARIMI
st.set_page_config(page_title="Dahiliye CDSS Supreme Archive v18", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020617 0%, #080a0f 50%, #1e1b4b 100%); color: #f1f5f9; }
    .main-header {
        background: rgba(30, 41, 59, 0.9); padding: 60px; border-radius: 40px;
        border: 2px solid #6366f1; text-align: center; margin-bottom: 40px;
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.3);
    }
    .status-card { padding: 25px; border-radius: 20px; margin-bottom: 20px; font-weight: 500; }
    .emergency { background: rgba(220, 38, 38, 0.15); border-left: 10px solid #ef4444; border-right: 1px solid #ef4444; }
    .diagnostic { background: rgba(37, 99, 235, 0.15); border-left: 10px solid #3b82f6; border-right: 1px solid #3b82f6; }
    .radiology { background: rgba(139, 92, 246, 0.15); border-left: 10px solid #8b5cf6; border-right: 1px solid #8b5cf6; }
    .epikriz-box { background: #ffffff; color: #000; padding: 40px; border-radius: 10px; font-family: 'Courier New', monospace; border: 4px solid #475569; }
    .stButton>button {
        background: linear-gradient(90deg, #1e3a8a, #581c87, #831843);
        color: white; border-radius: 30px; height: 6em; font-weight: 900; font-size: 24px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5); transition: 0.4s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 20px 60px rgba(99, 102, 241, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>⚕️ DAHİLİYE CDSS - THE SUPREME ARCHIVE v18.0</h1><p style='font-size:1.4em'>Tüm Dahiliye Müfredatı | Radyoloji Rehberi | Toksikoloji | İSMAİL ORHAN Ultimate Software</p></div>", unsafe_allow_html=True)

# 3. VERİ GİRİŞİ (VİTALLER VE LAB)
with st.sidebar:
    st.header("📊 HASTA TERMİNALİ")
    h_ad = st.text_input("Protokol No / Hasta Adı", "PROTOKOL_X")
    yas = st.number_input("Yaş", 18, 120, 45)
    kilo = st.number_input("Vücut Ağırlığı (kg)", 30, 250, 75)
    st.divider()
    ates = st.slider("Vücut Isısı (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik Tansiyon", 40, 300, 120)
    ta_dia = st.number_input("Diastolik Tansiyon", 30, 200, 80)
    nabiz = st.number_input("Nabız (Vuru/dk)", 20, 300, 80)
    spo2 = st.slider("Oksijen Satürasyonu (%SpO2)", 30, 100, 98)
    kreatinin = st.number_input("Serum Kreatinin (mg/dL)", 0.1, 20.0, 1.0)
    st.divider()
    st.warning("⚠️ Radyoloji için Kreatinin değerini kontrol ediniz!")

# 4. DEV SEMPTOM MATRİSİ (HİÇBİR ŞEYİ ATLAMADAN)
st.subheader("🔍 Klinik Belirti ve Toksikolojik Bulgular")
t1, t2, t3, t4, t5, t6 = st.tabs(["GİS & HEPATO", "KARDİYO & SOLUNUM", "NÖRO & TOKSİKO", "HEMATO & ONKO", "ROMATO & NEFRO", "ENDOKRİN"])

secilen = []
with t1:
    secilen.extend(st.multiselect("Sindirim Sistemi", ["Hematemez", "Melena", "Sarılık", "Asit", "Disfaji", "Hepatomegali", "Splenomegali", "Karahindiba Görünümü", "Asteriksis", "Abdominal Hassasiyet"]))
with t2:
    secilen.extend(st.multiselect("Dolaşım & Solunum", ["Baskı Tarzı Göğüs Ağrısı", "Plevritik Ağrı", "Hemoptizi", "Ortopne", "Bacakta Ödem (Tek Taraflı)", "Boyun Ven Dolgunluğu", "Çomak Parmak", "Ral/Ronküs"]))
with t3:
    secilen.extend(st.multiselect("Sinir & Zehirlenme", ["Ani Şiddetli Baş Ağrısı", "Miyozis (İğne ucu)", "Midriyazis (Geniş)", "Hipersalivasyon (Salyada artış)", "Konfüzyon", "Ense Sertliği", "Fokal Defisit", "Ataksi"]))
with t4:
    secilen.extend(st.multiselect("Kan & Tümör", ["Peteşi/Purpura", "Ekimoz", "Diş Eti Kanaması", "Lenfadenopati", "B-Semptomları (Gece terlemesi, Kilo kaybı)", "Schistosit Şüphesi", "Anemi Bulguları"]))
with t5:
    secilen.extend(st.multiselect("Bağ Dokusu & Böbrek", ["Kelebek Döküntü", "Poliartrit", "Güneş Hassasiyeti", "Oligüri (İdrar miktarında azalma)", "Hematüri", "Üremik Koku", "Oral/Genital Ülser"]))
with t6:
    secilen.extend(st.multiselect("Metabolizma", ["Aseton Kokusu", "Poliüri", "Polidipsi", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Buffalo Hörgücü"]))

# 5. SUPREME ANALİZ MOTORU
if st.button("🚀 TÜM DAHİLİYE ARŞİVİNİ TARA VE ANALİZ ET"):
    
    # Yerel Matematiksel Hesaplamalar
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1)
    b = set(secilen)
    tanilar, tedaviler, ddx, rad_rehber = [], [], [], []

    # --- 1. KARDİYOLOJİ & VASKÜLER ---
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        tanilar.append("AKUT KORONER SENDROM")
        ddx.append("Ayırıcı Tanı: Aort Diseksiyonu, Pulmoner Emboli, Perikardit, GÖRH")
        rad_rehber.append("Öneri: EKG, Seri Troponin, EKO. Aort Diseksiyonu şüphesinde Kreatinin normalse Kontrastlı Toraks BT.")
        tedaviler.append("ASA 300mg + Klopidogrel 300mg (veya Tikagrelor)")

    # --- 2. GASTROENTEROLOJİ & HEPATOLOJİ ---
    if "Hematemez" in b or "Melena" in b:
        tanilar.append("ÜST GİS KANAMA")
        ddx.append("Ayırıcı Tanı: Peptik Ülser, Varis Kanama, Mallory-Weiss")
        rad_rehber.append("Öneri: Direkt Radyoloji yerine ACİL ENDOSKOPİ birincil tercihtir.")
        tedaviler.append("IV PPI İnfüzyonu (80mg bolus + 8mg/saat)")

    # --- 3. TOKSİKOLOJİ (YENİ KATMAN) ---
    if "Miyozis (İğne ucu)" in b and "Hipersalivasyon (Salyada artış)" in b:
        tanilar.append("KOLİNERJİK KRİZ (Organofosfat Zehirlenmesi)")
        tedaviler.append("ACİL ANTİDOT: ATROPİN (Yanıt alınana kadar doz artırımı)")
        tedaviler.append("Pralidoksim (PAM) tedavisi düşünülmelidir.")
        
    if "Midriyazis (Geniş)" in b and "Konfüzyon" in b:
        tanilar.append("ANTİKOLİNERJİK TOKSİDROM")
        ddx.append("Ayırıcı Tanı: TCA Zehirlenmesi, Atropin Doz Aşımı")

    # --- 4. HEMATOLOJİ & ONKOLOJİ ---
    if "Peteşi/Purpura" in b and "Schistosit Şüphesi" in b:
        tanilar.append("TROMBOTİK TROMBOSİTOPENİK PURPURA (TTP)")
        tedaviler.append("ACİL PLAZMAFEREZ (Gecikme hayati risk taşır)")
        tedaviler.append("Trombosit transfüzyonundan kaçınılmalıdır!")

    # --- 5. RADYOLOJİ REHBERİ (YENİ KATMAN) ---
    if egfr < 30:
        rad_rehber.append("⚠️ KRİTİK UYARI: eGFR < 30. İyotlu kontrast kullanımı kontrendikedir. Kontrastsız tetkik veya MR-Hidrasyon planlanmalıdır.")
    elif egfr < 60:
        rad_rehber.append("⚠️ UYARI: eGFR 30-60 aralığında. Kontrast kullanımı öncesi ve sonrası IV hidrasyon (SF) önerilir.")

    # --- 6. NEFROLOJİ & SIVI RESÜSİTASYONU ---
    if "Oligüri (İdrar miktarında azalma)" in b:
        tanilar.append("AKUT BÖBREK HASARI (Prerenal / Renal / Postrenal?)")
        rad_rehber.append("Öneri: Üriner Sistem USG (Obstrüksiyon ekarte etmek için)")

    # 7. SONUÇLARIN SERGİLENMESİ
    st.divider()
    col_a, col_b = st.columns([1, 1.2])

    with col_a:
        st.markdown("<div class='status-card emergency'><h3>🚨 TANI VE AYIRICI TANI</h3>", unsafe_allow_html=True)
        for t in tanilar: st.write(f"🚩 **{t}**")
        for d in ddx: st.write(f"🔍 *{d}*")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='status-card radiology'><h3>🩻 RADYOLOJİ VE GÖRÜNTÜLEME REHBERİ</h3>", unsafe_allow_html=True)
        for r in rad_rehber: st.write(f"📡 {r}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("### 📝 PROFESYONEL KLİNİK EPİKRİZ")
        epikriz = f"""KLİNİK EPİKRİZ RAPORU - {datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
HASTA: {h_ad} | YAŞ: {yas} | eGFR: {egfr} mL/dk
VİTALLER: Ateş {ates}C | TA {ta_sis}/{ta_dia}mmHg | SpO2 %{spo2} | Nabız {nabiz}/dk

BELİRLENEN KLİNİK BULGULAR:
{', '.join(secilen) if secilen else 'Spesifik bulgu girilmedi.'}

[ANALİZ VE ÖN TANILAR]
{chr(10).join(['- ' + t for t in tanilar])}
{chr(10).join(['- ' + d for d in ddx])}

[RADYOLOJİ PLANI]
{chr(10).join(['* ' + r for r in rad_rehber])}

[ACİL TEDAVİ VE YÖNETİM]
{chr(10).join(['+ ' + ted for ted in tedaviler])}

--------------------------------------------------
Kayıt: Supreme Archive v18 | Sistem Sorumlusu: İsmail Orhan
"""
        st.markdown(f"<div class='epikriz-box'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
        st.download_button("📥 Epikrizi .txt Olarak Kaydet", epikriz, file_name=f"{h_ad}_supreme.txt")

st.markdown("---")
st.caption("Dahiliye Supreme Archive v18.0 | Full Spectrum Diagnostic Software | İSMAİL ORHAN")
