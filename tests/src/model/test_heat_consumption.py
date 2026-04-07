from unittest.mock import Mock

import pandas as pd
import pytest

from src.constants import W_TO_KW
from src.model.heat_consumption import heat_consumption_heat_pump, heat_request_house
from src.model.heat_pump import HeatPump
from src.model.house import House


@pytest.mark.parametrize(
    "U, A, T_set, T_out",
    [
        (2, 100, 20, pd.Series([10.0, 12.0, 15.0])),
        (2, 100, pd.Series([20.0, 21.0, 22.0]), pd.Series([10.0, 12.0, 15.0])),
        (2, 100, 15.0, pd.Series([15.0, 15.0, 15.0])),
        (2, 100, 10.0, pd.Series([15.0, 15.0, 15.0])),
    ],
)
def test_heat_request(U: float, A: float, T_set: float | pd.Series, T_out: pd.Series):
    """Test heat request with constant float setpoint"""
    house = House(average_heat_transfer_coefficient=U, shell_area=A)
    result = heat_request_house(house, T_set, T_out)
    expected = U * A * (T_set - T_out) * W_TO_KW
    pd.testing.assert_series_equal(result, expected)


@pytest.mark.parametrize(
    "COP, heat_request, T_out",
    [
        (pd.Series([3.0, 3.5, 2.5]), pd.Series([6.0, 7.0, 5.0]), pd.Series([10.0, 12.0, 8.0])),
        (pd.Series([4.0, 4.0, 4.0]), pd.Series([12.0, 16.0, 8.0]), pd.Series([10.0, 12.0, 8.0])),
        (pd.Series([4.0, 4.0, 4.0]), pd.Series([0, 0, 0]), pd.Series([10.0, 12.0, 8.0])),
    ],
)
def test_heat_pump_consumption(COP: pd.Series, heat_request: pd.Series, T_out: pd.Series):
    """Test heat pump energy consumption calculation"""
    heat_pump = Mock(spec=HeatPump)
    heat_pump.get_COP.return_value = COP

    result = heat_consumption_heat_pump(heat_pump, heat_request, T_out)

    expected = heat_request / heat_pump.get_COP(T_out)
    pd.testing.assert_series_equal(result, expected)
