import pandas as pd
from loguru import logger
from pandera.typing import DataFrame

from src.data_structures.data_structures import RawTemperatureData, TemperatureData


class TemperatureDataProcessor:
    @classmethod
    def process_temperature_data(
        cls, temperature_data: DataFrame[RawTemperatureData]
    ) -> DataFrame[TemperatureData]:
        """Process the raw data into the TemperatureData structure



        Args:
            temperature_data (DataFrame[RawTemperatureData]): The raw temperature data

        Returns:
            DataFrame[TemperatureData]: The processed temperature data
        """
        # Process the temperature data
        processed_data = pd.DataFrame()
        processed_data[[TemperatureData.date_time, TemperatureData.hour]] = (
            cls._get_date_time_and_hour(temperature_data)
        )
        processed_data[TemperatureData.outside_temperature_C] = cls._get_temperature_C(
            temperature_data
        )

        # Validate the processed temperature data
        TemperatureData.validate(processed_data)

        # Dataset is complete
        # Optional TODO: Clean the incoming data.

        logger.debug("Temperature data processed succesfully")
        return processed_data

    @staticmethod
    def _get_date_time_and_hour(temperature_data: DataFrame[RawTemperatureData]) -> DataFrame:
        """Extract the date and hour from the temperature dataset

        Args:
            temperature_data (DataFrame[RawTemperatureData]): the raw temperature dataset

        Returns:
            DataFrame: The date and hour of the day
        """

        date_hour = temperature_data[[RawTemperatureData.YYYYMMDD, RawTemperatureData.HH]].copy()

        date_time_hour = (
            date_hour[RawTemperatureData.HH] - 1
        )  # Change to run the hours from 0 to 23 instead of 1 to 24

        # Make combined string
        date_time_str = date_hour[RawTemperatureData.YYYYMMDD].astype(str) + date_time_hour.astype(
            str
        ).str.zfill(2)
        # Store the date time
        date_hour[RawTemperatureData.YYYYMMDD] = pd.to_datetime(date_time_str, format="%Y%m%d%H")
        return date_hour

    @staticmethod
    def _get_temperature_C(temperature_data: DataFrame[RawTemperatureData]) -> DataFrame:
        """Extract the temperature [0.1C] from the dataset and convert to [C]

        Args:
            temperature_data (DataFrame[RawTemperatureData]): the raw temperature dataset

        Returns:
            DataFrame: The temperature in degrees C
        """
        return temperature_data[RawTemperatureData.T] / 10
