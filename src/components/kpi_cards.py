# -*- coding: utf-8 -*-
"""
KPI 卡片：新增确诊、累计确诊、现存确诊、覆盖区数。
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.components.glass_card import glass_open, glass_close


def _fmt_int(n: float) -> str:
    try:
        return f"{int(round(n)):,}"
    except Exception:
        return str(n)


def render_kpi_row(df_range: pd.DataFrame) -> None:
    """
    根据当前日期筛选后的明细 df_range 计算 KPI。
    df_range 须包含列：日期、地区、新增确诊、累计确诊、现存确诊
    """
    if df_range.empty:
        new_sum = cum_max = active_sum = districts_n = 0
    else:
        new_sum = float(df_range["新增确诊"].sum())
        # 累计：取筛选区间内每个区最后一天记录的累计最大值之和（近似「时点存量合计」）
        last_per_dist = df_range.sort_values("日期").groupby("地区").tail(1)
        cum_max = float(last_per_dist["累计确诊"].sum())
        active_sum = float(last_per_dist["现存确诊"].sum())
        districts_n = int(df_range["地区"].nunique())

    fragments = [
        f'<div><div class="glass-kpi-label">新增确诊（区间内）</div>'
        f'<div class="glass-kpi-value">{_fmt_int(new_sum)}</div></div>',
        f'<div><div class="glass-kpi-label">累计确诊（期末汇总）</div>'
        f'<div class="glass-kpi-value">{_fmt_int(cum_max)}</div></div>',
        f'<div><div class="glass-kpi-label">现存确诊（期末汇总）</div>'
        f'<div class="glass-kpi-value">{_fmt_int(active_sum)}</div></div>',
        f'<div><div class="glass-kpi-label">覆盖区数</div>'
        f'<div class="glass-kpi-value">{districts_n}</div></div>',
    ]

    glass_open()
    cols = st.columns(4)
    for col, frag in zip(cols, fragments):
        with col:
            st.markdown(frag, unsafe_allow_html=True)
    glass_close()
