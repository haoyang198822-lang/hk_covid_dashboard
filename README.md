# 香港疫情区级可视化 Dashboard

基于 **Streamlit + Plotly + Pandas** 的香港各区疫情数据可视化应用（**GeoPandas** 为可选依赖，需系统 GDAL），采用深色主题与 **毛玻璃（Glassmorphism）** 卡片风格。

## 功能概览

- 顶部标题与**全局日期筛选**，联动 KPI、地图、趋势图、排名、饼图与表格  
- **KPI**：新增确诊、累计确诊、现存确诊、覆盖区数  
- **左侧交互地图** + **右侧双 Y 轴趋势折线图**（选中区域 vs 全港）  
- **Top10 条形图**、**风险等级饼图**、可筛选 **数据表格**  
- GeoJSON 为空时使用各区近似经纬度的散点地图作为占位，便于开发与演示  

## 环境要求

- Python 3.10+（推荐 3.11）

## 安装与运行

```bash
cd hk_covid_dashboard
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

浏览器默认打开 `http://localhost:8501`。

## 数据文件

将 Excel 放入：

`data/香港各区疫情数据_20250322.xlsx`

### 推荐列名（程序会自动尝试映射同义列）

| 含义       | 推荐列名示例                          |
|------------|---------------------------------------|
| 日期       | `日期`、`report_date`、`Date`         |
| 区名       | `地区`、`区`、`district`、`District`  |
| 新增确诊   | `新增确诊`、`新增`、`new_cases`       |
| 累计确诊   | `累计确诊`、`累计`、`cumulative`      |
| 现存确诊   | `现存确诊`、`现存`、`active`          |
| 风险等级   | `风险等级`、`风险`、`risk`、`risk_level`（可选） |

若缺少「风险等级」，程序会根据当日各区新增确诊分位数自动划分为低/中/高。

若 Excel 缺失或无法读取，程序将使用**内置演示数据**启动（便于界面调试）。

## 地图数据

将各区边界 GeoJSON 置于：

`geojson/hk_districts.geojson`

当前仓库可为空 `FeatureCollection`；非空且含与 Excel 一致的区名属性时，将尝试使用地理边界绘制（属性字段名可在 `src/config.py` 中配置）。

## 项目结构

```
hk_covid_dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── 香港各区疫情数据_20250322.xlsx
├── geojson/
│   └── hk_districts.geojson
└── src/
    ├── __init__.py
    ├── config.py
    ├── data_loader.py
    ├── utils.py
    ├── styles/
    │   └── custom_css.py
    └── components/
        ├── __init__.py
        ├── glass_card.py
        ├── kpi_cards.py
        ├── district_map.py
        ├── trend_chart.py
        ├── ranking_chart.py
        └── risk_pie.py
```

说明：Python 包约定使用 `__init__.py`（而非 `init.py`），以保证 `from src.xxx` 导入正常。

## 许可证

仅供学习与非商业演示使用；疫情数据请以官方发布为准。
