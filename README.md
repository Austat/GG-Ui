# GG-Ui
## GUI for Linux Geo-Shell

<img width="1736" height="940" alt="image" src="https://github.com/user-attachments/assets/6c221ebe-70bb-4674-a989-7e22946ab58d" />

## Overview:

The purpose of GG-Ui is to:

Run the geoip-shell status command.
Read the configured inbound and outbound geoblocking country lists.
Convert country codes from ISO-2 format (e.g., RU, CN, US) to ISO-3 format (RUS, CHN, USA).
Display the results on a world map.
Color countries according to their geoblocking status.

Run from the shell:

python3 GG-Ui.py

## Required Dependencies

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

Additionally, GeoPandas requires several GIS libraries depending on the operating system.

<details>
  <summary>Details about GG-Ui</summary>

External Requirements
1. geoip-shell

The script executes:

Python
sudo geoip-shell status

through:

Python
subprocess.run(
["sudo", "geoip-shell", "status"]
)
 
This means:

geoip-shell must be installed.
The user must have permission to execute it via sudo.
The command must output sections called:
Plain Text
inbound geoblocking:
Näytä lisää rivejä

and

outbound geoblocking:

with lines containing:

Country codes:

for the parser to work correctly.

2. World Map Shapefile

The script loads:

Python
/maps/ne_110m_admin_0_countries.shp

with:

Python
gpd.read_file(...)

This means the Natural Earth shapefile must exist at that exact location.

The shapefile usually consists of several files:

Plain Text
ne_110m_admin_0_countries.shp
ne_110m_admin_0_countries.dbf
ne_110m_admin_0_countries.shx
ne_110m_admin_0_countries.prj
Näytä lisää rivejä

All should be present in the same directory.

How the Script Works
Step 1: Run geoip-shell

Function:

Python
run_geoip_shell()
Näytä lisää rivejä

Executes:

Shell
sudo geoip-shell status
Näytä lisää rivejä

and captures the command output.

Example:

Plain Text
inbound geoblocking:
Country codes: RU CN KP
 
outbound geoblocking:
Country codes: RU IR
Näytä lisää rivejä

The entire text output is returned for processing.

Step 2: Parse Country Codes

Function:

Python
parse_country_codes(output)
Näytä lisää rivejä

Searches for:

Plain Text
inbound geoblocking:
Näytä lisää rivejä

and

Plain Text
outbound geoblocking:
Näytä lisää rivejä

sections in the command output.

It also removes ANSI terminal color codes using:

Python
ANSI_ESCAPE
Näytä lisää rivejä

so colored terminal output doesn't break parsing.

Country codes are extracted and returned as Python sets:

Python
inbound_codes
outbound_codes
Näytä lisää rivejä

Example:

Python
{"RU", "CN", "KP"}
{"RU", "IR"}
``
Näytä lisää rivejä

Step 3: Convert ISO2 to ISO3

Function:

Python
iso2_to_iso3()
Näytä lisää rivejä

Examples:

Python
RU -> RUS
US -> USA
CN -> CHN
DE -> DEU
Näytä lisää rivejä

This conversion is needed because the world map uses ISO-3 country identifiers.

Step 4: Build Color Mapping

Function:

Python
build_color_mapping()
Näytä lisää rivejä

Compares inbound and outbound lists.

Green

Country appears in both lists:

Python
inbound AND outbound
Näytä lisää rivejä

Example:

Python
RU
Näytä lisää rivejä

Result:

Python
"RUS": "green"
Näytä lisää rivejä

Yellow

Country appears in only one list:

Python
inbound OR outbound
Näytä lisää rivejä

Example:

Python
CN
IR
Näytä lisää rivejä

Result:

Python
"CHN": "yellow"
"IRN": "yellow"
Näytä lisää rivejä

Step 5: Load the World Map

Function:

Python
plot_world()
Näytä lisää rivejä

Loads the Natural Earth shapefile.

It uses the field:

Python
SOV_A3
Näytä lisää rivejä

as the ISO-3 country code field.

Step 6: Assign Colors

Each country's ISO-3 code is checked against the generated color map:

Python
color_map.get(iso3, "lightgrey")
`
Näytä lisää rivejä

Meaning:

Status	ColorInbound + Outbound	Green
Only Inbound OR Outbound	Yellow
Not blocked	Light Grey

This color is stored in:

Python
world["color"]
Näytä lisää rivejä

Step 7: Render the Map

GeoPandas draws the map:

Python
world.plot(...)
Näytä lisää rivejä

The script adds:

Black country borders
Legend
Title
Automatic layout adjustment

Legend:

Plain Text
Green = Inbound & outbound blacklist
Yellow = Only inbound or outbound
Light grey = Not blacklisted
Näytä lisää rivejä

Console Output

Before displaying the map, the script prints:

Python
print("Inbound:", inbound_codes)
print("Outbound:", outbound_codes)
print("color_map keys:", color_map.keys())
Näytä lisää rivejä

Example:

Plain Text
Inbound: {'RU', 'CN', 'KP'}
Outbound: {'RU', 'IR'}
color_map keys: dict_keys(['RUS', 'CHN', 'PRK', 'IRN'])
Näytä lisää rivejä

This helps verify that parsing worked correctly.

Workflow Summary
Plain Text
geoip-shell status
│
▼
Read terminal output
│
▼
Extract inbound country codes
Extract outbound country codes
│
▼
Convert ISO2 → ISO3
│
▼
Create country color map
│
▼
Load Natural Earth shapefile
│
▼
Color countries
│
▼
Display world map
Näytä vähemmän

Strengths
Simple and easy to understand.
Automatically visualizes firewall geoblocking configuration.
Uses official ISO country codes.
Removes ANSI terminal formatting safely.
Clearly distinguishes partially and fully blocked countries.
