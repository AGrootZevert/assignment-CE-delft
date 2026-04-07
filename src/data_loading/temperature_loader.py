import os

import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from pandera.typing import DataFrame

from src.data_structures.data_structures import RawTemperatureData

# Load the enviroment variables
load_dotenv()


class TemperatureDataLoader:
    folder: str = os.getenv("TEMPERATURE_DATA_PATH")

    @classmethod
    def load_temperature_data(
        cls, file_name: str, nrows_header: int = 10
    ) -> DataFrame[RawTemperatureData]:
        """Read the temperature data from the provided file


        Args:
            file_name (str): The file to read including extension
            nrows_header (int, optional): The number of rows to skip while reading the data

        Returns:
            DataFrame[RawTemperatureData]: The temperature data according the the RawTemperatureData
            structure
        """
        # Get the path to the data
        path = cls.folder + "/" + file_name
        logger.debug(f"Loading temperature data: {path}...")

        # Read the data
        data = pd.read_csv(path, header=nrows_header)

        # Strip the colum names from unwanted whitespaces and characters
        data.columns = data.columns.str.replace(r"[\s#]+", "", regex=True)

        # Validate the loaded data format
        RawTemperatureData.validate(data)

        logger.debug("... Loading of temperature data complete.")
        return data
