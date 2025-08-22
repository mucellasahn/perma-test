# perma_app.py
# -*- coding: utf-8 -*-
# PERMA iyilik hâli anketi (23 soru) – Streamlit tek dosya uygulaması
# Kaynak model: Seligman (2011) PERMA. Bu uygulama eğitim/öğrenme amaçlıdır; klinik tanı koymaz.

import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt

# ---------- Sayfa ayarı ----------
st.set_page_config(
    page_title="PERMA İyilik Hâli Testi (Demo)",
    page_icon="🌱",
    layout="centered",
)

# ---------- Yardımcılar ----------
def likert(label, key):
    return st.slider(label, 1, 7, 4, key=key,
                    help="1=Kesinlikle katılmıyorum ··· 7=Kesinlikle katılıyorum")

def radar_chart(scores):
    """scores: dict {'P': float, 'E': float, ...} 1–7 arası ortalamalar"""
    labels = ["P", "E", "R", "M", "A"]
    values = [scores[k] for k in labels]
    # radar kapanışı için tekrar başa ekle
    labels_wrap = labels + [labels[0]]
    values_wrap = values + [values[0]]

    angles = np.linspace(0, 2*math.pi, len(labels_wrap))
    fig = plt.figure(figsize=(4.8, 4.8))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values_wrap, linewidth=2)
    ax.fill(angles, values_wrap, alpha=0.15)
    ax.set_thetagrids(angles[:-1] * 180 / math.pi, labels)
    ax.set_ylim(1, 7)
    ax.set_title("PERMA Profilin (1–7)", pad=12)
    ax.grid(True)
    return fig

def explain_dimension(name):
    return {
        "P": "P (Positive Emotion) – Pozitif duygu: keyif, huzur, şükran vb. sıklığı.",
        "E": "E (Engagement) – Akış/katılım: kendini kaptırdığın, zamanın akıp gittiği anlar.",
        "R": "R (Relationships) – İlişkiler: sosyal destek, yakınlık ve aidiyet.",
        "M": "M (Meaning) – Anlam: yaşamda amaç ve değerlerle hizalanma.",
        "A": "A (Accomplishment) – Başarı: hedef koyma ve ilerleme duygusu."
    }[name]

# ---------- Başlık ----------
st.markdown("# 🌱 PERMA İyilik Hâli Testi")
st.caption("Seligman’ın PERMA modelinden esinlenen 23 maddelik kısa anket (öğrenme amaçlı demo).")
st.divider()

# ---------- Soru havuzu (23 madde) ----------
# Her madde bir boyuta etiketli: P/E/R/M/A
QUESTIONS = [
    # P – Positive Emotion (5)
    ("Son günlerde sık sık neşeli/huzurlu hissettim.", "P"),
    ("Kendimi genel olarak iyimser hissediyorum.", "P"),
    ("Gün içinde minik anlardan keyif alıyorum.", "P"),
    ("Şükran duyduğum şeyleri fark ediyorum.", "P"),
    ("Stresle baş ederken olumlu kalabiliyorum.", "P"),

    # E – Engagement (5)
    ("Bir işle meşgulken sıklıkla 'akış'a giriyorum (zamanın uçması).", "E"),
    ("Gün içinde kendimi tamamen kaptırdığım aktiviteler oluyor.", "E"),
    ("Yeteneklerimi zorlayan görevleri severim.", "E"),
    ("Odaklanmak benim için genelde kolaydır.", "E"),
    ("Yeni bir şey öğrenirken hevesli hissederim.", "E"),

    # R – Relationships (4)
    ("Yakın hissettiğim insanlarla kaliteli zaman geçiriyorum.", "R"),
    ("Zorlandığımda destek isteyebileceğim kişiler var.", "R"),
    ("Günlük yaşamımda anlamlı sosyal etkileşimler yaşıyorum.", "R"),
    ("İlişkilerim bana enerji veriyor.", "R"),

    # M – Meaning (4)
    ("Yaptıklarımın daha büyük bir amaca hizmet ettiğini hissediyorum.", "M"),
    ("Değerlerimle uyumlu yaşıyorum.", "M"),
    ("Kendimden daha büyük bir şeye aitlik hissim var.", "M"),
    ("Hayatıma yön veren bir amaç hissediyorum.", "M"),

    # A – Accomplishment (5)
    ("Gerçekçi hedefler koyar ve peşinden giderim.", "A"),
    ("Son zamanlarda anlamlı şeyler başardım.", "A"),
    ("Günümü planlamak ve tamamlamakta iyiyim.", "A"),
    ("Engellerle karşılaşınca vazgeçmem.", "A"),
    ("İlerlemediğimi hissettiğimde adım atarım.", "A"),
]

# ---------- Form ----------
with st.form("perma_form"):
    st.subheader("Soruları yanıtla")
    st.caption("Her maddeyi 1 (katılmıyorum) – 7 (katılıyorum) aralığında işaretle.")
    answers = []
    for i, (text, dim) in enumerate(QUESTIONS, start=1):
        val = likert(f"{i}. {text}", key=f"q{i}")
        answers.append((val, dim))
    submitted = st.form_submit_button("Skorumu Hesapla")

# ---------- Hesaplama ----------
if submitted:
    # boyutlara göre gruplama
    results = {"P": [], "E": [], "R": [], "M": [], "A": []}
    for val, dim in answers:
        results[dim].append(val)

    # ortalamalar
    means = {k: float(np.mean(v)) if v else 0.0 for k, v in results.items()}
    overall = float(np.mean(list(means.values())))

    st.success("Yanıtların alındı! Aşağıda profilin 👇")
    cols = st.columns(5)
    order = ["P", "E", "R", "M", "A"]
    for i, k in enumerate(order):
        with cols[i]:
            st.metric(k, f"{means[k]:.2f} / 7")
            st.caption(explain_dimension(k))

    st.markdown("### Radar Grafik")
    fig = radar_chart(means)
    st.pyplot(fig, use_container_width=True)

    st.markdown("### Genel PERMA Skoru")
    st.info(f"**{overall:.2f} / 7** \n"
            "Bu, beş boyutun ortalamasıdır. Gelişim için en düşük kalan alana küçük hedefler koyabilirsin.")

    # Basit öneri: en düşük boyuta ipucu
    lowest_dim = min(means, key=means.get)
    tips = {
        "P": "P: Gün sonunda 3 minik iyi olayı not et (gratitude).",
        "E": "E: Günün 25 dakikasını tek bir işe ayır; bildirimleri kapat.",
        "R": "R: Bu hafta birine minnet mesajı gönder / kahve molası ayarla.",
        "M": "M: Değerlerini yaz; haftalık hedeflerinden 1’ini bir değerinle eşleştir.",
        "A": "A: Haftaya 1 küçük bitirilebilir hedef tanımla ve takvimine koy."
    }
    st.markdown("### Mini İpucu")
    st.warning(tips[lowest_dim])

    st.divider()
    st.caption(
        "Kaynak: Seligman, M. E. P. (2011). *Flourish*. PERMA modeli esinleriyle hazırlanmış eğitim amaçlı bir demodur; "
        "klinik değerlendirme yerine kişisel farkındalık için kullanın."
    )
else:
    st.info("Formu doldurup **Skorumu Hesapla**'ya bas.")