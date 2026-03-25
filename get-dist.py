import csv
import math
import os
import sys
import argparse
from urllib.request import urlretrieve

# --- Configuration ---
AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
DATA_FILE = "airports.csv"

EARTH_RADII = {"km": 6371.0, "mi": 3958.8, "nm": 3440.1}
UNIT_LABELS = {"km": "km", "mi": "mi", "nm": "nm", "country": "km", "continent": "km"}

# --- Airline Hub Registry ---
AIRLINE_HUBS = {
    # Oceania - New Zealand
    "NZ": {"AKL", "CHC", "WLG", "ZQN", "NSN", "DUD"}, # Added ZQN, NSN (Regional Hub/Maint), DUD
    "3C": {"CHT", "AKL", "WLG"}, # Air Chathams (CHT = Chatham Islands)
    "S8": {"WLG", "BHE", "NSN"}, # Sounds Air (BHE = Blenheim, NSN = Nelson)
    
    # Oceania - Australia
    "QF": {"SYD", "MEL", "BNE", "PER", "ADL", "DRW", "TMW", "CNS", "TSV", "CBR", "WSI"}, 
    "VA": {"BNE", "MEL", "SYD", "ADL", "PER"},
    "JQ": {"MEL", "SYD", "BNE", "OOL", "AKL", "ADL", "CHC", "CNS", "PER", "ZQN", "WLG"},
    "ZL": {"SYD", "MEL", "BNE", "ADL", "PER", "TSV", "CNS", "WGA", "WSI"},

    # Global Majors (Sample)
    "SQ": {"SIN"}, "NZ": {"AKL", "CHC", "WLG", "ZQN", "NSN", "DUD"}, 
    "CX": {"HKG"}, "AA": {"DFW", "ORD", "CLT", "MIA"}, "BA": {"LHR", "LGW"},
    "LH": {"FRA", "MUC"}, "EK": {"DXB"}, "FJ": {"NAN", "SUV"} # Fiji Airways
}

HARDCODED_AIRPORTS = {
    "WSI": {
        "ident": "YSWS", "iata_code": "WSI", "type": "large_airport",
        "name": "Western Sydney International Airport",
        "latitude_deg": -33.8833, "longitude_deg": 150.716, "iso_country": "AU", "continent": "OC"
    }
}

class PrettierParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f'Error: {message}\n\n')
        self.print_help()
        sys.exit(2)

def download_data():
    if not os.path.exists(DATA_FILE):
        print(">> Initial setup: Downloading airport database...")
        urlretrieve(AIRPORTS_URL, DATA_FILE)

def calculate_distance(lat1, lon1, lat2, lon2, unit="km"):
    calc_unit = "km" if unit in ["country", "continent"] else unit
    radius = EARTH_RADII.get(calc_unit, EARTH_RADII["km"])
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_airlines_at_airport(iata_code):
    if not iata_code: return ""
    matches = [airline for airline, hubs in AIRLINE_HUBS.items() if iata_code.upper() in hubs]
    return ", ".join(sorted(set(matches)))

def get_airports_in_range(center_code, min_dist, max_dist, unit="km", filter_mode="large", 
                           hub_airline=None, same_country=False, same_continent=False):
    download_data()
    airports_data = []
    origin = None
    center_code = center_code.upper()

    with open(DATA_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            airports_data.append(row)
            if not origin:
                if row['iata_code'] == center_code or row['ident'] == center_code:
                    origin = row
    
    if not origin and center_code in HARDCODED_AIRPORTS:
        origin = HARDCODED_AIRPORTS[center_code]

    if not origin: return None

    for _, data in HARDCODED_AIRPORTS.items():
        if not any(r['iata_code'] == data['iata_code'] for r in airports_data):
            airports_data.append(data)

    ga_types = {'large_airport', 'medium_airport', 'small_airport'}
    hub_set = set().union(*AIRLINE_HUBS.values()) if hub_airline == "ALL" else (AIRLINE_HUBS.get(hub_airline.upper(), set()) if hub_airline else set())

    results = []
    for row in airports_data:
        if not row['latitude_deg'] or not row['longitude_deg']: continue
        if same_country and row['iso_country'] != origin['iso_country']: continue
        if same_continent and row['continent'] != origin['continent']: continue

        dist = calculate_distance(float(origin['latitude_deg']), float(origin['longitude_deg']),
                                float(row['latitude_deg']), float(row['longitude_deg']), unit=unit)

        is_in_range = (min_dist <= dist <= max_dist) if unit not in ["country", "continent"] else True

        if is_in_range:
            iata = row['iata_code']
            if filter_mode == "hub" and iata not in hub_set: continue
            elif filter_mode == "large" and row['type'] != 'large_airport': continue
            elif filter_mode == "ga" and row['type'] not in ga_types: continue

            results.append({
                "code": iata if iata else row['ident'],
                "name": row['name'],
                "distance": round(dist, 2),
                "type": row['type'],
                "airlines": get_airlines_at_airport(iata)
            })

    return sorted({res['code']: res for res in results}.values(), key=lambda x: x['distance'])

def main():
    parser = PrettierParser(description="✈️  Airport Proximity Finder")
    parser.add_argument("code", help="IATA/ICAO code")
    parser.add_argument("max_dist", type=float, help="Max search radius")
    parser.add_argument("-u", "--unit", choices=["km", "mi", "nm", "country", "continent"], default="km")
    parser.add_argument("-c", "--same-country", action="store_true")
    parser.add_argument("-K", "--same-continent", action="store_true")
    
    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument("--ga", action="store_true")
    filter_group.add_argument("--hub", nargs='?', const='ALL', metavar="AIRLINE")
    filter_group.add_argument("--include-all", action="store_true")

    args = parser.parse_args()
    mode = "hub" if args.hub else ("ga" if args.ga else ("all" if args.include_all else "large"))
    country_filter = (args.unit == "country" or args.same_country)
    continent_filter = (args.unit == "continent" or args.same_continent)

    nearby = get_airports_in_range(args.code, 0, args.max_dist, unit=args.unit, 
                                   filter_mode=mode, hub_airline=args.hub, 
                                   same_country=country_filter, same_continent=continent_filter)

    if nearby is None:
        print(f"Error: Could not find '{args.code.upper()}'.")
    elif not nearby:
        print("No matches found.")
    else:
        unit_str = UNIT_LABELS[args.unit]
        tag = []
        if country_filter: tag.append("DOMESTIC")
        if continent_filter: tag.append("CONT.")
        tag.append("HUBS" if args.hub else mode.upper())
        label = " ".join(tag)
        header = f"Found {len(nearby)} {label} within {args.max_dist} {unit_str}" if args.unit not in ["country", "continent"] else f"Found {len(nearby)} {label} entries"
        
        print(f"\n{header} of {args.code.upper()}:")
        print("=" * 110)
        print(f"{'Code':<8} | {'Name':<40} | {'Distance':<12} | {'Hubbed Airlines'}")
        print("-" * 110)
        for a in nearby:
            if a['distance'] == 0: continue
            print(f"{a['code']:<8} | {a['name'][:40]:<40} | {a['distance']:>6} {unit_str:<4} | {a['airlines']}")
        print("=" * 110)

if __name__ == "__main__":
    main()