# %% imports
import os

from loguru import logger
from scipy.integrate import trapezoid

from src.data_loading.temperature_loader import TemperatureDataLoader
from src.data_processing.process_temperature_data import TemperatureDataProcessor
from src.data_structures.data_structures import HeatData
from src.model.heat_consumption import heat_consumption_heat_pump, heat_request_house
from src.model.heat_pump import HeatPump
from src.model.house import House
from src.visualization.visualize_heat_consumption import visualize_with_average


def main():
    # %% Load and process the temperature data
    data = TemperatureDataLoader.load_temperature_data(
        "temperature_data_bilt_20250101_to_2025_12_31.txt"
    )
    hourly_data = TemperatureDataProcessor.process_temperature_data(data)

    # %% Set up model
    RC = 2.5  # RC value for 1992. https://vkmakelaars.nl/blog/bouwkundig-advies/aan-het-bouwjaar-van-je-woning-zien-hoe-die-geisoleerd-is/

    house = House(average_heat_transfer_coefficient=1 / RC, shell_area=400)
    heat_pump = HeatPump()

    # %% determine the temperature setpoint
    hourly_data[HeatData.setpoint_temperature_C] = 15.0  # night temperature

    day_mask = hourly_data[HeatData.hour].between(7, 21)  # Hours for 'daytime temperature'
    hourly_data.loc[day_mask, HeatData.setpoint_temperature_C] = 20.0  # Day temperature

    # %% compute the heat request and heat pump power.
    hourly_data[HeatData.heat_request_house] = heat_request_house(
        house,
        hourly_data[HeatData.setpoint_temperature_C],
        hourly_data[HeatData.outside_temperature_C],
    )
    hourly_data[HeatData.heat_pump_power] = heat_consumption_heat_pump(
        heat_pump,
        hourly_data[HeatData.heat_request_house],
        hourly_data[HeatData.outside_temperature_C],
    )

    # %% Export the data
    os.makedirs("out/figures", exist_ok=True)

    hourly_data.to_csv("out/hourly_data.csv")

    # %% visualization
    logger.debug("Start making figures...")

    figure = visualize_with_average(
        hourly_data,
        HeatData.date_time,
        [HeatData.heat_request_house],
        x_label="Date and time",
        y_label="Heat requested by house [kW]",
        title="Heat request by house",
    )
    figure.write_html("out/figures/heat_request.html")

    figure = visualize_with_average(
        hourly_data,
        HeatData.date_time,
        [HeatData.heat_pump_power],
        x_label="Date and time",
        y_label="Heat pump power [kW]",
        title="Energy consumption of the heatpump",
    )
    figure.write_html("out/figures/heat_pump_power.html")

    figure = visualize_with_average(
        hourly_data,
        HeatData.date_time,
        [HeatData.heat_request_house, HeatData.heat_pump_power],
        x_label="Date and time",
        y_label="Power [kW]",
        title="Energy request of the house and consumption of the heatpump",
    )
    figure.write_html("out/figures/heat_request_and_power_consumption.html")

    logger.debug("... Finished making figures")

    # %% Compute total power consumption
    total_consumption = trapezoid(
        hourly_data[HeatData.heat_pump_power], hourly_data[HeatData.date_time].dt.hour
    )
    logger.info(f"Total heat pump power consumption = {total_consumption} kWh")


# %%
if __name__ == "__main__":
    main()
