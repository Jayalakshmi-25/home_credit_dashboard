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