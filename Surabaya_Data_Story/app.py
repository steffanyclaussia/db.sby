from pathlib import Path
import html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import spearmanr, kruskal

# ============================================================
# SATU KOTA, 31 CERITA — Streamlit Data Story
# Palet: Ink Navy, Parchment Cream, Burgundy, putih, hitam
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
IMG_DIR = BASE_DIR / "assets" / "images"
DATA_FILE = DATA_DIR / "data_bersih_plus_kemiskinan.csv"
CLUSTER_FILE = DATA_DIR / "hasil_cluster_per_kecamatan.csv"
PRIORITY_FILE = DATA_DIR / "kecamatan_prioritas_per_bidang.csv"

st.set_page_config(page_title="Satu Kota, 31 Cerita", page_icon="◫", layout="wide", initial_sidebar_state="expanded")

NAVY = "#1B2A3D"
CREAM = "#EDE3C8"
BURGUNDY = "#5C1F2E"
WHITE = "#FFFFFF"
BLACK = "#000000"
IVORY = "#FAF9F5"
MUTED = "#626262"
CLUSTER_COLORS = {1: NAVY, 2: BURGUNDY, 3: "#8C9AA8"}
REGIONS = ["Pusat", "Utara", "Timur", "Selatan", "Barat"]

# Font dan gaya global: Times New Roman, kontras tegas, sidebar outline.
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&display=swap');
html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
  font-family: 'Times New Roman', Times, serif !important;
  color: {BLACK};
}}
.stApp {{ background: {IVORY}; }}
[data-testid="stHeader"] {{ background: rgba(250,249,245,0.94); }}
[data-testid="stSidebar"] {{ background: {NAVY}; border-right: 1px solid rgba(237,227,200,.18); }}
[data-testid="stSidebar"] * {{ font-family: 'Times New Roman', Times, serif !important; }}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{ color: {CREAM}; }}
.block-container {{ padding-top: 1.7rem; padding-bottom: 3rem; max-width: 1440px; }}
h1,h2,h3,h4 {{ color: {NAVY} !important; font-family: 'Times New Roman', Times, serif !important; font-weight: 700 !important; }}
h1 {{ font-size: 2.55rem !important; line-height: 1.08 !important; }}
h2 {{ font-size: 1.9rem !important; }}
h3 {{ font-size: 1.35rem !important; }}
p, li, label, .stMarkdown {{ font-size: 1.03rem; line-height: 1.62; }}
[data-testid="stMetric"] {{ background: {WHITE}; border: 1px solid #E8E4DC; border-radius: 15px; padding: 15px 17px; box-shadow: 0 3px 12px rgba(27,42,61,.045); }}
[data-testid="stMetricLabel"] {{ color: {NAVY} !important; font-size: .98rem !important; font-weight: 700 !important; }}
[data-testid="stMetricValue"] {{ color: {BURGUNDY} !important; font-size: 2rem !important; font-weight: 700 !important; }}
.story-card {{ background: {WHITE}; border: 1px solid #E9E5DD; border-radius: 16px; padding: 19px 21px; box-shadow: 0 4px 15px rgba(27,42,61,.045); height: 100%; }}
.story-kicker {{ color: {BURGUNDY}; font-size: .78rem; letter-spacing: .12em; text-transform: uppercase; font-weight: 700; }}
.story-title {{ color: {NAVY}; font-size: 1.45rem; font-weight: 700; margin: .3rem 0 .55rem; line-height: 1.2; }}
.story-copy {{ color: #202020; font-size: 1.02rem; line-height: 1.62; }}
.hero {{ background: {NAVY}; border-radius: 22px; padding: 34px 36px; color: {CREAM}; }}
.hero h1 {{ color: {CREAM} !important; font-size: clamp(2.35rem,4vw,3.4rem) !important; margin-bottom: .5rem; }}
.hero p {{ color: {CREAM}; font-size: 1.12rem; max-width: 760px; }}
.pill {{ display:inline-block; background:{CREAM}; color:{BURGUNDY}; padding:5px 11px; border-radius:999px; font-size:.82rem; font-weight:700; }}
.nav-wrap {{ padding: 6px 5px 16px; }}
.nav-brand {{ color:{CREAM}; font-size:1.25rem; font-weight:700; padding:10px 10px 18px; border-bottom:1px solid rgba(237,227,200,.22); margin-bottom:14px; }}
a.nav-link {{ display:flex; align-items:center; gap:13px; color:{CREAM} !important; text-decoration:none !important; padding:11px 12px; border-radius:10px; margin:4px 0; font-size:1.02rem; border:1px solid transparent; }}
a.nav-link:hover {{ background:rgba(237,227,200,.12); border-color:rgba(237,227,200,.18); }}
a.nav-link.active {{ background:{CREAM}; color:{NAVY} !important; font-weight:700; }}
a.nav-link svg {{ width:21px; height:21px; flex:0 0 21px; stroke:currentColor; fill:none; stroke-width:1.65; stroke-linecap:round; stroke-linejoin:round; }}
.small-note {{ color:{MUTED}; font-size:.86rem; line-height:1.5; }}
hr {{ border-color:#E6E1D8 !important; }}
.stButton>button {{ background:{NAVY}; color:{CREAM}; border:1px solid {NAVY}; border-radius:9px; font-family:'Times New Roman',serif; font-weight:700; }}
.stButton>button:hover {{ background:{BURGUNDY}; color:{WHITE}; border-color:{BURGUNDY}; }}
[data-testid="stSelectbox"] label, [data-testid="stMultiSelect"] label {{ color:{NAVY}; font-weight:700; }}
[data-testid="stExpander"] {{ background:{WHITE}; border:1px solid #E7E1D8; border-radius:12px; }}
footer {{ visibility:hidden; }}
</style>
""", unsafe_allow_html=True)

# Outline SVG icons (Lucide-like visual language)
ICONS = {
"Beranda": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
"Apa yang Kita Ukur?": '<path d="M4 19V5M4 19h17"/><path d="m7 15 4-4 3 2 6-7"/><path d="M16 6h4v4"/>',
"Tidak Ada yang Seragam": '<path d="M4 19V5M4 19h17"/><path d="M7 15h2v2H7zM12 10h2v7h-2zM17 6h2v11h-2z"/>',
"Apa Hubungan Antarindikator?": '<circle cx="6" cy="7" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="11" cy="18" r="2"/><path d="m8 7 8-1M7 9l3 7m6-8-4 8"/>',
"Tiga Kelompok Kecamatan": '<circle cx="7" cy="7" r="3"/><circle cx="17" cy="7" r="3"/><circle cx="12" cy="17" r="3"/><path d="M9.5 9 11 14m3.5-5L13 14"/>',
"Di Mana Mereka Berada?": '<path d="m12 21-7-7a9 9 0 1 1 14 0z"/><circle cx="12" cy="10" r="2.5"/>',
"Siapa yang Perlu Perhatian?": '<path d="M4 19V5M4 19h17"/><path d="M7 16v-4h3v4m2 0V8h3v8m2 0V5h3v11"/>',
"Penutup: Dari Data ke Arah Perhatian": '<path d="M9 18h6m-5 3h4"/><path d="M8 14a7 7 0 1 1 8 0c-1 .7-1.5 1.5-1.5 2.5h-5C9.5 15.5 9 14.7 8 14Z"/><path d="M12 3v2"/>'
}
PAGES = list(ICONS.keys())

@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"File data tidak ditemukan: {DATA_FILE}")
    data = pd.read_csv(DATA_FILE)
    if CLUSTER_FILE.exists():
        cl = pd.read_csv(CLUSTER_FILE)
        keep = [c for c in ["Kecamatan", "Cluster_GMM", "Subcluster_GMM", "Probabilitas_Tertinggi_Cluster"] if c in cl.columns]
        data = data.merge(cl[keep], on="Kecamatan", how="left")
        # Nomor cluster GMM adalah label nominal. Ditata ulang untuk tampilan
        # agar sesuai urutan narasi: C1 (16), C2 (6), C3 (9).
        data["Cluster_Tampilan"] = data["Cluster_GMM"].map({3: 1, 2: 2, 1: 3})
        data["Subcluster_Tampilan"] = data["Subcluster_GMM"].astype(str).replace({
            "C3.1":"C1.1", "C3.3":"C1.2", "C3.2":"C1.3",
            "C2.1":"C2.1", "C2.3":"C2.2", "C2.2":"C2.3",
            "C1.3":"C3.1", "C1.2":"C3.2", "C1.1":"C3.3"
        })
    else:
        data["Cluster_Tampilan"] = np.nan
        data["Subcluster_Tampilan"] = "Belum tersedia"
    return data

try:
    df = load_data()
except Exception as exc:
    st.error(f"Tidak dapat membaca data: {exc}")
    st.stop()

NUMERIC = [
    "Kepadatan penduduk (jiwa/km²)", "Persentase penduduk usia produktif",
    "Persentase pendidikan tinggi", "Rasio murid:guru",
    "Tenaga kesehatan per 10.000 penduduk", "Fasilitas kesehatan per 10.000 penduduk",
    "Kepadatan Usaha per 10.000 penduduk", "Persentase penduduk miskin (%)"
]
DISPLAY = {
    "Kepadatan penduduk (jiwa/km²)": "Kepadatan penduduk",
    "Persentase penduduk usia produktif": "Penduduk usia produktif",
    "Persentase pendidikan tinggi": "Pendidikan tinggi",
    "Rasio murid:guru": "Rasio murid:guru",
    "Tenaga kesehatan per 10.000 penduduk": "Tenaga kesehatan / 10.000 penduduk",
    "Fasilitas kesehatan per 10.000 penduduk": "Fasilitas kesehatan / 10.000 penduduk",
    "Kepadatan Usaha per 10.000 penduduk": "Kepadatan usaha / 10.000 penduduk",
    "Persentase penduduk miskin (%)": "Penduduk miskin"
}
DOMAIN = {
    "Pendidikan": ["Persentase pendidikan tinggi", "Rasio murid:guru"],
    "Kesehatan": ["Tenaga kesehatan per 10.000 penduduk", "Fasilitas kesehatan per 10.000 penduduk"],
    "Ekonomi": ["Kepadatan Usaha per 10.000 penduduk"]
}

def image(name, width=None, caption=None):
    p = IMG_DIR / name
    if p.exists():
        st.image(str(p), width=width, caption=caption, use_container_width=(width is None))

def card(kicker, title, copy):
    st.markdown(f'<div class="story-card"><div class="story-kicker">{kicker}</div><div class="story-title">{title}</div><div class="story-copy">{copy}</div></div>', unsafe_allow_html=True)

def heading(kicker, title, intro):
    st.markdown(f'<div class="story-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(intro)
    st.divider()

def chart_layout(fig, height=390):
    fig.update_layout(
        height=height, paper_bgcolor=WHITE, plot_bgcolor=WHITE,
        font=dict(family="Times New Roman", color=BLACK, size=13),
        margin=dict(l=24, r=20, t=48, b=35),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0)
    )
    fig.update_xaxes(showgrid=False, linecolor="#D8D3CA")
    fig.update_yaxes(gridcolor="#ECE8E1", zerolinecolor="#C9C2B7")
    return fig

def domain_index(frame):
    out = pd.DataFrame(index=frame.index)
    # Samakan dengan prinsip indeks notebook: standardisasi indikator,
    # rasio murid:guru dibalik; kesehatan dan usaha menggunakan z-score.
    from scipy.stats import zscore
    out["Pendidikan"] = zscore(frame["Persentase pendidikan tinggi"], nan_policy="omit") - zscore(frame["Rasio murid:guru"], nan_policy="omit")
    out["Kesehatan"] = zscore(frame["Tenaga kesehatan per 10.000 penduduk"], nan_policy="omit") + zscore(frame["Fasilitas kesehatan per 10.000 penduduk"], nan_policy="omit")
    out["Ekonomi"] = zscore(frame["Kepadatan Usaha per 10.000 penduduk"], nan_policy="omit")
    return out

# Sidebar navigation dengan ikon outline custom, bukan emoji / ikon penuh warna.
current = st.query_params.get("page", "Beranda")
if current not in PAGES:
    current = PAGES[0]
with st.sidebar:
    st.markdown('<div class="nav-wrap"><div class="nav-brand">SATU KOTA, 31 CERITA<br><span style="font-size:.78rem;font-weight:400;opacity:.82">SURABAYA DATA STORY</span></div>', unsafe_allow_html=True)
    for label in PAGES:
        active = "active" if current == label else ""
        svg = f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[label]}</svg>'
        st.markdown(f'<a class="nav-link {active}" href="?page={html.escape(label)}">{svg}<span>{html.escape(label)}</span></a>', unsafe_allow_html=True)
    st.markdown('</div><div style="padding:8px 12px;color:#EDE3C8;opacity:.7;font-size:.78rem">Data: 31 kecamatan · 5 wilayah</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Eksplorasi data pendidikan, kesehatan, dan aktivitas ekonomi.")

# Header kecil konsisten
st.markdown(f'<div class="story-kicker">SURABAYA DATA STORY  /  {PAGES.index(current)+1:02d} — 08</div>', unsafe_allow_html=True)

# ----------------------------- PAGE 1 -----------------------------
if current == "Beranda":
    st.markdown(f'''<div class="hero"><div class="pill">DATA STORYTELLING · KOTA SURABAYA</div><h1>Satu Kota, 31 Cerita</h1><p>Membaca Surabaya lewat data pendidikan, kesehatan, dan aktivitas ekonomi. Apakah 31 kecamatan Surabaya punya cerita yang sama?</p></div>''', unsafe_allow_html=True)
    st.write("")
    c1,c2,c3 = st.columns(3)
    c1.metric("Kecamatan dianalisis", f"{df['Kecamatan'].nunique()}")
    c2.metric("Cluster utama", "3")
    c3.metric("Wilayah Surabaya", f"{df['Wilayah'].nunique()}")
    left,right = st.columns([1.25,1])
    with left:
        image("surabaya_skyline_day.png", caption="Surabaya: satu kota dengan karakteristik kecamatan yang beragam.")
    with right:
        st.markdown("### Satu kota, banyak wajah")
        st.write("Surabaya kerap dilihat sebagai satu kesatuan kota. Namun, setiap kecamatan memiliki kondisi yang berbeda. Ada wilayah dengan indikator pendidikan dan layanan kesehatan relatif tinggi, sementara wilayah lain menghadapi tantangan kepadatan penduduk, kemiskinan, atau keterbatasan aktivitas usaha.")
        st.write("Melalui data 31 kecamatan, perjalanan ini mengajak kita mengenali perbedaan tersebut, menemukan pola, dan melihat wilayah yang membutuhkan perhatian lebih lanjut.")
        if st.button("Mulai Menjelajah →", use_container_width=True):
            st.query_params["page"] = PAGES[1]
            st.rerun()
    st.markdown("### Tiga hal yang akan ditemukan")
    a,b,c = st.columns(3)
    with a: card("01 · KERAGAMAN", "Tidak semua kecamatan sama", "Kepadatan, pendidikan, kesehatan, dan aktivitas usaha membentuk kombinasi yang berbeda.")
    with b: card("02 · POLA", "Tiga kelompok utama", "Pengelompokan membantu membaca kecamatan dengan karakteristik yang relatif serupa.")
    with c: card("03 · WILAYAH", "Rata-rata bukan seluruh cerita", "Perbandingan wilayah perlu dilengkapi dengan kondisi setiap kecamatan.")

# ----------------------------- PAGE 2 -----------------------------
elif current == "Apa yang Kita Ukur?":
    heading("02 · MENGENAL DATA", "Apa yang Kita Ukur?", "Enam indikator digunakan untuk membentuk gambaran karakteristik kecamatan. Dua indikator tambahan membantu memperkaya interpretasi.")
    st.markdown("#### Enam indikator pembentuk cluster")
    indicators = [
        ("Kepadatan penduduk", "Menggambarkan tingkat kepadatan dan tekanan ruang suatu kecamatan."),
        ("Pendidikan tinggi", "Persentase penduduk dengan pendidikan tinggi."),
        ("Rasio murid:guru", "Gambaran jumlah murid dibandingkan dengan guru; rasio lebih kecil dapat menunjukkan ketersediaan guru relatif lebih baik."),
        ("Tenaga kesehatan", "Jumlah tenaga kesehatan per 10.000 penduduk."),
        ("Fasilitas kesehatan", "Jumlah fasilitas kesehatan per 10.000 penduduk."),
        ("Kepadatan usaha", "Jumlah usaha per 10.000 penduduk sebagai proksi aktivitas usaha.")]
    cols = st.columns(3)
    for i,(t,d) in enumerate(indicators):
        with cols[i%3]: card(f"INDIKATOR {i+1:02d}",t,d)
    st.markdown("#### Variabel pendukung")
    st.info("Persentase penduduk usia produktif dan persentase penduduk miskin digunakan untuk memperkaya profil dan interpretasi, bukan sebagai fitur pembentuk cluster.")
    st.markdown("### Jelajahi indikator")
    variable = st.selectbox("Pilih indikator", NUMERIC, format_func=lambda x: DISPLAY[x])
    sort_order = st.radio("Urutan peringkat", ["Tertinggi", "Terendah"], horizontal=True)
    view = df[["Kecamatan","Wilayah",variable]].sort_values(variable, ascending=(sort_order=="Terendah"))
    top = view.head(10)
    fig = px.bar(top, x=variable, y="Kecamatan", orientation="h", color_discrete_sequence=[NAVY], title=f"10 kecamatan — {DISPLAY[variable]} ({sort_order.lower()})")
    fig.update_layout(yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(chart_layout(fig,420), use_container_width=True)
    st.dataframe(view.reset_index(drop=True).rename(columns={variable:DISPLAY[variable]}), use_container_width=True, hide_index=True)
    st.caption("Sumber: dataset analisis 31 kecamatan yang digunakan dalam proyek. Satuan mengikuti definisi setiap indikator.")

# ----------------------------- PAGE 3 -----------------------------
elif current == "Tidak Ada yang Seragam":
    heading("03 · EKSPLORASI", "Tidak Ada yang Seragam", "Satu indikator yang tinggi tidak otomatis berarti indikator lain juga tinggi. Karena itu, kita membaca beberapa sisi kota secara bersamaan.")
    st.markdown("### Satu kota, kondisi yang beragam")
    photo_a, photo_b = st.columns(2)
    with photo_a:
        image("permukiman_padat.png", caption="Ilustrasi kawasan permukiman padat.")
    with photo_b:
        image("surabaya_skyline_day.png", caption="Ilustrasi kawasan perkotaan Surabaya.")
    st.markdown("### Bandingkan sebaran indikator")
    v = st.selectbox("Pilih indikator untuk melihat distribusinya", NUMERIC, format_func=lambda x: DISPLAY[x])
    c1,c2 = st.columns([1.1,1])
    with c1:
        fig = px.histogram(df, x=v, nbins=12, color_discrete_sequence=[NAVY], title=f"Sebaran {DISPLAY[v]}")
        st.plotly_chart(chart_layout(fig,340), use_container_width=True)
    with c2:
        fig = px.box(df, y=v, points="all", color_discrete_sequence=[BURGUNDY], title=f"Rentang dan pencilan — {DISPLAY[v]}")
        fig.update_traces(jitter=.28)
        st.plotly_chart(chart_layout(fig,340), use_container_width=True)
    st.markdown("### Lihat perbedaan antarwilayah")
    region_var = st.selectbox("Pilih indikator perbandingan", NUMERIC, index=2, format_func=lambda x: DISPLAY[x], key="region_var")
    fig = px.box(df, x="Wilayah", y=region_var, color="Wilayah", category_orders={"Wilayah":REGIONS}, title=f"Perbandingan {DISPLAY[region_var]} pada lima wilayah")
    fig.update_layout(showlegend=False)
    st.plotly_chart(chart_layout(fig,380), use_container_width=True)
    st.markdown("**Apa yang perlu diperhatikan?**")
    st.write("Kepadatan penduduk menggambarkan konteks tekanan ruang, bukan otomatis kondisi baik atau buruk. Demikian pula, jumlah tenaga dan fasilitas kesehatan berdasarkan lokasi kecamatan belum tentu sama dengan akses layanan seluruh warga karena masyarakat dapat menggunakan layanan lintas kecamatan.")

# ----------------------------- PAGE 4 -----------------------------
elif current == "Apa Hubungan Antarindikator?":
    heading("04 · ANALISIS STATISTIK", "Apa Hubungan Antarindikator?", "Kita melihat apakah dua indikator bergerak searah, berlawanan arah, atau tidak menunjukkan hubungan yang jelas.")
    xvar = st.selectbox("Indikator pertama", NUMERIC, index=4, format_func=lambda x: DISPLAY[x], key="corr_x")
    yvar = st.selectbox("Indikator kedua", NUMERIC, index=5, format_func=lambda x: DISPLAY[x], key="corr_y")
    if xvar == yvar:
        st.warning("Pilih dua indikator yang berbeda.")
    else:
        rho,pv = spearmanr(df[xvar],df[yvar])
        c1,c2 = st.columns(2)
        c1.metric("Korelasi Spearman (ρ)", f"{rho:.3f}")
        c2.metric("P-value", f"{pv:.4f}")
        fig = px.scatter(df,x=xvar,y=yvar,hover_name="Kecamatan",color="Wilayah",category_orders={"Wilayah":REGIONS},title=f"{DISPLAY[xvar]} dan {DISPLAY[yvar]}")
        st.plotly_chart(chart_layout(fig,430), use_container_width=True)
        direction = "positif" if rho>0 else "negatif" if rho<0 else "mendekati nol"
        st.info(f"Pada 31 kecamatan, hubungan yang terukur bersifat **{direction}** dengan ρ = {rho:.3f}. Korelasi menggambarkan keterkaitan peringkat, bukan hubungan sebab-akibat.")
    st.markdown("### Temuan hubungan yang menonjol")
    findings = [
        ("Fasilitas kesehatan ↔ kepadatan usaha", "ρ = 0,888; p-Holm < 0,001", "Hubungan positif sangat kuat pada data ini."),
        ("Tenaga kesehatan ↔ fasilitas kesehatan", "ρ = 0,723; p-Holm = 0,0001", "Hubungan positif kuat."),
        ("Kepadatan penduduk ↔ persentase penduduk miskin", "ρ = 0,623; p-Holm = 0,0043", "Hubungan positif kuat."),
        ("Pendidikan tinggi ↔ fasilitas kesehatan", "ρ = 0,664; p-Holm = 0,0012", "Hubungan positif kuat.")]
    for title,stat,desc in findings:
        card("SPEARMAN", title, f"{stat}. {desc}")
    with st.expander("Detail metode dan hasil uji statistik"):
        st.markdown("**Shapiro–Wilk.** Digunakan sebagai diagnostik distribusi. Pada hasil analisis, kepadatan penduduk (p=0,0074), tenaga kesehatan (p=0,0046), fasilitas kesehatan (p=0,0059), dan persentase penduduk miskin (p=0,0236) menunjukkan bukti penyimpangan dari normalitas pada taraf 5%.")
        st.markdown("**Kruskal–Wallis antarwilayah.** Setelah koreksi Holm, perbedaan yang signifikan ditemukan pada pendidikan tinggi (p-Holm=0,0048) dan kepadatan penduduk (p-Holm=0,0343).")
        st.markdown("**Dunn–Holm.** Pasangan signifikan: kepadatan penduduk Barat–Pusat (p-Holm=0,0041); pendidikan tinggi Timur–Utara (p-Holm=0,0021); pendidikan tinggi Selatan–Utara (p-Holm=0,0142).")
        st.caption("Hasil ini berasal dari notebook Statistika Nonparametrik yang disertakan sebagai dasar proyek. Perbedaan signifikan tidak menunjukkan sebab-akibat.")

# ----------------------------- PAGE 5 -----------------------------
elif current == "Tiga Kelompok Kecamatan":
    heading("05 · PENGENALAN POLA", "Tiga Kelompok Kecamatan", "PCA membantu merangkum variasi indikator, kemudian Gaussian Mixture Model (GMM) mengelompokkan kecamatan dengan karakteristik yang relatif serupa.")
    cluster_info = {
        1: ("Relatif lebih baik pada sejumlah indikator", "Pendidikan tinggi, tenaga dan fasilitas kesehatan, serta kepadatan usaha memiliki nilai median relatif lebih tinggi dibanding kelompok lain."),
        2: ("Kepadatan dan kemiskinan relatif tinggi", "Memiliki median kepadatan penduduk dan persentase penduduk miskin tertinggi di antara tiga kelompok."),
        3: ("Indikator layanan dan usaha relatif rendah", "Pendidikan tinggi, tenaga kesehatan, fasilitas kesehatan, dan kepadatan usaha memiliki median relatif lebih rendah.")}
    photo_cols = st.columns(3)
    cluster_photos = [
        (1, "surabaya_skyline_sunset.png", "Ilustrasi suasana kawasan perkotaan"),
        (2, "permukiman_padat.png", "Ilustrasi kawasan permukiman"),
        (3, "surabaya_landmark_suro_boyo.png", "Landmark Kota Surabaya")]
    for col, (num, fname, cap) in zip(photo_cols, cluster_photos):
        with col:
            image(fname, width=220, caption=cap)
            st.caption(f"Cluster {num} · visual pendukung")
    st.caption("Foto hanya ilustrasi suasana kota dan bukan bukti atau representasi langsung seluruh kecamatan dalam cluster.")
    selected = st.radio("Pilih cluster untuk dijelajahi", [1,2,3], horizontal=True, format_func=lambda x:f"Cluster {x}")
    group = df[df["Cluster_Tampilan"]==selected].copy()
    title,desc = cluster_info[selected]
    c1,c2 = st.columns([1,1.4])
    with c1:
        st.metric("Jumlah anggota", f"{len(group)} kecamatan")
        card(f"CLUSTER {selected}", title, desc)
    with c2:
        st.markdown("#### Anggota cluster")
        st.write(", ".join(group["Kecamatan"].tolist()))
        st.markdown("#### Profil median indikator")
        prof_vars = ["Persentase pendidikan tinggi","Tenaga kesehatan per 10.000 penduduk","Fasilitas kesehatan per 10.000 penduduk","Kepadatan Usaha per 10.000 penduduk"]
        prof = group[prof_vars].median().reset_index(); prof.columns=["Indikator","Median"]
        prof["Indikator"] = prof["Indikator"].map(DISPLAY)
        fig = px.bar(prof,x="Median",y="Indikator",orientation="h",color_discrete_sequence=[CLUSTER_COLORS[selected]],title="Median indikator utama (satuan asli berbeda)")
        st.plotly_chart(chart_layout(fig,330),use_container_width=True)
    with st.expander("Lihat 9 subcluster sebagai pendalaman eksploratif"):
        sub = df[df["Cluster_Tampilan"]==selected]
        for subname, sg in sub.groupby("Subcluster_Tampilan", sort=True):
            st.markdown(f"**{subname} · {len(sg)} kecamatan** — {', '.join(sg['Kecamatan'].tolist())}")
        st.warning("Subcluster beranggota satu atau dua kecamatan bersifat eksploratif. Jangan menafsirkannya sebagai kelompok yang stabil atau representatif.")
    st.markdown("### Bagaimana kualitas pengelompokan? ")
    m1,m2,m3 = st.columns(3)
    m1.metric("Silhouette GMM", "0,290")
    m2.metric("ARI GMM vs Ward", "0,429")
    m3.metric("Rata-rata ARI resampling", "0,529")
    st.write("Indikator evaluasi menunjukkan pemisahan dan stabilitas yang masih sedang. BIC memilih dua komponen sebagai kandidat terbaik pada rentang model yang diuji. Tiga cluster tetap digunakan sebagai rancangan segmentasi utama agar profil lebih mudah dibahas, bukan diklaim sebagai optimum BIC.")
    with st.expander("Catatan metodologi clustering"):
        st.write("Nomor cluster pada dashboard ditata ulang untuk mengikuti urutan profil yang dipakai dalam cerita: Cluster 1 (16 anggota), Cluster 2 (6 anggota), dan Cluster 3 (9 anggota). Nomor ini adalah label tampilan, bukan peringkat resmi. Wilayah administratif tidak digunakan sebagai fitur pembentuk cluster.")
        st.write("BIC terendah pada kandidat yang diuji adalah k=2. ARI GMM vs Ward sebesar 0,429 menunjukkan kesesuaian dua metode, bukan akurasi klasifikasi. Rata-rata ARI resampling sekitar 0,529.")

# ----------------------------- PAGE 6 -----------------------------
elif current == "Di Mana Mereka Berada?":
    heading("06 · PERSEBARAN GEOGRAFIS", "Di Mana Mereka Berada?", "Cluster tidak selalu mengikuti batas wilayah administratif. Kecamatan yang berdekatan secara geografis belum tentu memiliki karakteristik yang sama.")
    cross = pd.crosstab(df["Wilayah"],df["Cluster_Tampilan"]).reindex(REGIONS).fillna(0).astype(int)
    cross.columns=[f"Cluster {int(c)}" for c in cross.columns]
    fig = px.bar(cross.reset_index().melt(id_vars="Wilayah",var_name="Cluster",value_name="Jumlah kecamatan"),x="Wilayah",y="Jumlah kecamatan",color="Cluster",barmode="stack",category_orders={"Wilayah":REGIONS,"Cluster":["Cluster 1","Cluster 2","Cluster 3"]},color_discrete_map={"Cluster 1":CLUSTER_COLORS[1],"Cluster 2":CLUSTER_COLORS[2],"Cluster 3":CLUSTER_COLORS[3]},title="Jumlah kecamatan pada setiap wilayah")
    st.plotly_chart(chart_layout(fig,390),use_container_width=True)
    region = st.selectbox("Pilih wilayah untuk melihat kecamatannya", REGIONS)
    rdata = df[df["Wilayah"]==region].sort_values("Cluster_Tampilan")
    st.markdown(f"### Kecamatan di wilayah {region}")
    for cl in [1,2,3]:
        names = rdata.loc[rdata["Cluster_Tampilan"]==cl,"Kecamatan"].tolist()
        if names:
            st.markdown(f"**Cluster {cl} ({len(names)}):** {', '.join(names)}")
    st.markdown("### Peta referensi Surabaya")
    image("peta_referensi_surabaya.png", width=760, caption="Peta referensi wilayah Surabaya yang diberikan untuk rancangan dashboard. Peta ini bersifat ilustratif dan belum menjadi peta tematik interaktif per batas kecamatan.")
    st.info("Peta klik-per-kecamatan membutuhkan file batas administrasi GeoJSON/shapefile yang tervalidasi. File batas tersebut belum tersedia dalam paket ini, sehingga dashboard tidak menggambar batas atau koordinat kecamatan secara perkiraan.")
    st.dataframe(cross, use_container_width=True)

# ----------------------------- PAGE 7 -----------------------------
elif current == "Siapa yang Perlu Perhatian?":
    heading("07 · MEMBACA KESENJANGAN", "Siapa yang Perlu Perhatian?", "Indeks berikut menunjukkan posisi relatif lima wilayah terhadap rata-rata 31 kecamatan. Nilai positif berarti relatif di atas rata-rata; nilai negatif berarti relatif di bawah rata-rata.")
    # Gunakan nilai indeks wilayah yang telah dihitung dan disimpan dalam hasil analisis.
    index_values = pd.DataFrame({
        "Wilayah": ["Barat","Pusat","Selatan","Timur","Utara"],
        "Pendidikan": [-0.215,-0.356,0.479,0.584,-0.999],
        "Kesehatan": [-0.459,0.135,0.359,0.457,-0.680],
        "Ekonomi": [-0.076,0.253,0.145,0.412,-0.905]})
    dimension = st.radio("Pilih bidang", ["Pendidikan","Kesehatan","Ekonomi"], horizontal=True)
    sorted_idx = index_values.sort_values(dimension, ascending=True)
    fig = px.bar(sorted_idx,x=dimension,y="Wilayah",orientation="h",color=dimension,color_continuous_scale=[[0,"#5C1F2E"],[.5,"#EDE3C8"],[1,"#1B2A3D"]],title=f"Indeks relatif bidang {dimension.lower()} per wilayah")
    fig.add_vline(x=0,line_dash="dash",line_color="#000000")
    st.plotly_chart(chart_layout(fig,360),use_container_width=True)
    st.markdown("### Ringkasan lima wilayah")
    summaries = {
        "Timur":"Relatif unggul pada pendidikan, kesehatan, dan ekonomi dibanding rata-rata 31 kecamatan.",
        "Selatan":"Relatif baik pada pendidikan dan kesehatan; ekonomi juga sedikit di atas rata-rata.",
        "Pusat":"Kesehatan dan ekonomi berada di atas rata-rata, sedangkan pendidikan di bawah rata-rata.",
        "Barat":"Pendidikan dan ekonomi mendekati rata-rata; kesehatan berada di bawah rata-rata.",
        "Utara":"Memiliki indeks relatif terendah pada ketiga bidang dan perlu dikaji lebih lanjut."}
    for r in REGIONS:
        card("WILAYAH", r, summaries[r])
    st.warning("Indeks ini bersifat deskriptif, berbasis z-score dengan bobot kecamatan sama. Bukan indeks resmi BPS atau ukuran kesejahteraan penduduk. Rata-rata wilayah juga dapat menyembunyikan perbedaan antarkecamatan.")
    if PRIORITY_FILE.exists():
        with st.expander("Lihat kecamatan dengan skor relatif terendah per bidang"):
            pri = pd.read_csv(PRIORITY_FILE)
            field = st.selectbox("Bidang prioritas", pri["Bidang"].dropna().unique().tolist())
            st.dataframe(pri[pri["Bidang"]==field].head(8),use_container_width=True,hide_index=True)

# ----------------------------- PAGE 8 -----------------------------
elif current == "Penutup: Dari Data ke Arah Perhatian":
    heading("08 · DARI DATA KE ARAH PERHATIAN", "Penutup: Dari Data ke Arah Perhatian", "Pemerataan membutuhkan pandangan sampai tingkat kecamatan. Rata-rata kota penting, tetapi tidak cukup untuk menceritakan seluruh kondisi.")
    left,right=st.columns([1.1,1])
    with left:
        card("PENDIDIKAN", "Lihat kebutuhan pendidikan", "Cermati kecamatan dengan persentase pendidikan tinggi relatif rendah dan rasio murid:guru yang perlu ditinjau lebih lanjut.")
        st.write("")
        card("KESEHATAN", "Tinjau pemerataan layanan", "Evaluasi persebaran tenaga dan fasilitas kesehatan. Perhatikan bahwa layanan dapat digunakan warga lintas kecamatan.")
        st.write("")
        card("EKONOMI", "Pahami aktivitas usaha", "Kaji kecamatan dengan kepadatan usaha relatif rendah dan lengkapi dengan indikator ekonomi lainnya.")
    with right:
        image("surabaya_skyline_sunset.png", caption="Surabaya — sebuah kota dengan banyak cerita yang layak dibaca.")
        st.markdown("### Cari kecamatanmu")
        chosen = st.selectbox("Pilih kecamatan", sorted(df["Kecamatan"].unique()))
        row = df[df["Kecamatan"]==chosen].iloc[0]
        st.markdown(f"**Wilayah:** {row['Wilayah']}  \n**Cluster:** {int(row['Cluster_Tampilan'])}  \n**Subcluster:** {row['Subcluster_Tampilan']}")
        st.write("Lihat profil indikator kecamatan ini pada bagian Apa yang Kita Ukur? dan Tiga Kelompok Kecamatan.")
    st.markdown(f'''<div class="hero"><h1 style="font-size:2.25rem !important">Surabaya bukan satu cerita.</h1><p>Ada 31 cerita yang layak didengar.</p><span class="pill">DARI DATA MENJADI PEMAHAMAN</span></div>''',unsafe_allow_html=True)
    st.caption("Hasil analisis merupakan bahan awal untuk memahami variasi karakteristik kecamatan. Rekomendasi bukan keputusan kebijakan; penentuan program memerlukan data tambahan dan kajian lapangan.")

st.markdown("---")
st.markdown('<div class="small-note">SATU KOTA, 31 CERITA · Dashboard eksplorasi data kecamatan Kota Surabaya. Sumber data dan keterbatasan interpretasi dijelaskan pada setiap bagian.</div>',unsafe_allow_html=True)
