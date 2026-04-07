from dataclasses import dataclass


@dataclass
class House:
    """Class containing the information for the house"""

    average_heat_transfer_coefficient: float  # [W/(m^2K})
    shell_area: float  # [m^2]
