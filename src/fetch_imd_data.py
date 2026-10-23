import os
import imdlib as imd

# Define storage directory
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
os.makedirs(output_dir, exist_ok=True)

# Download high-resolution daily max temperature data for India
start_yr = 2020
end_yr = 2023
variable = "tmax" # 'tmax' (max temp), 'tmin' (min temp), or 'rain'

print(f"Downloading IMD {variable} data from {start_yr} to {end_yr}...")
data = imd.get_data(variable, start_yr, end_yr, fn_format='yearwise', file_dir=output_dir)

# Convert IMD grid binaries to CSV for Kerala bounding box
# Kerala approx bounding coordinates: Lat 8.2°N to 12.8°N, Lon 74.8°E to 77.5°E
ds = data.get_xarray()
kerala_ds = ds.sel(lat=slice(8.2, 12.8), lon=slice(74.8, 77.5))
kerala_df = kerala_ds.to_dataframe().reset_index()

csv_path = os.path.join(output_dir, "kerala_imd_climate.csv")
kerala_df.dropna().to_csv(csv_path, index=False)
print(f"Saved Kerala IMD Climate Dataset to: {csv_path}")