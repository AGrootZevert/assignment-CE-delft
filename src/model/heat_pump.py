from dataclasses import dataclass

import pandas as pd


@dataclass
class HeatPump:
    """Class containing all the information to define a heat pump"""

    COP: float

    def get_COP(self, temperature: pd.Series) -> float:
        """Compute the temperature dependent COP

        Args:
            temperature (pd.Series): The outside temperature [C]

        Returns:
            float: The COP of the heat pump
        """
        return self.COP
