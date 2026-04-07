from numpy import datetime64
from pandera.pandas import DataFrameModel, Field
from pandera.typing import Series


class RawTemperatureData(DataFrameModel):
    STN: Series[int]  # Station number
    YYYYMMDD: Series[int]  # year_month_day
    HH: Series[int] = Field(ge=1, le=24)  # hour of the day
    T: Series[int] = Field(nullable=True)  # temperature


class TemperatureData(DataFrameModel):
    date_time: Series[datetime64]  # year_month_day_hour
    hour: Series[int] = Field(ge=1, le=24)  # hour of the day
    outside_temperature_C: Series[float]  # outside temperature in degrees C


class HeatData(TemperatureData):
    setpoint_temperature_C: Series[float]  # temperature setpoint of the house [C]
    heat_request_house: Series[float]  # heat request by house [kW]
    heat_pump_power: Series[float]  # energy consumption heat pump [kW]
