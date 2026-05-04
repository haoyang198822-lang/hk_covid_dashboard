# -*- coding: utf-8 -*-
"""
风险等级饼图：取各区在区间结束日的风险等级分布。
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config import PAPER_BG, PLOT_BG, RISK_COLORS, TEXT_PRIMARY


def render_risk_pie(df_range: pd.DataFrame) -> None:
    if df_range.empty:
        st.info("当前日期范围内无数据。")
        return

    end_date = df_range["日期"].max()
    if pd.isna(end_date):
        st.info("无法确定期末日期。")
        return
    last_day = df_range[df_range["日期"] == end_date]
    last_row_per_dist = last_day.sort_values("日期").groupby("地区").tail(1)
    counts = last_row_per_dist["风险等级"].value_counts().reset_index()
    counts.columns = ["风险等级", "区数"]

    colors = [RISK_COLORS.get(str(r), RISK_COLORS["未知"]) for r in counts["风险等级"]]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts["风险等级"],
                values=counts["区数"],
                hole=0.42,
                marker=dict(colors=colors, line=dict(color="rgba(255,255,255,0.25)", width=1)),
                textinfo="percent+label",
                hovertemplate="%{label}<br>区数: %{value}<br>占比: %{percent}<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title=dict(text=f"风险等级分布（期末日 {end_date.date()}）", font=dict(color=TEXT_PRIMARY, size=14)),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT_PRIMARY),
        margin=dict(l=10, r=10, t=50, b=10),
        showlegend=True,
        legend=dict(font=dict(color=TEXT_PRIMARY)),
    )
    st.plotly_chart(fig, use_container_width=True, key="risk_pie")
