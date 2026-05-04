# -*- coding: utf-8 -*-
"""
读取 Excel 疫情数据，标准化列名，并在缺失文件时生成演示数据。
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

from src.config import DATA_XLSX
from src.utils import assign_risk_by_new_cases, parse_dates

logger = logging.getLogger(__name__)

# 列名别名 -> 标准列名
COLUMN_ALIASES = {
    "日期": ["日期", "report_date", "Date", "date", "报告日期"],
    "地区": ["地区", "区", "district", "District", "區", "区域"],
    "新增确诊": ["新增确诊", "新增", "new_cases", "New", "当日新增"],
    "累计确诊": ["累计确诊", "累计", "cumulative", "累计个案"],
    "现存确诊": ["现存确诊", "现存", "active", "Active"],
    "风险等级": ["风险等级", "风险", "risk", "risk_level", "Risk"],
}


def _find_column(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    """在 DataFrame 中寻找第一个存在的列名。"""
    cols = {str(c).strip(): c for c in df.columns}
    for cand in candidates:
        key = str(cand).strip()
        if key in cols:
            return cols[key]
    # 模糊：忽略大小写
    lower_map = {str(c).strip().lower(): c for c in df.columns}
    for cand in candidates:
        lk = str(cand).strip().lower()
        if lk in lower_map:
            return lower_map[lk]
    return None


def _rename_standard_columns(df: pd.DataFrame) -> pd.DataFrame:
    """将原始列映射为标准中文列名。"""
    out = df.copy()
    rename_map = {}
    for standard, aliases in COLUMN_ALIASES.items():
        found = _find_column(out, aliases)
        if found is not None and found != standard:
            rename_map[found] = standard
    out = out.rename(columns=rename_map)

    required = ["日期", "地区", "新增确诊", "累计确诊", "现存确诊"]
    missing = [c for c in required if c not in out.columns]
    if missing:
        raise ValueError(f"Excel 缺少必要列（或无法识别别名）: {missing}，当前列: {list(out.columns)}")

    out["日期"] = parse_dates(out["日期"])
    out = out.dropna(subset=["日期", "地区"])

    for col in ["新增确诊", "累计确诊", "现存确诊"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)

    out["地区"] = out["地区"].astype(str).str.strip()

    if "风险等级" not in out.columns:
        # 按「日期 + 地区」当日新增计算风险分级
        out["风险等级"] = np.nan
        risks = []
        for d, sub in out.groupby("日期"):
            risks.append(assign_risk_by_new_cases(sub["新增确诊"]).rename(d))
        # 简化：逐行填充
        out["风险等级"] = assign_risk_by_new_cases(out["新增确诊"])
    else:
        out["风险等级"] = out["风险等级"].astype(str).str.strip()
        out.loc[out["风险等级"].isin(["", "nan", "None"]), "风险等级"] = "未知"

    out = out.sort_values(["日期", "地区"]).reset_index(drop=True)
    return out


def build_demo_dataframe() -> pd.DataFrame:
    """生成演示用面板数据（18 区 × 日期序列）。"""
    districts = [
        "中西区",
        "湾仔",
        "东区",
        "南区",
        "油尖旺",
        "深水埗",
        "九龙城",
        "黄大仙",
        "观塘",
        "荃湾",
        "屯门",
        "元朗",
        "北区",
        "大埔",
        "沙田",
        "西贡",
        "葵青",
        "离岛",
    ]
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", periods=45, freq="D")
    rows = []
    cum_tracker = {d: 8000 + (hash(d) % 500) for d in districts}
    for d in dates:
        base = 20 + int(np.sin(d.dayofyear / 8.0) * 15)
        for dist in districts:
            noise = int(rng.integers(-8, 12))
            new_cases = max(0, base + noise + hash(dist) % 7)
            cum_tracker[dist] = cum_tracker[dist] + new_cases
            active = max(0, int(new_cases * (1.2 + rng.random())))
            rows.append(
                {
                    "日期": d,
                    "地区": dist,
                    "新增确诊": float(new_cases),
                    "累计确诊": float(cum_tracker[dist]),
                    "现存确诊": float(active),
                }
            )
    df = pd.DataFrame(rows)
    df["风险等级"] = assign_risk_by_new_cases(df["新增确诊"])
    return df


def load_covid_data(path: Optional[str] = None) -> pd.DataFrame:
    """
    加载疫情数据。
    - 默认读取 config.DATA_XLSX
    - 文件不存在或解析失败时使用演示数据并记录日志
    """
    p = path or str(DATA_XLSX)
    try:
        df_raw = pd.read_excel(p, engine="openpyxl")
        df = _rename_standard_columns(df_raw)
        logger.info("已从 Excel 加载 %s 行数据", len(df))
        return df
    except FileNotFoundError:
        logger.warning("未找到数据文件 %s，使用内置演示数据。", p)
        return build_demo_dataframe()
    except Exception as exc:
        logger.exception("读取 Excel 失败: %s，改用演示数据。", exc)
        return build_demo_dataframe()
