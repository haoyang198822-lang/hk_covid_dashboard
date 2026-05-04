# -*- coding: utf-8 -*-
"""
全局配置：深色主题配色、毛玻璃参数、路径与 GeoJSON 字段名。
"""

from pathlib import Path

# 项目根目录（src 的上级）
ROOT_DIR = Path(__file__).resolve().parent.parent

# 数据与地图路径
DATA_XLSX = ROOT_DIR / "data" / "香港各区疫情数据_20250322.xlsx"
GEOJSON_PATH = ROOT_DIR / "geojson" / "hk_districts.geojson"

# GeoJSON 中与 Excel 「地区」列对齐的属性键（按顺序尝试）
GEOJSON_DISTRICT_KEYS = ("NAME_TC", "name_tc", "District", "district", "区", "NAME", "name")

# -------------------- 深色主题 / 图表配色 --------------------
BG_PAGE = "#0a0e17"
BG_CARD = "rgba(18, 24, 38, 0.55)"
TEXT_PRIMARY = "#e8eefc"
TEXT_MUTED = "#8b9bb4"
ACCENT_CYAN = "#3ee8ff"
ACCENT_PURPLE = "#a78bfa"
ACCENT_PINK = "#fb7185"
ACCENT_GREEN = "#34d399"
ACCENT_AMBER = "#fbbf24"

# Plotly 模板基色
PLOT_BG = "rgba(15, 20, 35, 0.3)"
PAPER_BG = "rgba(0,0,0,0)"

# 序列色（排名条、多系列）
CHART_PALETTE = [
    ACCENT_CYAN,
    ACCENT_PURPLE,
    ACCENT_PINK,
    ACCENT_GREEN,
    ACCENT_AMBER,
    "#60a5fa",
    "#f472b6",
]

# 风险等级颜色
RISK_COLORS = {
    "低": "#34d399",
    "中": "#fbbf24",
    "高": "#fb7185",
    "未知": "#64748b",
}

# -------------------- 毛玻璃（Glassmorphism）CSS 变量 --------------------
GLASS_BORDER = "1px solid rgba(255, 255, 255, 0.12)"
GLASS_SHADOW = "0 8px 32px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255,255,255,0.06)"
GLASS_BLUR = "18px"
GLASS_RADIUS = "16px"
