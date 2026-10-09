import pandas as pd
from src.processing import calculate_kpis, clean_records

def test_kpis_empty():
    assert calculate_kpis(pd.DataFrame())["records"] == 0

def test_kpis_basic():
    df = pd.DataFrame({"campus":["Mossoró","Zona Norte"],"indicator":["NOA","NPS"],"value":[3,4]})
    result = calculate_kpis(df)
    assert result["records"] == 2
    assert result["campuses"] == 2
    assert result["sum_value"] == 7
