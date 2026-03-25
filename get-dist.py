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

# --- Alliance Registry ---
# STRICTURE: KE is SkyTeam. OZ is Star.
ALLIANCES = {
    "oneworld": {"AA", "BA", "IB", "QF", "CX", "JL", "QR", "AY", "AS", "AT", "MH", "UL"},
    "star": {"UA", "LH", "SQ", "NZ", "AC", "NH", "OZ", "TK", "LX", "OS", "SN", "TP", "AI", "ET"},
    "skyteam": {"DL", "AF", "KL", "KE", "AM", "AZ", "SV", "VN", "GA", "ME"}
}

# --- Airline Hub Registry ---
AIRLINE_HUBS = {
    "KE": {"ICN", "GMP", "PUS"}, # SkyTeam
    "OZ": {"ICN", "GMP", "PUS"}, # Star Alliance
    "JL": {"HND", "NRT", "ITM", "KIX"}, "NH": {"HND", "NRT", "ITM", "KIX"},
    "CX": {"HKG"}, "SQ": {"SIN"}, "NZ": {"AKL", "CHC", "WLG", "ZQN", "NSN", "DUD"},
    "EI": {"DUB", "SNN", "ORK"}, "BA": {"LHR", "LGW"}, "IB": {"MAD"}, 
    "LH": {"FRA", "MUC", "BER", "DUS", "HAM", "STR"}, "AF": {"CDG", "ORY"}, "KL": {"AMS"},
    "QF": {"SYD", "MEL", "BNE", "PER", "ADL", "DRW", "TMW", "CNS", "TSV", "CBR", "WSI"}, 
    "VA": {"BNE", "MEL", "SYD", "ADL", "PER"}, "UA": {"ORD", "SFO", "EWR", "DEN", "IAH", "LAX", "IAD"},
    "AA": {"CLT", "DFW", "MIA", "PHL", "PHX", "DCA", "ORD", "LGA", "LAX", "JFK"},
    "DL": {"ATL", "DTW", "MSP", "SLC", "JFK", "LGA", "BOS", "LAX", "SEA"}
}

HARDCODED_AIRPORTS = {
    "WSI": {
        "ident": "YSWS", "iata_code": "WSI", "type": "large_airport",
        "name": "Western Sydney International Airport",
        "latitude_deg": -33.8833, "longitude_deg": 150.716, "iso_country": "AU", "continent": "OC"
    }
}

def download_data():
    if not os.path.exists(DATA_FILE):
        urlretrieve(AIRPORTS_URL, DATA_FILE)

def calculate_distance(lat1, lon1, lat2, lon2, unit="km"):
    radius = EARTH_RADII.get(unit if unit in EARTH_RADII else "km")
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_filtered_airlines(iata_code, alliance_limit=None):
    """Returns airlines at airport, restricted by alliance if one is active."""
    if not iata_code: return ""
    matches = [air for air, hubs in AIRLINE_HUBS.items() if iata_code.upper() in hubs]
    
    if alliance_limit:
        members = ALLIANCES.get(alliance_limit.lower(), set())
        matches = [m for m in matches if m in members]
        
    return ", ".join(sorted(set(matches)))

def get_airports_in_range(center_code, max_dist, unit="km", alliance=None, same_country=False, same_continent=False):
    download_data()
    airports_data = []
    origin = None
    center_code = center_code.upper()

    with open(DATA_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            airports_data.append(row)
            if not origin and (row['iata_code'] == center_code or row['ident'] == center_code):
                origin = row
    
    if not origin and center_code in HARDCODED_AIRPORTS: origin = HARDCODED_AIRPORTS[center_code]
    if not origin: return None

    # Determine which hubs are valid for the current search
    valid_hubs = set()
    if alliance:
        for member in ALLIANCES[alliance.lower()]:
            valid_hubs.update(AIRLINE_HUBS.get(member, set()))

    results = []
    for row in airports_data:
        if not row['latitude_deg'] or not row['longitude_deg']: continue
        if same_country and row['iso_country'] != origin['iso_country']: continue
        if same_continent and row['continent'] != origin['continent']: continue

        dist = calculate_distance(float(origin['latitude_deg']), float(origin['longitude_deg']),
                                float(row['latitude_deg']), float(row['longitude_deg']), unit=unit)

        if (unit not in ["country", "continent"]) and dist > max_dist: continue

        iata = row['iata_code']
        if alliance and iata not in valid_hubs: continue
        
        # Enforce Large Airport rule for general searches
        if not alliance and row['type'] != 'large_airport': continue

        display_airlines = get_filtered_airlines(iata, alliance_limit=alliance)
        if alliance and not display_airlines: continue

        results.append({
            "code": iata if iata else row['ident'],
            "name": row['name'],
            "distance": round(dist, 2),
            "airlines": display_airlines
        })

    return sorted({res['code']: res for res in results}.values(), key=lambda x: x['distance'])

def main():
    parser = argparse.ArgumentParser(description="✈️ Airport Hub & Alliance Finder")
    parser.add_argument("code", help="Origin IATA code")
    parser.add_argument("max_dist", type=float, help="Radius")
    parser.add_argument("-u", "--unit", choices=["km", "mi", "nm", "country", "continent"], default="km")
    parser.add_argument("-c", "--same-country", action="store_true")
    parser.add_argument("-K", "--same-continent", action="store_true")
    parser.add_argument("--alliance", choices=["oneworld", "star", "skyteam"])

    args = parser.parse_args()
    
    res = get_airports_in_range(args.code, args.max_dist, unit=args.unit, alliance=args.alliance,
                                 same_country=(args.unit=="country" or args.same_country),
                                 same_continent=(args.unit=="continent" or args.same_continent))

    if not res:
        print("No matches found.")
        return

    print(f"\nFound {len(res)} results for {args.code.upper()} ({args.alliance or 'All'}):")
    print("=" * 90)
    print(f"{'Code':<8} | {'Name':<40} | {'Distance':<12} | {'Airlines'}")
    print("-" * 90)
    for a in res:
        if a['distance'] == 0: continue
        print(f"{a['code']:<8} | {a['name'][:40]:<40} | {a['distance']:>6} {args.unit:<3} | {a['airlines']}")

if __name__ == "__main__":
    main()