from astroquery.gaia import Gaia
import pandas as pd
import math
import json

# Define the RA and DEC of your exoplanet
ra_exoplanet = 180  # Replace with the actual RA of your exoplanet
dec_exoplanet = -30  # Replace with the actual DEC of your exoplanet

# Define the search range (in degrees)
search_radius = 1.0  # 1 degree

# Create the ADQL query
query = f"""
SELECT TOP 2000 source_id, ra, dec, phot_g_mean_mag, parallax
FROM gaiadr3.gaia_source 
WHERE ra BETWEEN {ra_exoplanet - search_radius} AND {ra_exoplanet + search_radius} 
AND dec BETWEEN {dec_exoplanet - search_radius} AND {dec_exoplanet + search_radius}
ORDER BY phot_g_mean_mag ASC
"""

# Launch the query
job = Gaia.launch_job(query)
results = job.get_results()

# Convert results to a Pandas DataFrame
df = results.to_pandas()

# Save the DataFrame to an Excel file
output_file = 'exoplanet_star_data.xlsx'
df.to_excel(output_file, index=False)

print("Star data saved to exoplanet_star_data.xlsx")


# Function to convert RA, Dec, and parallax to Cartesian coordinates
def ra_dec_parallax_to_cartesian(ra_deg, dec_deg, parallax_mas):
    # Convert RA and Dec from degrees to radians
    ra_rad = math.radians(ra_deg)
    dec_rad = math.radians(dec_deg)

    # Convert parallax from milliarcseconds to distance in parsecs
    if parallax_mas <= 0:
        return None, None, None  # Skip invalid parallax values
    
    # Convert parallax from milliarcseconds to parsecs (assuming input is in mas)
    distance_parsecs = 1 / (parallax_mas / 1000)
    
    # Calculate Cartesian coordinates
    x = distance_parsecs * math.cos(dec_rad) * math.cos(ra_rad)
    y = distance_parsecs * math.cos(dec_rad) * math.sin(ra_rad)
    z = distance_parsecs * math.sin(dec_rad)

    return x, y, z

# Load the Excel file
# excel_file_path = 'gaia_trial_data.xlsx'
# df = pd.read_excel(excel_file_path)

df = pd.read_excel(output_file)

# Filter out rows where parallax is less than or equal to 0
df_valid = df[df['parallax'] > 0].copy()  # Keep a copy of valid rows only

# Create empty lists for the x, y, z coordinates
x_vals = []
y_vals = []
z_vals = []

# Loop through the filtered DataFrame and calculate X, Y, Z coordinates
for index, row in df_valid.iterrows():
    ra = row['ra']
    dec = row['dec']
    parallax = row['parallax']
    
    # Perform conversion
    x, y, z = ra_dec_parallax_to_cartesian(ra, dec, parallax)
    
    # Append the values directly (since we have filtered valid data)
    x_vals.append(x)
    y_vals.append(y)
    z_vals.append(z)

# Add X, Y, Z coordinates to the filtered DataFrame
df_valid['X'] = x_vals
df_valid['Y'] = y_vals
df_valid['Z'] = z_vals

# Convert the filtered DataFrame to a dictionary for JSON
data_dict = df_valid.to_dict(orient='records')

# Save the data to a JSON file
json_file_path = 'exoplanet_star_data.json'
with open(json_file_path, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print(f"Data saved to {json_file_path}")
