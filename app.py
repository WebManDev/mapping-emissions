import pandas as pd
from geopy.geocoders import Nominatim
from tqdm import tqdm
import folium

# Load and clean data
file_name = "2023 Disclosed Benchmarking Data for All Covered Buildings.xlsx"
data = pd.read_excel(file_name)
data.columns = data.columns.str.strip()
required_fields = ["Address", "Building Name", "Site EUI (kBtu/sq ft)"]
data = data.dropna(subset=required_fields)

# Geocode addresses
geolocator = Nominatim(user_agent="geoapi")

def geocode_address(address):
    try:
        location = geolocator.geocode(address, timeout=5)
        return (location.latitude, location.longitude) if location else (None, None)
    except:
        return (None, None)

print("Geocoding addresses...")
success_count = 0  # Counter for successful geocodes
results = []  # Store geocoded rows

for _, row in tqdm(data.iterrows(), total=len(data), desc="Geocoding Progress"):
    lat, lon = geocode_address(f"{row['Address']}, {row['City']}, {row['State']} {row['Zip']}")
    if lat and lon:
        results.append({**row, "Latitude": lat, "Longitude": lon})
        print(success_count)
        success_count += 1
    if success_count >= 200:
        break

data = pd.DataFrame(results)  # Convert successful results back to a DataFrame

print(f"Successfully geocoded {success_count} addresses.")

# Create map
map_center = [39.1, -77.2]
montgomery_map = folium.Map(location=map_center, zoom_start=10)
folium.GeoJson(
    "h.geojson",  # Ensure this GeoJSON file exists in the same directory
    name="Council Districts",
    style_function=lambda _: {"fillColor": "blue", "color": "black", "weight": 2, "fillOpacity": 0.3},
).add_to(montgomery_map)

# Use smoke.png as icon and scale based on SEUI
icon_path = "smoke.png"
for _, row in data.iterrows():
    site_eui = row["Site EUI (kBtu/sq ft)"]
    icon_size = int(min(max(site_eui / 5, 20), 300))  # Scale icon size dynamically

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        icon=folium.CustomIcon(icon_path, icon_size=(icon_size, icon_size)),
        popup=(
            f"<b>Building Name:</b> {row['Building Name']}<br>"
            f"<b>Address:</b> {row['Address']}<br>"
            f"<b>Site EUI:</b> {row['Site EUI (kBtu/sq ft)']:.2f} kBtu/sq ft"
        ),
    ).add_to(montgomery_map)

# Save map
map_output_file = "index.html"
montgomery_map.save(map_output_file)
print("Map created and saved as 'index.html'.")
