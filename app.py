# -*- coding: utf-8 -*-
"""
香港疫情区级可视化 Dashboard — Streamlit 入口。
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.components.district_map import render_district_map
from src.components.glass_card import glass_open, glass_close, glass_title
from src.components.kpi_cards import render_kpi_row
from src.components.ranking_chart import render_ranking_chart
from src.components.risk_pie import render_risk_pie
from src.components.trend_chart import render_trend_chart
from src.data_loader import load_covid_data
from src.styles.custom_css import inject_global_styles
from src.utils import build_map_snapshot, filter_by_date_range


st.set_page_config(
    page_title="香港疫情区级 Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()


@st.cache_data(show_spinner=False)
def _load_data():
    """缓存加载，避免重复读取 Excel。"""
    return load_covid_data()


def _init_session():
    """初始化会话状态。"""
    if "selected_district" not in st.session_state:
        st.session_state.selected_district = None


def main() -> None:
    _init_session()
    df = _load_data()

    min_d = df["日期"].min().date()
    max_d = df["日期"].max().date()

    glass_title("香港疫情 · 区级可视化 Dashboard", subtitle="深色主题 · 毛玻璃卡片 · Plotly 交互")

    with st.sidebar:
        st.markdown('<div class="glass-panel-subtle">', unsafe_allow_html=True)
        st.markdown("### 全局日期筛选")
        col_a, col_b = st.columns(2)
        with col_a:
            start = st.date_input("开始日期", value=min_d, min_value=min_d, max_value=max_d)
        with col_b:
            end = st.date_input("结束日期", value=max_d, min_value=min_d, max_value=max_d)
        if start > end:
            st.error("开始日期不能晚于结束日期。")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-panel-subtle">', unsafe_allow_html=True)
        st.markdown("### 趋势对比区域")
        districts = sorted(df["地区"].unique().tolist())
        options = ["（未选择，仅显示全港）"] + districts
        default_idx = 0
        cur = st.session_state.get("selected_district")
        if cur in districts:
            default_idx = districts.index(cur) + 1
        # 不使用固定 key，便于每轮用 index 与地图选中状态同步
        choice = st.selectbox(
            "手动选择或与地图联动",
            options=options,
            index=default_idx,
        )
        if choice.startswith("（未选择"):
            st.session_state.selected_district = None
        else:
            st.session_state.selected_district = choice
        st.caption("提示：在地图上使用套索或框选工具可选中标记点。")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-panel-subtle">', unsafe_allow_html=True)
        st.markdown("### 表格筛选")
        table_filter = st.multiselect("显示哪些地区？", options=districts, default=districts)
        st.markdown("</div>", unsafe_allow_html=True)

    df_range = filter_by_date_range(df, start, end)
    map_snap = build_map_snapshot(df_range)

    render_kpi_row(df_range)

    glass_open()
    st.markdown("##### 主视图 · 地图与趋势联动")
    c1, c2 = st.columns((1.05, 1.0), gap="medium")
    with c1:
        st.caption("地图颜色：区间内新增确诊合计；点位大小：期末现存确诊")
        render_district_map(map_snap, map_key="hk_covid_map")
    with c2:
        render_trend_chart(df_range, st.session_state.get("selected_district"))
    glass_close()

    glass_open()
    st.markdown("##### 排名、风险与明细")
    r1, r2 = st.columns((1.1, 0.9), gap="medium")
    with r1:
        render_ranking_chart(df_range, top_n=10)
    with r2:
        render_risk_pie(df_range)
    glass_close()

    glass_open()
    st.markdown("##### 数据表格（可排序）")
    show_cols = [
        "日期",
        "地区",
        "新增确诊",
        "累计确诊",
        "现存确诊",
        "风险等级",
    ]
    view = df_range[df_range["地区"].isin(table_filter)][show_cols].sort_values(["日期", "地区"])
    st.dataframe(view, use_container_width=True, height=360)
    glass_close()


if __name__ == "__main__":
    main()
