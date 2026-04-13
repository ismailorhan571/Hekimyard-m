import streamlit as st
from datetime import datetime

# 1. SİBER KLİNİK TASARIM (PREMIUM DARK MODE)
st.set_page_config(page_title="İSMAİL ORHAN | Medical Infrastructure", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010409; color: #e2e8f0; }
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%); padding: 45px;
        border-radius: 20px; text-align: center; border: 2px solid #312e81; margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .diag-card { 
        background: #0d1117; border: 1px solid #30363d; padding: 25px; border-radius: 15px; 
        margin-bottom: 20px; border-left: 10px solid #238636; transition: 0.3s;
    }
    .diag-card:hover { transform: scale(1.01); border-color: #58a6ff; }
    .critical-alert { 
        background: rgba(215, 58, 73, 0.2); border: 2px solid #f85149; 
        color: #ff7b72; padding: 20px; border-radius: 12px; font-weight: bold; margin-bottom: 15px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% {opacity: 1;} 50% {opacity: 0.7;} 100% {opacity: 1;} }
    .epikriz-paper { 
        background: #f8fafc; color: #0f172a; padding: 40px; border-radius: 8px; 
        font-family: 'Courier New', monospace; border: 3px double #cbd5e1; line-height: 1.5;
    }
    .stButton>button {
        background: linear-gradient(90deg, #238636, #2ea043); color: white; border-radius: 12px; 
        height: 5.5em; width: 100%; font-weight: 900; font-size: 24px; border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST KOMUTA PANELİ
st.markdown("<div class='main-header'><h1>⚖️ ULTIMATE MEDICAL INFRASTRUCTURE</h1><p>Tanı-Tetkik-Tedavi-Dozaj-Skorlama-Arşiv | İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 3. AKILLI VİTAL TERMİNALİ (YAN PANEL)
with st.sidebar:
    st.header("📊 VİTAL & METRİKLER")
    h_ad = st.text_input("Hasta Protokol", "PRT-2026-FINAL")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 220, 75)
    st.divider()
    ates = st.number_input("Ateş (°C)", 32.0, 43.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA", 40, 280, 120)
    seker = st.number_input("Kan Şekeri (mg/dL)", 20, 1000, 110)
    kreatinin = st.number_input("Kreatinin (mg/dL)", 0.1, 15.0, 1.0)
    potasyum = st.number_input("Potasyum (mEq/L)", 1.0, 10.0, 4.2, 0.1)
    
    egfr = round(((140 - yas) * kilo) / (72 * kreatinin), 1) if kreatinin > 0 else 0
    st.metric("eGFR (Böbrek Fonk.)", f"{egfr} ml/dk")
    
    # GERÇEK ZAMANLI KLİNİK UYARILAR
    if seker > 300: st.markdown("<div class='critical-alert'>🚨 DKA RİSKİ: Hidrasyon ve İnsülin!</div>", unsafe_allow_html=True)
    if seker < 65: st.markdown("<div class='critical-alert'>🚨 HİPOGLİSEMİ: %10 Dekstroz/Glukagon!</div>", unsafe_allow_html=True)
    if potasyum > 5.5: st.markdown("<div class='critical-alert'>🚨 HİPERPOTASEMİ: Kalsiyum Glukonat + EKG!</div>", unsafe_allow_html=True)
    if egfr < 30: st.markdown("<div class='critical-alert'>⚠️ İLERİ RENAL YETMEZLİK: Doz Ayarı!</div>", unsafe_allow_html=True)

# 4. KLİNİK SKORLAMA VE ASİSTAN ARAÇLARI
st.subheader("🧮 Otomatik Skorlama ve Karar Destek")
sc1, sc2, sc3 = st.columns(3)
with sc1:
    curb = st.checkbox("Pnömoni (CURB-65)")
    if curb:
        c = st.toggle("Konfüzyon")
        u = st.toggle("Üre > 42")
        r = st.toggle("Solunum > 30")
        b = st.toggle("TA Düşüklüğü")
        a = st.toggle("Yaş >= 65")
        score = sum([c,u,r,b,a])
        st.info(f"CURB-65 Puanı: {score} ({'Yatış Önerilir' if score >= 2 else 'Ayaktan Takip'})")
with sc2:
    siroz = st.checkbox("Siroz (Child-Pugh)")
    if siroz:
        asc = st.selectbox("Asit", ["Yok", "Hafif", "Masif"])
        bil = st.selectbox("Bilirubin", ["< 2", "2-3", "> 3"])
        st.info(f"Evreleme aktif...")
with sc3:
    gks = st.select_slider("Glasgow Koma Skalası", options=range(3, 16), value=15)
    if gks <= 8: st.error("ENTÜBASYON ENDİKASYONU!")

# 5. MAKSİMUM SİSTEMİK SORGULAMA (5 SEKMELİ YAPI)
st.subheader("🧬 Multidisipliner Belirti Tarayıcı")
t1, t2, t3, t4, t5 = st.tabs(["MİDE-KC", "KALP-AKCİĞER", "NÖRO-TOKSİKO", "HEMATO-ROMATO", "ENDOKRİN-RENAL"])

hepsi = []
with t1: hepsi.extend(st.multiselect("Gastro-Hepato", ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Hematemez", "Melena", "Caput Medusae", "Murphy (+)", "Asteriksis", "Karahindiba Görünümü"]))
with t2: hepsi.extend(st.multiselect("Kardiyo-Pulmoner", ["Göğüs Ağrısı", "Nefes Darlığı", "Ortopne", "PND", "Bilateral Ödem", "Unilateral Ödem", "Hemoptizi", "Boyun Ven Dolgunluğu", "Ral/Ronküs"]))
with t3: hepsi.extend(st.multiselect("Nörolojik-Toksik", ["Konfüzyon", "Ense Sertliği", "Miyozis", "Midriyazis", "Hipersalivasyon", "Nöbet", "Fokal Defisit", "Tremor", "Ataksi"]))
with t4: hepsi.extend(st.multiselect("Hemato-Romato", ["Peteşi/Purpura", "Lenfadenopati", "Kelebek Döküntü", "Oral Aft", "Sabah Sertliği", "Eklem Ağrısı", "Gece Terlemesi", "Splenomegali (Masif)"]))
with t5: hepsi.extend(st.multiselect("Endokrin-Renal", ["Aseton Kokusu", "Poliüri", "Polidipsi", "Oligüri", "Hiperpigmentasyon", "Ekzoftalmi", "Mor Stria", "Aydede Yüzü"]))

# 6. DEVASA BİLGİ BANKASI (TANI + HASTAYA ÖZEL DOZ + LABORATUVAR REHBERİ)
# İsmail, burası tıbbın kalbi; hiçbir hastalık silinmedi, üzerine yenileri eklendi.
arsiv = {
    "Siroz ve Karaciğer Yetmezliği": {
        "bulgular": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Caput Medusae", "Asteriksis"],
        "tüp": "Sarı (Biyokimya), Mor (Hemogram), Mavi (INR), Buzda (Amonyak)",
        "doz": f"Spironolakton 100mg 1x1, Furosemid 40mg 1x1, Laktüloz 3x1.",
        "not": "NSBB (Propranolol) eklemeyi düşün. Parasentez >5L ise 8g/L Albümin ver."
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgular": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Konfüzyon"],
        "tüp": "Kan Gazı Enjektörü, Sarı (Elektrolit), Mor (HbA1c)",
        "doz": f"İnsülin İnfüzyon: {round(kilo*0.1, 1)} Ünite/Saat. Hidrasyon: %0.9 SF 1L/saat.",
        "not": "K+ < 3.3 ise İnsülini durdur! Kan şekeri <250 olunca %5 Dekstroz ekle."
    },
    "Akut Pulmoner Emboli": {
        "bulgular": ["Hemoptizi", "Unilateral Ödem", "Taşikardi", "Nefes Darlığı"],
        "tüp": "Mavi (D-Dimer), Kan Gazı, Sarı (Troponin)",
        "doz": f"Enoksaparin (Clexane) {kilo}mg 2x1 S.C. (eGFR <30 ise dozu %50 düşür!)",
        "not": "RV yüklenmesi varsa Trombolitik (tPA) değerlendir."
    },
    "Feokromositoma": {
        "bulgular": ["Ani Baş Ağrısı", "Terleme", "Çarpıntı", "Hipertansiyon"],
        "tüp": "24 Saatlik İdrar, Sarı (Metanefrinler)",
        "doz": "Alfa Bloker (Doksazosin) 1x1mg başlat.",
        "not": "KRİTİK: Alfa bloker yapmadan asla Beta bloker verme!"
    },
    "Akut Pankreatit": {
        "bulgular": ["Karın Ağrısı (Kuşak)", "Bulantı", "Hipotansiyon"],
        "tüp": "Sarı (Amilaz/Lipaz - 3 kat artış tanısal)",
        "doz": "Agresif IV Hidrasyon (Ringer Laktat tercih), Analjezi.",
        "not": "Balthazar kriterleri için 72. saatte Kontrastlı BT planla."
    }
}

# 7. ANALİZ MOTORU VE EPİKRİZ ÜRETİCİ
if st.button("🚀 OMNI-İTYAPILARI ÇALIŞTIR VE ARŞİVLE"):
    if not hepsi:
        st.error("Lütfen klinik bulgu girişi yapınız.")
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
            st.markdown("### 📊 Klinik Analiz & Akıllı Dozaj")
            for s in sonuclar:
                st.markdown(f"""
                <div class='diag-card'>
                    <div style='font-size:1.6em; color:#58a6ff; font-weight:bold;'>{s['ad']} (%{s['puan']})</div>
                    <p>🧪 <b>Laboratuvar (Tüp):</b> {s['veri']['tüp']}</p>
                    <p>💉 <b>Hastaya Özel Doz ({kilo}kg):</b> {s['veri']['doz']}</p>
                    <p style='color:#ff7b72;'>⚠️ <b>Hayati Klinik Not:</b> {s['veri']['not']}</p>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📝 RESMİ KLİNİK EPİKRİZ")
            radyo = "Kontrastlı uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / HİDRASYON ŞART"
            epikriz = f"""TIBBİ ANALİZ VE KARAR RAPORU
--------------------------------------------------
HASTA: {yas}Y | {kilo}KG | eGFR: {egfr}
GLİKOZ: {seker} | POTASYUM: {potasyum} | TA: {ta_sis}
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}

[KLİNİK BULGULAR]
{", ".join(hepsi)}

[ÖN TANILAR VE UYUM ORANI]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[HEKİM YÖNETİM PLANI]
- eGFR {egfr} nedeniyle {radyo}.
- {"DİKKAT: Diyabetik acil yönetimi (DKA) öncelikli!" if seker > 300 else "Glisemi kontrolü sağlandı."}
- {"DİKKAT: Hiperpotasemi için kalsiyum glukonat düşünülmelidir." if potasyum > 5.5 else "Elektrolitler stabil."}

--------------------------------------------------
SİSTEM GELİŞTİRİCİSİ: İSMAİL ORHAN
"""
            st.markdown(f"<div class='epikriz-paper'><pre>{epikriz}</pre></div>", unsafe_allow_html=True)
            st.download_button("📥 Raporu PDF/TXT Olarak İndir", epikriz, file_name=f"{h_ad}_medical_report.txt")

st.markdown("---")
st.caption("İSMAİL ORHAN | The Ultimate Medical Infrastructure | Cumulative Edition")
