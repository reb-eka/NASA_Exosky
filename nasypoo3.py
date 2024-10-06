"""import pandas as pd
import math
import json

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
excel_file_path = 'gaia_trial_data.xlsx'
df = pd.read_excel(excel_file_path)

# Filter out rows where parallax is less than or equal to 0
df_valid = df[df['parallax'] > 0].copy()  # Keep a copy of valid rows only


# Create empty lists for the x, y, z coordinates
x_vals = []
y_vals = []
z_vals = []

# Loop through the DataFrame and calculate X, Y, Z coordinates
for index, row in df.iterrows():
    ra = row['ra']
    dec = row['dec']
    parallax = row['parallax']
    
    # Perform conversion
    x, y, z = ra_dec_parallax_to_cartesian(ra, dec, parallax)
    
    # Skip appending if the parallax conversion returned None (i.e., invalid data)
    if x is not None and y is not None and z is not None:
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
json_file_path = 'gaia_new_star_data.json'
with open(json_file_path, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print(f"Data saved to {json_file_path}")
"""

import pandas as pd
import math
import json

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
excel_file_path = 'gaia_trial_data.xlsx'
df = pd.read_excel(excel_file_path)

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
json_file_path = 'gaia_new_star_data.json'
with open(json_file_path, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print(f"Data saved to {json_file_path}")
