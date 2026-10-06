# GG-Ui
## GUI for Geo-Shell

## Overview:

The purpose of GG-Ui is to:

Run the geoip-shell status command.
Read the configured inbound and outbound geoblocking country lists.
Convert country codes from ISO-2 format (e.g., RU, CN, US) to ISO-3 format (RUS, CHN, USA).
Display the results on a world map.
Color countries according to their geoblocking status.
Required Dependencies

The script imports:

Python
subprocess
re
pycountry
geopandas
matplotlib.pyplot

Therefore the following Python packages are required:

Shell
pip install pycountry geopandas matplotlib
Näytä lisää rivejä

Additionally, GeoPandas requires several GIS libraries depending on the operating system.
