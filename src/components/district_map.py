# -*- coding: utf-8 -*-
"""
区级交互地图：基于 Plotly Scattermap（OpenStreetMap，无需 Token）。
GeoJSON 占位文件存在时，可在后续接入 Polygon（需 Mapbox / MapLibre 等底图方案）。
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config import ACCENT_CYAN, CHART_PALETTE, TEXT_PRIMARY

# 香港 18 区近似中心（与 Excel 「地区」列名称对齐）
DISTRICT_CENTROIDS: dict[str, tuple[float, float]] = {
    "中西区": (22.286, 114.154),
    "湾仔": (22.279, 114.172),
    "东区": (22.284, 114.226),
    "南区": (22.247, 114.156),
    "油尖旺": (22.311, 114.171),
    "深水埗": (22.331, 114.162),
    "九龙城": (22.328, 114.191),
    "黄大仙": (22.342, 114.193),
    "观塘": (22.311, 114.226),
    "荃湾": (22.371, 114.115),
    "屯门": (22.391, 113.977),
    "元朗": (22.445, 114.022),
    "北区": (22.494, 114.139),
    "大埔": (22.451, 114.165),
    "沙田": (22.387, 114.195),
    "西贡": (22.381, 114.273),
    "葵青": (22.357, 114.129),
    "离岛": (22.286, 113.942),
}


def build_map_figure(
    df_snapshot: pd.DataFrame,
    *,
    color_col: str = "新增确诊",
    size_col: str = "现存确诊",
) -> go.Figure:
    """
    df_snapshot：每个区一行（已按选定日期聚合），需含「地区」及指标列。
    """
    if df_snapshot.empty:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=30, b=0),
            annotations=[
                dict(
                    text="暂无数据",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(color=TEXT_PRIMARY, size=16),
                )
            ],
        )
        return fig

    df = df_snapshot.copy()
    df["lat"] = df["地区"].map(lambda x: DISTRICT_CENTROIDS.get(x, (None, None))[0])
    df["lon"] = df["地区"].map(lambda x: DISTRICT_CENTROIDS.get(x, (None, None))[1])

    missing = df["lat"].isna()
    if missing.any():
        # 未知区名：放在港岛附近偏移，避免静默丢失
        df.loc[missing, "lat"] = 22.32
        df.loc[missing, "lon"] = 114.17

    sizes = df[size_col].astype(float).clip(lower=1)
    max_s = float(sizes.max()) or 1.0
    marker_size = 12 + 28 * (sizes / max_s)

    fig = go.Figure(
        go.Scattermap(
            lat=df["lat"],
            lon=df["lon"],
            mode="markers",
            marker=dict(
                size=marker_size,
                color=df[color_col],
                colorscale=[[0, CHART_PALETTE[1]], [0.5, ACCENT_CYAN], [1, CHART_PALETTE[2]]],
                showscale=True,
                colorbar=dict(
                    title=dict(text=color_col, font=dict(color=TEXT_PRIMARY)),
                    tickfont=dict(color=TEXT_PRIMARY),
                ),
                # Plotly 6+ 的 Scattermap.marker 不支持 outline「line」，去掉以避免报错
                opacity=0.92,
            ),
            text=df["地区"],
            customdata=df[["地区", color_col, size_col]].values,
            hovertemplate=(
                "<b>%{text}</b><br>"
                f"{color_col}: %{{customdata[1]}}<br>"
                f"{size_col}: %{{customdata[2]}}<br>"
                "<extra></extra>"
            ),
            selected=dict(marker=dict(opacity=0.98)),
            unselected=dict(marker=dict(opacity=0.55)),
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        dragmode="lasso",
        map=dict(
            style="open-street-map",
            center=dict(lat=22.35, lon=114.18),
            zoom=10.2,
            bearing=0,
            pitch=0,
        ),
        font=dict(color=TEXT_PRIMARY),
        uirevision="district-map",
    )
    return fig


def render_district_map(df_snapshot: pd.DataFrame, *, map_key: str = "hk_covid_map") -> None:
    """渲染地图并根据 Streamlit 选中事件更新 session_state['selected_district']。"""
    fig = build_map_figure(df_snapshot)
    st.plotly_chart(fig, use_container_width=True, key=map_key, on_select="rerun")

    state = st.session_state.get(map_key)
    district: Optional[str] = None

    if state is not None:
        points = None
        if isinstance(state, dict):
            points = state.get("points") or state.get("selection", {}).get("points")
        else:
            points = getattr(state, "points", None)

        if points:
            first = points[0]
            if isinstance(first, dict):
                custom = first.get("customdata")
                if custom is not None and len(custom) >= 1:
                    district = str(custom[0])
                elif first.get("text") is not None:
                    district = str(first["text"])
            else:
                custom = getattr(first, "customdata", None)
                if custom is not None and len(custom) >= 1:
                    district = str(custom[0])
                elif getattr(first, "text", None):
                    district = str(first.text)

    if district:
        st.session_state["selected_district"] = district
