# -*- coding: utf-8 -*-
"""
注入自定义 CSS：深色背景 + 毛玻璃卡片 + 弱化默认 Streamlit 边框。
"""

import streamlit as st

from src.config import (
    ACCENT_CYAN,
    BG_PAGE,
    GLASS_BLUR,
    GLASS_BORDER,
    GLASS_RADIUS,
    GLASS_SHADOW,
    TEXT_PRIMARY,
)


def inject_global_styles() -> None:
    """在页面首次渲染时注入全局样式。"""
    css = f"""
    <style>
    /* 页面底色 */
    .stApp {{
        background: linear-gradient(145deg, {BG_PAGE} 0%, #0f1628 45%, #0a1620 100%);
        color: {TEXT_PRIMARY};
    }}
    /* 主容器略微内边距 */
    .block-container {{
        padding-top: 1.25rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}
    /* 标题渐变 */
    .hk-dash-title {{
        font-weight: 700;
        letter-spacing: 0.02em;
        background: linear-gradient(90deg, {ACCENT_CYAN}, #c4b5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    /* 毛玻璃外壳：用于 markdown unsafe_allow_html 包裹 */
    .glass-panel {{
        background: rgba(255, 255, 255, 0.06);
        border: {GLASS_BORDER};
        border-radius: {GLASS_RADIUS};
        box-shadow: {GLASS_SHADOW};
        backdrop-filter: blur({GLASS_BLUR});
        -webkit-backdrop-filter: blur({GLASS_BLUR});
        padding: 0.4rem 0.8rem;
        margin-bottom: 0.75rem;
    }}
    .glass-panel-subtle {{
        background: rgba(255, 255, 255, 0.04);
        border: {GLASS_BORDER};
        border-radius: 6px;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        padding: 0.4rem 0.8rem;
    }}
    /* KPI 数字强调 */
    .glass-kpi-value {{
        font-size: 1.65rem;
        font-weight: 700;
        color: {ACCENT_CYAN};
        text-shadow: 0 0 24px rgba(62, 232, 255, 0.35);
    }}
    .glass-kpi-label {{
        font-size: 0.85rem;
        color: rgba(232, 238, 252, 0.72);
    }}
    /* 侧边栏与控件融合深色 */
    section[data-testid="stSidebar"] {{
        background: rgba(12, 18, 32, 0.85);
        backdrop-filter: blur(12px);
    }}
    /* 表格毛玻璃感 */
    div[data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        border: {GLASS_BORDER};
        box-shadow: {GLASS_SHADOW};
    }}
    /* Plotly 容器圆角 */
    .js-plotly-plot {{
        border-radius: 12px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
