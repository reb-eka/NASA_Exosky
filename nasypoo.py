"""
One hour of RA is equal to 15 degrees of angular distance.
RA gives the longitude on the celestial sphere (converted to degrees if necessary).
DEC gives the latitude in degrees.

"""


from astroquery.gaia import Gaia
import pandas as pd

# Set a row limit (optional)
Gaia.ROW_LIMIT = 50000

# ADQL query to get star data from Gaia
query = """
SELECT TOP 8000 source_id, ra, dec, phot_g_mean_mag, parallax
FROM gaiadr3.gaia_source
WHERE ra BETWEEN 0 AND 360
AND dec BETWEEN -90 AND 90
ORDER BY phot_g_mean_mag ASC
"""

# SELECT source_id, ra, dec, phot_g_mean_mag, parallax
# FROM gaiadr3.gaia_source
# WHERE ra BETWEEN 150 AND 360
# AND dec BETWEEN -90 AND 90
# ORDER BY phot_g_mean_mag ASC
# LIMIT 5000

# SELECT source_id, ra, dec, phot_g_mean_mag, parallax
# FROM gaiadr3.gaia_source
# WHERE parallax BETWEEN -5 AND 5
# AND ra BETWEEN 150 AND 360
# AND dec BETWEEN -90 AND 90

# Launch the query and get the results
job = Gaia.launch_job(query)
results = job.get_results()

# Convert results to a Pandas DataFrame
df = results.to_pandas()

# Save the DataFrame to an Excel file
df.to_excel('gaia_trial_data.xlsx', index=False)

print("Data saved to gaia_trial_data.xlsx")