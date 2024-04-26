import csv
import folium

def visualize_vehicle_positions():
    # Create a map centered around New York
    map_ny = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

    # Assuming vehicle_data is your DataFrame and it has 'lat', 'lon', and 'status' columns
    with open("data_output/vehicle_data2023-07-10.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["total_seconds"]) % 3600 != 0:
                continue
            color = 'blue' if row['status'] == 'occupied' else 'red'
            folium.CircleMarker(location=[row['lat'], row['lon']],
                                radius=0.1,
                                color=color,
                                fill=True,
                                fill_color=color).add_to(map_ny)

    # Save or show the map
    map_ny.save('index.html')  # This saves the map as an HTML file you can open in a browser
