import pandas as pd
import pytest
from pandera.typing import DataFrame

from src.data_processing.process_temperature_data import TemperatureDataProcessor
from src.data_structures.data_structures import RawTemperatureData, TemperatureData


@pytest.fixture
def input_data() -> DataFrame[RawTemperatureData]:
    return pd.DataFrame(
        {
            RawTemperatureData.STN: [1, 1, 1],
            RawTemperatureData.YYYYMMDD: [20250101, 20250102, 20250103],
            RawTemperatureData.HH: [1, 2, 3],
            RawTemperatureData.T: [250, 270, 280],
        }
    )


def test__get_date_and_time(input_data: DataFrame[RawTemperatureData]):
    """Check if the correct date and hour are obtained"""
    output_data = TemperatureDataProcessor._get_date_time_and_hour(input_data)
    expected = pd.DataFrame(
        {
            RawTemperatureData.YYYYMMDD: pd.to_datetime(
                [2025010100, 2025010201, 2025010302], format="%Y%m%d%H"
            ),
            RawTemperatureData.HH: input_data[RawTemperatureData.HH].values,
        }
    )
    pd.testing.assert_frame_equal(output_data, expected)


def test__get_temperature_C(input_data: DataFrame[RawTemperatureData]):
    """Check if the correct temperature is obtained"""
    output_data = TemperatureDataProcessor._get_temperature_C(input_data)

    pd.testing.assert_series_equal(output_data, input_data[RawTemperatureData.T] / 10)
