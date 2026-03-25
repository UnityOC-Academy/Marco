import csv
import math
import os
import argparse
from urllib.request import urlretrieve

# --- Configuration ---
AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
DATA_FILE = "airports.csv"
EARTH_RADIUS_KM = 6371.0

# Hardcoded data for airports missing or mislabeled in the database
HARDCODED_AIRPORTS = {
    "WSI": {
        "ident": "YSWS",
        "iata_code": "WSI",
        "name": "Western Sydney International (Nancy-Bird Walton) Airport",
        "latitude_deg": -33.8833,
        "longitude_deg": 150.716,
        "type": "large_airport"
    }
}

def download_data():
    if not os.path.exists(DATA_FILE):
        print("Initial setup: Downloading airport database...")
        urlretrieve(AIRPORTS_URL, DATA_FILE)

def calculate_distance(lat1, lon1, lat2, lon2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * EARTH_RADIUS_KM * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_airports_in_range(center_code, min_km, max_km, only_large=True):
    download_data()
    airports_data = []
    center_coords = None
    center_code = center_code.upper()

    # Check hardcoded list for the center airport first
    if center_code in HARDCODED_AIRPORTS:
        entry = HARDCODED_AIRPORTS[center_code]
        center_coords = (entry['latitude_deg'], entry['longitude_deg'])

    with open(DATA_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            airports_data.append(row)
            # Find center coords in CSV if not already found in hardcoded list
            if not center_coords:
                if row['iata_code'] == center_code or row['ident'] == center_code:
                    center_coords = (float(row['latitude_deg']), float(row['longitude_deg']))
    
    if not center_coords:
        return None

    # Add hardcoded airports to the data list for proximity checking
    for code, data in HARDCODED_AIRPORTS.items():
        # Avoid duplicating if the code already exists in the CSV
        if not any(r['iata_code'] == data['iata_code'] for r in airports_data):
            airports_data.append(data)

    results = []
    for row in airports_data:
        if not row['latitude_deg'] or not row['longitude_deg']:
            continue
            
        dist = calculate_distance(center_coords[0], center_coords[1],
                                float(row['latitude_deg']), float(row['longitude_deg']))

        if min_km <= dist <= max_km:
            # Skip if filtering for large and this isn't large (unless it's our hardcoded WSI)
            is_hardcoded = row.get('iata_code') in HARDCODED_AIRPORTS
            if only_large and row['type'] != 'large_airport' and not is_hardcoded:
                continue

            results.append({
                "code": row['iata_code'] if row['iata_code'] else row['ident'],
                "name": row['name'],
                "distance": round(dist, 2),
                "type": row['type']
            })

    # Filter out duplicates (e.g., if the center airport itself is in the results)
    unique_results = {res['code']: res for res in results}.values()
    return sorted(unique_results, key=lambda x: x['distance'])

def main():
    parser = argparse.ArgumentParser(description="Find airports within a distance range.")
    parser.add_argument("code", help="Center airport code (e.g., SYD)")
    parser.add_argument("max_dist", type=float, help="Maximum distance in km")
    parser.add_argument("--min", type=float, default=0.0, help="Minimum distance in km")
    parser.add_argument("--include-all", action="store_true", help="Include all airport types")

    args = parser.parse_args()

    if args.min > args.max_dist:
        print(f"Error: Min ({args.min}km) is greater than Max ({args.max_dist}km).")
        return

    nearby = get_airports_in_range(args.code, args.min, args.max_dist, only_large=not args.include_all)

    if nearby is None:
        print(f"Error: Could not find airport '{args.code.upper()}'.")
    elif not nearby:
        print("No airports found within that criteria.")
    else:
        label = "major" if not args.include_all else "total"
        print(f"\nFound {len(nearby)} {label} airports:")
        print("-" * 75)
        print(f"{'Code':<10} | {'Name':<45} | {'Distance'}")
        print("-" * 75)
        for a in nearby:
            print(f"{a['code']:<10} | {a['name'][:45]:<45} | {a['distance']} km")

if __name__ == "__main__":
    main()