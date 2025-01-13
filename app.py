import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
import json
import time
from tqdm import tqdm  # For progress bar

# Step 1: Load the Excel file
file_name = "2023 Disclosed Benchmarking Data for All Covered Buildings.xlsx"
data = pd.read_excel(file_name)

# Step 2: Clean column names
data.columns = data.columns.str.strip()

# Step 3: Filter rows with required fields
required_fields = ["Address", "Building Name", "Site EUI (kBtu/sq ft)"]
filtered_data = data.dropna(subset=required_fields)

# Step 4: Initialize geolocator
geolocator = Nominatim(user_agent="geoapi")

# Define geocoding function with retries
def geocode_address(row):
    full_address = f"{row['Address']}, {row['City']}, {row['State']} {row['Zip']}"
    for attempt in range(3):  # Retry up to 3 times
        try:
            location = geolocator.geocode(full_address, timeout=10)
            if location:
                return location.latitude, location.longitude
        except GeocoderTimedOut:
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
    return None, None

# Step 5: Perform geocoding with progress bar
print("Geocoding addresses...")
filtered_data[['Latitude', 'Longitude']] = list(
    tqdm(
        filtered_data.apply(lambda row: pd.Series(geocode_address(row)), axis=1),
        total=len(filtered_data),
        desc="Geocoding"
    )
)

# Drop rows where geocoding failed
filtered_data = filtered_data.dropna(subset=["Latitude", "Longitude"])

# Step 6: Load GeoJSON file
geojson_file = "h.geojson"  # Replace with your GeoJSON file path
with open(geojson_file, "r") as file:
    geojson_data = json.load(file)

# Step 7: Create a map with the original Leaflet style
map_center = [39.1, -77.2]  # Center of Montgomery County
montgomery_map = folium.Map(location=map_center, zoom_start=10)

# Step 8: Add GeoJSON overlay for council districts
folium.GeoJson(
    geojson_data,
    name="Council Districts",
    style_function=lambda feature: {
        "fillColor": "blue",
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.3,
    },
).add_to(montgomery_map)

# Step 9: Add geocoded building markers with custom smoke plume icons
icon_path = "smoke.png"  # Path to your custom smoke plume image

for _, row in filtered_data.iterrows():
    site_eui = row["Site EUI (kBtu/sq ft)"]
    icon_size = int(min(max(site_eui / 5, 30), 100))  # Scale icon size based on Site EUI

    # Create a custom icon
    custom_icon = folium.CustomIcon(
        icon_image=icon_path,
        icon_size=(icon_size, icon_size)  # Adjust icon size dynamically
    )

    # Add marker with the custom icon
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        icon=custom_icon,
        popup=(
            f"<b>Building Name:</b> {row['Building Name']}<br>"
            f"<b>Address:</b> {row['Address']}, {row['City']}, {row['State']} {row['Zip']}<br>"
            f"<b>Site EUI:</b> {site_eui:.2f} kBtu/sq ft"
        ),
    ).add_to(montgomery_map)

# Step 10: Save the map to an HTML file
map_output_file = "index.html"
montgomery_map.save(map_output_file)

print(f"Map created and saved as '{map_output_file}'.")
