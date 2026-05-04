# -*- coding: utf-8 -*-
"""
毛玻璃卡片容器：通过 HTML + backdrop-filter 实现玻璃质感。
"""

from __future__ import annotations

import streamlit as st


def glass_open(extra_class: str = "") -> None:
    """开启一层玻璃面板（后续 markdown / 组件写入其内）。"""
    cls = f"glass-panel {extra_class}".strip()
    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)


def glass_close() -> None:
    """关闭玻璃面板。"""
    st.markdown("</div>", unsafe_allow_html=True)


def glass_title(text: str, subtitle: str | None = None) -> None:
    """标题区：主标题 + 可选副标题。"""
    glass_open()
    st.markdown(f'<div class="hk-dash-title" style="font-size:1.75rem;">{text}</div>', unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)
    glass_close()


def glass_metric_row_inner(html_fragments: list[str]) -> None:
    """
    在一行玻璃容器内展示多块 HTML（调用方控制栅格）。
    html_fragments: 每项为已转义的 HTML 片段。
    """
    glass_open()
    cols = st.columns(len(html_fragments))
    for col, frag in zip(cols, html_fragments):
        with col:
            st.markdown(frag, unsafe_allow_html=True)
    glass_close()
