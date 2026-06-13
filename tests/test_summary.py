import pandas as pd


def test_latency_quantiles_are_computable():
    values = pd.Series([1, 2, 3, 4, 100])
    assert values.quantile(0.50) == 3
    assert values.quantile(0.99) > 96

