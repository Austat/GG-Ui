import subprocess
import re
import pycountry
import geopandas as gpd
import matplotlib.pyplot as plt

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')

def run_geoip_shell():
    # Ajetaan komento ja otetaan stdout talteen
    result = subprocess.run(
        ["sudo", "geoip-shell", "status"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

def parse_country_codes(output: str):
    """
    Parsii inbound/outbound Country codes -rivit.
    Palauttaa (inbound_set, outbound_set) ISO2-koodeina (esim. 'RU', 'CN').
    """
    inbound_codes = set()
    outbound_codes = set()

    # Etsitään blokit "inbound geoblocking:" ja "outbound geoblocking:"
    inbound_block = re.search(
        r"inbound geoblocking:(.*?)(?:\n\n|\Z)",
        output,
        re.DOTALL
    )
    outbound_block = re.search(
        r"outbound geoblocking:(.*?)(?:\n\n|\Z)",
        output,
        re.DOTALL
    )

    def extract_codes(block_match):
        if not block_match:
            return set()
        block = block_match.group(1)
        
        # Poista ANSI-värikoodit
        block = ANSI_ESCAPE.sub('', block)
        
        # Etsitään rivi, joka alkaa "  Country codes:"
        m = re.search(r"Country codes:\s*(.+)", block)
        if not m:
            return set()
        codes_str = m.group(1).strip()
        # Jaetaan välilyönneillä
        return {c.strip().upper() for c in re.split(r"\s+", codes_str) if c.strip()}

    inbound_codes = extract_codes(inbound_block)
    outbound_codes = extract_codes(outbound_block)

    return inbound_codes, outbound_codes

def iso2_to_iso3(code2: str):
    """
    Muuntaa ISO2 -> ISO3 (esim. RU -> RUS) pycountryn avulla.
    Palauttaa None jos ei löydy.
    """
    try:
        country = pycountry.countries.get(alpha_2=code2)
        return country.alpha_3
    except Exception:
        return None

def build_color_mapping(inbound_codes, outbound_codes):
    """
    Palauttaa dict: {ISO3: 'green'/'yellow'}.
    - green: koodi on inbound & outbound
    - yellow: koodi on vain toisessa
    """
    both = inbound_codes & outbound_codes
    only_inbound = inbound_codes - outbound_codes
    only_outbound = outbound_codes - inbound_codes

    color_map = {}

    for code2 in both:
        iso3 = iso2_to_iso3(code2)
        if iso3:
            color_map[iso3] = "green"

    for code2 in only_inbound | only_outbound:
        iso3 = iso2_to_iso3(code2)
        if iso3 and iso3 not in color_map:
            color_map[iso3] = "yellow"

    return color_map
    
def plot_world(color_map):
    """
    Piirtää maailman kartan:
    - maat, jotka löytyvät color_mapista, värjätään sen mukaan
    - muut harmaalla
    """
    world = gpd.read_file("./maps/ne_110m_admin_0_countries.shp")
    
    iso_col = "SOV_A3"

    # Lisätään sarake 'color' kartalle
    def get_color(row):
        iso3 = row[iso_col]
        return color_map.get(iso3, "lightgrey")

    world["color"] = world.apply(get_color, axis=1)

    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    world.plot(color=world["color"], edgecolor="black", ax=ax)

    # Selite
    import matplotlib.patches as mpatches
    green_patch = mpatches.Patch(color="green", label="Inbound & outbound blacklist")
    yellow_patch = mpatches.Patch(color="yellow", label="Vain inbound tai outbound")
    grey_patch = mpatches.Patch(color="lightgrey", label="Ei blacklistissä")

    plt.legend(handles=[green_patch, yellow_patch, grey_patch], loc="lower left")
    plt.title("GeoIP firewall geoblocking – inbound/outbound")
    plt.tight_layout()
    plt.show()

def main():
    output = run_geoip_shell()
    inbound_codes, outbound_codes = parse_country_codes(output)
    color_map = build_color_mapping(inbound_codes, outbound_codes)
    
    print("Inbound:", inbound_codes)
    print("Outbound:", outbound_codes)
    print("color_map keys:", color_map.keys())
    
    plot_world(color_map)

if __name__ == "__main__":
    main()
