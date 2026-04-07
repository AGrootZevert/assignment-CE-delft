from dataclasses import dataclass

import pandas as pd


@dataclass
class HeatPump:
    """Class containing all the information to define a heat pump"""

    def get_COP(self, temperature: pd.Series) -> float:
        """Compute the temperature dependent COP. Formula taken from
        https://docs.energytransitionmodel.com/main/heat-pumps/ for space heating using air source
        heat pumps

        Args:
            temperature (pd.Series): The outside temperature [C]

        Returns:
            float: The COP of the heat pump
        """
        return 3.25 + 0.0875 * temperature
