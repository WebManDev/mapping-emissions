import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
import time

# Step 1: Load the Excel file
file_name = "2023 Disclosed Benchmarking Data for All Covered Buildings.xlsx"
data = pd.read_excel(file_name)

# Step 2: Clean column names
data.columns = data.columns.str.strip()

# Step 3: Initialize geolocatord
geolocator = Nominatim(user_agent="geoapi")

# Define geocoding function with retries
def geocode_address(row, progress):
    full_address = f"{row['Address']}, {row['City']}, {row['State']} {row['Zip']}"
    for attempt in range(3):  # Retry up to 3 times
        try:
            location = geolocator.geocode(full_address, timeout=10)
            if location:
                print(f"[{progress}%] Geocoded: {full_address}")
                return location.latitude, location.longitude
        except GeocoderTimedOut:
            print(f"Timeout: {full_address}, Retrying...")
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
    print(f"[{progress}%] Failed: {full_address}")
    return None, None

# Perform geocoding with progress tracking for the first 10 rows
def geocode_with_progress(data):
    total = len(data)
    geocoded_results = []
    for i, row in data.iterrows():
        if i >= 10:  # Limit to the first 10 rows
            break
        progress = round((i + 1) / 10 * 100, 2)
        latitude, longitude = geocode_address(row, progress)
        geocoded_results.append({"Latitude": latitude, "Longitude": longitude})
    return geocoded_results

# Step 4: Filter rows with all required fields
required_fields = ["Address", "Building Name", "Site EUI (kBtu/sq ft)"]
filtered_data = data.dropna(subset=required_fields).iloc[:10]  # Use only the first 10 rows

# Perform geocoding
print("Starting geocoding for the first 10 rows...")
geocoded_results = geocode_with_progress(filtered_data)

# Update filtered_data with geocoded results
for i, result in enumerate(geocoded_results):
    filtered_data.at[filtered_data.index[i], "Latitude"] = result["Latitude"]
    filtered_data.at[filtered_data.index[i], "Longitude"] = result["Longitude"]

# Filter rows with valid geocoding results
filtered_data = filtered_data.dropna(subset=["Latitude", "Longitude"])

# Step 5: Create a map with the geocoded data
montgomery_map = folium.Map(location=[39.1547, -77.2405], zoom_start=10)

# Add custom smoke plume markers for each building
icon_path = "smoke.png"  # Path to your custom smoke plume image
for _, row in filtered_data.iterrows():
    source_eui = row["Site EUI (kBtu/sq ft)"]
    icon_size = int(min(max(source_eui / 5, 30), 100))  # Scale icon size based on Source EUI

    # Create a custom icon
    custom_icon = folium.CustomIcon(
        icon_image=icon_path,  # Path to the image file
        icon_size=(icon_size, icon_size)  # Adjust icon size dynamically
    )

    # Add the marker with the custom icon
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        icon=custom_icon,
        popup=(
            f"<b>Building Name:</b> {row['Building Name']}<br>"
            f"<b>Address:</b> {row['Address']}, {row['City']}, {row['State']} {row['Zip']}<br>"
            f"<b>Site EUI:</b> {source_eui:.2f} kBtu/sq ft"
        ),
    ).add_to(montgomery_map)

# Step 6: Save the map to an HTML file
map_output_file = "montgomery_map_with_smoke_icons.html"
montgomery_map.save(map_output_file)

print(f"Map created! Open '{map_output_file}' to view.")
