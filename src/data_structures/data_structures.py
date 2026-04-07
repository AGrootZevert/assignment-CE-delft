from pandera.pandas import DataFrameModel, Field
from pandera.typing import Series


class RawTemperatureData(DataFrameModel):
    STN: Series[int]  # Station number
    YYYYMMDD: Series[int]  # year_month_day
    HH: Series[int] = Field(ge=1, le=24)  # hour of the day
    T: Series[int] = Field(nullable=True)  # temperature


class TemperatureData(DataFrameModel):
    date: Series[int]  # year_month_day
    hour: Series[int] = Field(ge=1, le=24)  # hour of the day
    temperature_C: Series[float]  # temperature in degrees C
