import streamlit as st

PAGE_SYMBOLS = {
    "Home Credit Risk Overview": "🏠",
    "Executive Overview": "📊",
    "Sales Analysis": "💰",
    "Profit Analysis": "📈",
    "Regional Analysis": "🌍",
    "State Analysis": "🗺️",
    "City Analysis": "🏙️",
    "Category Analysis": "🧩",
    "SubCategory Analysis": "📦",
    "Product Analysis": "🛍️",
    "Customer Analysis": "👥",
    "Segment Analysis": "🎯",
    "Order Analysis": "🧾",
    "Shipping Analysis": "🚚",
    "Discount Analysis": "🏷️",
    "Loss Analysis": "⚠️",
    "Time Series": "⏱️",
    "Growth Analysis": "📉",
    "Sales vs Profit": "📊",
    "Top Bottom": "🏆",
    "Data Explorer": "🔎",
}


def render_page_header(title, symbol=None, subtitle="Risk Intelligence", kicker=None):
    page_symbol = symbol or PAGE_SYMBOLS.get(title, "🏠")
    st.markdown(
        f"""
        <div class="top-brand">
            <div class="brand-mark">{page_symbol}</div>
            <div class="brand-text">
                <div class="brand-name">HOME CREDIT</div>
                <div class="brand-sub">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if kicker:
        st.markdown(f'<div class="page-kicker">{kicker}</div>', unsafe_allow_html=True)


def apply_sky_theme():
    st.sidebar.markdown(
        """
        <div class="brand-lockup">
            <div class="brand-mark">HC</div>
            <div><strong>HOME</strong><br><strong>CREDIT</strong></div>
        </div>
        <div class="sidebar-rule"></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --canvas: #0b0b0c;
            --surface: #171718;
            --navy: #080809;
            --ink: #f4f0f7;
            --muted: #99929f;
            --mint: #9c6cff;
            --mint-strong: #b27dff;
            --coral: #ff9279;
            --line: #29272c;
        }

        .stApp {
            background: radial-gradient(circle at 78% 0%, #241638 0, transparent 32%), var(--canvas);
            color: var(--ink);
            font-family: 'DM Sans', sans-serif;
        }

        body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: var(--canvas);
        }

        [data-testid="stHeader"] {
            background: rgba(11, 11, 12, 0.94);
            border-bottom: 1px solid transparent;
        }

        .top-brand {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin: 0 0 1rem;
            padding: 0.15rem 0;
        }

        .brand-mark {
            display: grid;
            place-items: center;
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(135deg, #c9a7ff 0%, #8b5cf6 100%);
            color: #120f1b;
            font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            box-shadow: 0 10px 20px rgba(139, 92, 246, 0.35);
        }

        .brand-text {
            display: flex;
            flex-direction: column;
            gap: 0.08rem;
        }

        .brand-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.45rem;
            font-weight: 700;
            line-height: 1.1;
            color: var(--ink);
        }

        .brand-sub {
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #c19aff;
        }

        [data-testid="stSidebar"] {
            background: var(--navy);
            border-right: 0;
            min-width: 214px;
        }

        .brand-lockup {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin: 0.35rem 0 1.1rem;
            color: #ffffff;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.82rem;
            line-height: 1.05;
            letter-spacing: 0.04em;
        }

        .brand-lockup .brand-mark {
            display: grid;
            place-items: center;
            width: 30px;
            height: 30px;
            border: 1px solid rgba(188, 239, 227, 0.8);
            border-radius: 8px;
            color: var(--mint);
            font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif;
            font-size: 0.9rem;
        }

        .sidebar-rule {
            height: 1px;
            margin-bottom: 1rem;
            background: rgba(217, 231, 232, 0.18);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #d9d2df;
        }

        .block-container {
            max-width: 1500px;
            padding: 2.5rem 3rem 3rem;
        }

        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: 0;
            font-family: 'Space Grotesk', sans-serif;
        }

        h1 {
            font-weight: 700;
            font-size: 2.25rem;
            margin-bottom: 0.2rem;
        }

        .page-kicker {
            color: #c19aff;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }

        .chart-badge {
            display: inline-block;
            margin: 0.25rem 0 1rem;
            padding: 0.32rem 0.58rem;
            border: 1px solid #7653b5;
            border-radius: 999px;
            background: #24183a;
            color: #c19aff;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.08em;
        }

        h2, h3 {
            font-weight: 600;
        }

        [data-testid="stCaptionContainer"] {
            color: var(--muted);
        }

        [data-testid="stSidebar"] .stCaption {
            color: #aaa2b2;
        }

        [data-testid="stSidebar"] [data-testid="stMultiSelect"] label,
        [data-testid="stSidebar"] [data-testid="stTextInput"] label,
        [data-testid="stSidebar"] [data-testid="stSlider"] label {
            color: #d9d2df;
        }

        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 12px;
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.25);
            padding: 0.85rem 1rem;
            min-height: 96px;
        }

        [data-testid="stMetric"]:nth-child(odd) {
            border-top: 3px solid var(--mint-strong);
        }

        [data-testid="stMetric"]:nth-child(even) {
            border-top: 3px solid var(--coral);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: var(--ink);
            font-family: 'Space Grotesk', sans-serif;
        }

        [data-testid="stPlotlyChart"],
        [data-testid="stDataFrame"],
        [data-testid="stExpander"],
        [data-testid="stAlert"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 10px;
            box-shadow: 0 5px 18px rgba(0, 0, 0, 0.22);
            padding: 0.45rem;
        }

        div[data-testid="stPlotlyChart"] > div {
            min-height: 280px;
        }

        [data-testid="stExpander"] summary {
            color: var(--ink);
            font-weight: 600;
        }

        [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
            background: #202022;
            border-color: #3b3740;
            border-radius: 7px;
        }

        .stButton > button {
            background: var(--mint);
            border: 1px solid var(--mint);
            color: #130d1c;
            border-radius: 7px;
            font-weight: 700;
        }

        .stButton > button:hover {
            background: var(--mint-strong);
            border-color: var(--mint-strong);
            color: white;
        }

        [data-testid="stDownloadButton"] > button {
            border: 1px solid #7653b5;
            border-radius: 7px;
            color: #d4baff;
            font-weight: 600;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            text-align: left;
            background: transparent;
            border: 0;
            color: #d9e7e8;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
