import streamlit as st
import os, json

st.set_page_config(
    page_title="Informatika Lab | InfoSchoolUz",
    page_icon="🖥️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #f8fafc !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"] { display: none; }

.header-block {
    background: #ffffff;
    border-bottom: 2px solid #e2e8f0;
    padding: 32px 0 24px;
    text-align: center;
    margin-bottom: 36px;
}
.header-block h1 {
    font-size: 2rem;
    font-weight: 800;
    color: #1e293b;
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.header-block p {
    color: #64748b;
    font-size: 0.95rem;
    margin: 0;
}
.header-logo {
    font-size: 2.5rem;
    margin-bottom: 8px;
}

.card {
    background: #ffffff;
    border: 1.5px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px 20px 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
    height: 100%;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.card:hover {
    border-color: var(--card-color);
    box-shadow: 0 6px 24px rgba(0,0,0,0.10);
    transform: translateY(-3px);
}
.card-icon  { font-size: 2.8rem; margin-bottom: 12px; }
.card-title { font-size: 1rem; font-weight: 700; color: #1e293b; margin-bottom: 6px; }
.card-desc  { font-size: 0.82rem; color: #64748b; line-height: 1.5; margin-bottom: 12px; }
.card-badge {
    display: inline-block;
    background: var(--card-color-light);
    color: var(--card-color);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-weight: 600;
}
.empty-state {
    text-align: center;
    padding: 80px 20px;
    color: #94a3b8;
}
.empty-state h3 { font-size: 1.2rem; margin-bottom: 8px; color: #64748b; }
.back-btn { margin-bottom: 16px; }
.korgazma-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 20px;
}
.count-badge {
    background: #f1f5f9;
    color: #475569;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────
if "selected" not in st.session_state:
    st.session_state.selected = None

# ── Ko'rgazmalarni o'qish ──────────────────────────────────────────────────
def get_korgazmalar():
    folder = "korgazmalar"
    items = []
    if not os.path.exists(folder):
        return items
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if not os.path.isdir(path):
            continue
        meta_path = os.path.join(path, "meta.json")
        html_path = os.path.join(path, "index.html")
        if os.path.exists(meta_path) and os.path.exists(html_path):
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            meta["folder"]    = name
            meta["html_path"] = html_path
            items.append(meta)
    return items

# ── Ko'rgazma ochilgan holat ───────────────────────────────────────────────
if st.session_state.selected:
    sel = st.session_state.selected

    col_back, col_title = st.columns([1, 9])
    with col_back:
        if st.button("← Orqaga", key="back"):
            st.session_state.selected = None
            st.rerun()
    with col_title:
        st.markdown(f'<div class="korgazma-title">{sel["icon"]} {sel["title"]}</div>',
                    unsafe_allow_html=True)

    with open(sel["html_path"], encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=900, scrolling=True)

# ── Dashboard ──────────────────────────────────────────────────────────────
else:
    items = get_korgazmalar()

    # Header
    count_text = f"{len(items)} ta ko'rgazma" if items else ""
    st.markdown(f"""
    <div class="header-block">
        <div class="header-logo">🖥️</div>
        <h1>Informatika fanidan vizual ko'rgazmalar</h1>
        <p>InfoSchoolUz · Urgench · Khorezm</p>
        {"<span class='count-badge'>📚 " + count_text + "</span>" if count_text else ""}
    </div>
    """, unsafe_allow_html=True)

    if not items:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:3rem">📂</div>
            <h3>Hozircha ko'rgazmalar yo'q</h3>
            <p><code>korgazmalar/</code> papkasiga yangi ko'rgazma qo'shing<br>
            va sahifa avtomatik yangilanadi</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(3, gap="large")
        for i, item in enumerate(items):
            color      = item.get("color", "#3b82f6")
            color_light = color + "18"
            sinf       = item.get("sinf", "")

            with cols[i % 3]:
                st.markdown(f"""
                <div class="card" style="--card-color:{color}; --card-color-light:{color_light}">
                    <div class="card-icon">{item["icon"]}</div>
                    <div class="card-title">{item["title"]}</div>
                    <div class="card-desc">{item.get("description", "")}</div>
                    {"<span class='card-badge'>" + sinf + "</span>" if sinf else ""}
                </div>
                """, unsafe_allow_html=True)

                if st.button("▶ Ochish", key=item["folder"], use_container_width=True):
                    st.session_state.selected = item
                    st.rerun()
