# -*- coding: utf-8 -*-
"""
通用工具：日期解析、风险分级、字符串规范化。
"""

from __future__ import annotations

import pandas as pd


def parse_dates(series: pd.Series) -> pd.Series:
    """将日期列转为 pandas datetime（容错）。"""
    return pd.to_datetime(series, errors="coerce")


def normalize_district_name(name: object) -> str:
    """统一区名显示（去空格）。"""
    if pd.isna(name):
        return ""
    return str(name).strip()


def assign_risk_by_new_cases(series: pd.Series) -> pd.Series:
    """
    根据当日新增确诊的分位数划分风险（演示用）。
    低：<=33%；中：<=66%；高：>66%
    """
    s = series.astype(float)
    if s.empty or s.notna().sum() == 0:
        return pd.Series(["未知"] * len(s), index=s.index)
    q1 = s.quantile(0.33)
    q2 = s.quantile(0.66)

    def _bucket(v: float) -> str:
        if pd.isna(v):
            return "未知"
        if v <= q1:
            return "低"
        if v <= q2:
            return "中"
        return "高"

    return s.map(_bucket)


def aggregate_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """按日期汇总全港（新增/累计/现存取合理的聚合方式）。"""
    if df.empty:
        return df
    g = df.groupby("日期", as_index=False).agg(
        新增确诊=("新增确诊", "sum"),
        累计确诊=("累计确诊", "sum"),
        现存确诊=("现存确诊", "sum"),
    )
    return g.sort_values("日期")


def filter_by_date_range(df: pd.DataFrame, start, end) -> pd.DataFrame:
    """按日期闭区间筛选。"""
    if df.empty:
        return df
    mask = (df["日期"] >= pd.Timestamp(start)) & (df["日期"] <= pd.Timestamp(end))
    return df.loc[mask].copy()


def build_map_snapshot(df_range: pd.DataFrame) -> pd.DataFrame:
    """
    生成地图用快照：「新增确诊」为区间内合计；
    「累计确诊」「现存确诊」「风险等级」取各区按时间排序后的最后一条（期末时点）。
    """
    if df_range.empty:
        return df_range
    df_sorted = df_range.sort_values(["地区", "日期"])
    last_rows = df_sorted.groupby("地区", as_index=False).tail(1).copy()
    new_sum = df_range.groupby("地区")["新增确诊"].sum()
    last_rows["新增确诊"] = last_rows["地区"].map(new_sum).astype(float)
    cols = ["地区", "新增确诊", "累计确诊", "现存确诊"]
    if "风险等级" in last_rows.columns:
        cols.append("风险等级")
    return last_rows[cols].reset_index(drop=True)
