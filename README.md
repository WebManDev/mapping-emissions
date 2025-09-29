🌍 Mapping Emissions

An interactive web-based project that visualizes emissions data to highlight environmental impacts. Built with HTML, JavaScript, and supporting data files, this tool helps users better understand disclosed benchmarking data and visualize pollution through an intuitive map-based interface.

📂 Project Structure

index.html – Main webpage template

index.js – Core JavaScript logic for rendering and interactivity

h.geojson – Geospatial data for mapping (GeoJSON format)

2023 Disclosed Benchmarking Data for All C… – Dataset providing emissions/benchmarking information

smoke.png – Static asset used for visualization

README.md – Documentation (you are here)

🚀 Features

Visualizes emissions data interactively on a map

Uses GeoJSON to overlay location-based emissions

Supports integration of benchmarking data for analysis

Simple web-based interface (no installation required)

🔧 Getting Started
1. Clone the Repository
git clone https://github.com/WebManDev/mapping-emissions.git
cd mapping-emissions

2. Open the App

Just open index.html in your browser, or serve locally for development:

# Using Python 3
python -m http.server 8000


Visit http://localhost:8000
 in your browser.

📊 Data Sources

GeoJSON file – Provides geographic boundaries for emissions mapping.

Benchmarking dataset (2023) – Publicly disclosed benchmarking data for cities/companies.

(Make sure your dataset filenames remain consistent for the app to work.)

🌐 Deployment

This project is deployed via Vercel:
👉 Live Demo

Every push to main auto-deploys to production.

🛠️ Tech Stack

Frontend: HTML, JavaScript

Mapping: GeoJSON

Hosting: Vercel

📌 Future Improvements

Add filtering options by region/year

Improve visualization styles (heatmap, color scales)

Support additional datasets for broader coverage

🤝 Contributing

Pull requests are welcome! If you have suggestions for improvements, feel free to open an issue or submit a PR.

📜 License

This project is open source and available under the MIT License.
