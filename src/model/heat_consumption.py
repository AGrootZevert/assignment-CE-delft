import pandas as pd

from src.constants import W_TO_KW
from src.model.heat_pump import HeatPump
from src.model.house import House


def heat_request_house(
    house: House, T_setpoint: float | pd.Series, T_outside: pd.Series
) -> pd.Series:
    """Model the heat consumption of a house based on the temperature setpoint and the outside temperature

    Args:
        house (House): The house for which to model the heat consumption
        T_setpoint (float | pd.Series): The temperature setpoint [C]
        T_outside (pd.Series): The outside temperature [C]

    Returns:
        pd.Series: The heat consumption of the house [kW]
    """
    heat_consumption = (
        house.average_heat_transfer_coefficient
        * house.shell_area
        * (T_setpoint - T_outside)
        * W_TO_KW
    )
    return heat_consumption


def heat_consumption_heat_pump(
    heat_pump: HeatPump, heat_request_house: pd.Series, outside_temperature: pd.Series
) -> pd.Series:
    """Compute the heat consumption of the heat pump based on the request of the house


    Args:
        heat_pump (HeatPump): The heat pump to use
        heat_request_house (pd.Series): House heat request from heat pump [kW]

    Returns:
        pd.Series: the energy consumption of the heat pump [kW]
    """
    return heat_request_house / heat_pump.get_COP(outside_temperature)
