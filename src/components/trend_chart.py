# -*- coding: utf-8 -*-
"""
趋势折线图：双 Y 轴 —— 左轴新增确诊，右轴累计确诊；
可选对比某一区 vs 全港。
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from src.config import ACCENT_CYAN, ACCENT_PURPLE, PAPER_BG, PLOT_BG, TEXT_PRIMARY
from src.utils import aggregate_by_date


def build_trend_figure(df_all: pd.DataFrame, selected_district: str | None) -> go.Figure:
    """
    df_all：完整明细（不仅限于当前筛选区间），用于画出完整趋势线再由上层切片；
    上层传入的 df_all 应为日期范围内的明细。
    """
    hk = aggregate_by_date(df_all)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=hk["日期"],
            y=hk["新增确诊"],
            name="全港-新增",
            mode="lines+markers",
            line=dict(color=ACCENT_CYAN, width=2),
            marker=dict(size=6),
            hovertemplate="全港 新增: %{y}<br>%{x|%Y-%m-%d}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=hk["日期"],
            y=hk["累计确诊"],
            name="全港-累计",
            mode="lines",
            line=dict(color=ACCENT_PURPLE, width=2, dash="dot"),
            hovertemplate="全港 累计: %{y}<br>%{x|%Y-%m-%d}<extra></extra>",
        ),
        secondary_y=True,
    )

    if selected_district:
        sub = df_all[df_all["地区"] == selected_district].sort_values("日期")
        if not sub.empty:
            fig.add_trace(
                go.Scatter(
                    x=sub["日期"],
                    y=sub["新增确诊"],
                    name=f"{selected_district}-新增",
                    mode="lines+markers",
                    line=dict(color="#f472b6", width=2),
                    marker=dict(size=5),
                    hovertemplate=f"{selected_district} 新增: %{{y}}<br>%{{x|%Y-%m-%d}}<extra></extra>",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=sub["日期"],
                    y=sub["累计确诊"],
                    name=f"{selected_district}-累计",
                    mode="lines",
                    line=dict(color="#fbbf24", width=2, dash="dash"),
                    hovertemplate=f"{selected_district} 累计: %{{y}}<br>%{{x|%Y-%m-%d}}<extra></extra>",
                ),
                secondary_y=True,
            )

    fig.update_xaxes(showgrid=False, gridcolor="rgba(255,255,255,0.08)", zeroline=False)
    fig.update_yaxes(
        title_text="新增确诊",
        secondary_y=False,
        gridcolor="rgba(255,255,255,0.08)",
        color=ACCENT_CYAN,
    )
    fig.update_yaxes(
        title_text="累计确诊",
        secondary_y=True,
        gridcolor="rgba(255,255,255,0.05)",
        color=ACCENT_PURPLE,
    )

    title = "疫情趋势（双轴）"
    if selected_district:
        title += f" — 对比：{selected_district} vs 全港"

    fig.update_layout(
        title=dict(text=title, font=dict(color=TEXT_PRIMARY, size=16)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=TEXT_PRIMARY)),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        margin=dict(l=10, r=10, t=60, b=10),
        hovermode="x unified",
        font=dict(color=TEXT_PRIMARY),
    )
    return fig


def render_trend_chart(df_range: pd.DataFrame, selected_district: str | None) -> None:
    """渲染趋势图（df_range 为当前日期筛选后的明细）。"""
    fig = build_trend_figure(df_range, selected_district)
    st.plotly_chart(fig, use_container_width=True, key="trend_chart")
