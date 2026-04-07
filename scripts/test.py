# %%
from src.data_loading.temperature_loader import TemperatureDataLoader

# %%
data = TemperatureDataLoader.load_temperature_data(
    "temperature_data_bilt_20250101_to_2025_12_31.txt"
)


print(data.columns)
# %%
