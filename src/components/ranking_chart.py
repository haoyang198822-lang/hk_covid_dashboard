# -*- coding: utf-8 -*-
"""
Top10 排名条形图：区间内各地区新增确诊合计。
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import CHART_PALETTE, PAPER_BG, PLOT_BG, TEXT_PRIMARY


def render_ranking_chart(df_range: pd.DataFrame, *, top_n: int = 10) -> None:
    if df_range.empty:
        st.info("当前日期范围内无数据。")
        return

    g = (
        df_range.groupby("地区", as_index=False)["新增确诊"]
        .sum()
        .sort_values("新增确诊", ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        g,
        x="新增确诊",
        y="地区",
        orientation="h",
        color="地区",
        color_discrete_sequence=CHART_PALETTE,
        labels={"新增确诊": "新增合计", "地区": "地区"},
    )
    fig.update_layout(
        title=dict(text=f"新增确诊 Top {top_n}", font=dict(color=TEXT_PRIMARY, size=15)),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT_PRIMARY),
        margin=dict(l=10, r=10, t=50, b=10),
        showlegend=False,
        yaxis=dict(categoryorder="total ascending"),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
    )
    fig.update_traces(hovertemplate="%{y}<br>新增合计: %{x}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True, key="ranking_chart")
