import pandas as pd
from loguru import logger
from pandera.typing import DataFrame

from data_structures.data_structures import RawTemperatureData, TemperatureData


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
        processed_data[[TemperatureData.date, TemperatureData.hour]] = cls._get_date_and_time(
            temperature_data
        )
        processed_data[[TemperatureData.temperature_C]] = cls._get_temperature_K(temperature_data)

        # Validate the processed temperature data
        TemperatureData.validate(processed_data)

        # Dataset seems complete
        # Optional TODO: Clean the incoming data.

        logger.debug("Temperature data processed succesfully")
        return processed_data

    def _get_date_and_time(temperature_data: DataFrame[RawTemperatureData]) -> DataFrame:
        """Extract the date and hour from the temperature dataset

        Args:
            temperature_data (DataFrame[RawTemperatureData]): the raw temperature dataset

        Returns:
            DataFrame: The date and hour of the day
        """
        return temperature_data[[RawTemperatureData.YYYYMMDD, RawTemperatureData.HH]]

    def _get_temperature_C(temperature_data: DataFrame[RawTemperatureData]) -> DataFrame:
        """Extract the temperature [0.1C] from the dataset and convert to [C]

        Args:
            temperature_data (DataFrame[RawTemperatureData]): the raw temperature dataset

        Returns:
            DataFrame: The temperature in degrees C
        """
        return temperature_data[RawTemperatureData.T] / 10
