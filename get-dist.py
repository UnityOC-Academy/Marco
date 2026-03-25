import csv
import math
import os
import sys
import argparse
from urllib.request import urlretrieve

# --- Configuration ---
AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
DATA_FILE = "airports.csv"

EARTH_RADII = {
    "km": 6371.0,
    "mi": 3958.8,
    "nm": 3440.1
}

# Threshold for a "useful" search (50km converted to other units)
MIN_RECOMMENDED_KM = 50.0

UNIT_LABELS = {"km": "km", "mi": "mi", "nm": "nm"}

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
    radius = EARTH_RADII.get(unit, EARTH_RADII["km"])
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_airports_in_range(center_code, min_dist, max_dist, unit="km", only_large=True):
    download_data()
    airports_data = []
    center_coords = None
    center_code = center_code.upper()

    with open(DATA_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            airports_data.append(row)
            if not center_coords:
                if row['iata_code'] == center_code or row['ident'] == center_code:
                    center_coords = (float(row['latitude_deg']), float(row['longitude_deg']))
    
    if not center_coords and center_code in HARDCODED_AIRPORTS:
        entry = HARDCODED_AIRPORTS[center_code]
        center_coords = (entry['latitude_deg'], entry['longitude_deg'])

    if not center_coords:
        return None

    for code, data in HARDCODED_AIRPORTS.items():
        if not any(r['iata_code'] == data['iata_code'] for r in airports_data):
            airports_data.append(data)

    results = []
    for row in airports_data:
        if not row['latitude_deg'] or not row['longitude_deg']:
            continue
            
        dist = calculate_distance(center_coords[0], center_coords[1],
                                float(row['latitude_deg']), float(row['longitude_deg']), 
                                unit=unit)

        if min_dist <= dist <= max_dist:
            is_hardcoded = row.get('iata_code') in HARDCODED_AIRPORTS
            if only_large and row['type'] != 'large_airport' and not is_hardcoded:
                continue

            results.append({
                "code": row['iata_code'] if row['iata_code'] else row['ident'],
                "name": row['name'],
                "distance": round(dist, 2),
                "type": row['type']
            })

    unique_results = {res['code']: res for res in results}.values()
    return sorted(unique_results, key=lambda x: x['distance'])

def main():
    parser = PrettierParser(
        description="✈️  Airport Proximity Finder: Find airports within a specific radius.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python get-dist.py SYD 500              # Major airports within 500km of Sydney
  python get-dist.py LAX 100 -u nm        # Major airports within 100nm of LAX
  python get-dist.py LHR 50 --include-all # All airfields within 50km of Heathrow
        """
    )

    required = parser.add_argument_group('Required Arguments')
    required.add_argument("code", metavar="AIRPORT_CODE", help="IATA or ICAO code (e.g., SYD, KJFK)")
    required.add_argument("max_dist", metavar="MAX_DISTANCE", type=float, help="Maximum radius to search")

    optional = parser.add_argument_group('Optional Settings')
    optional.add_argument("--min", type=float, default=0.0, metavar="DIST", help="Minimum distance (default: 0.0)")
    optional.add_argument("-u", "--unit", choices=["km", "mi", "nm"], default="km", 
                        help="Distance unit: km, mi, nm. Default: km")
    optional.add_argument("--include-all", action="store_true", 
                        help="Include small/medium airfields")

    args = parser.parse_args()

    # --- Unit-Aware Logic ---
    radius = EARTH_RADII[args.unit]
    half_circumference = math.pi * radius
    # Convert 50km recommendation to chosen unit
    unit_threshold = MIN_RECOMMENDED_KM * (radius / EARTH_RADII["km"])
    
    # 1. Physical impossibility check (Antipode)
    if args.max_dist > half_circumference or args.min > half_circumference:
        print(f"❌ Error: Distance exceeds the antipode limit ({round(half_circumference, 1)} {args.unit})!")
        print(f"   You're searching further than the opposite side of the planet.")
        return

    # 2. Logic check
    if args.min > args.max_dist:
        print(f"❌ Error: Min distance ({args.min}) cannot be greater than Max ({args.max_dist}).")
        return

    # 3. "Small Search" Warning (Prudence check)
    if args.max_dist < unit_threshold:
        print(f"⚠️  Note: {args.max_dist} {args.unit} is a very tight search radius.")
        print(f"   (Typically, 50km / {round(unit_threshold, 1)} {args.unit} is a standard minimum for meaningful results.)\n")

    # --- Fetching Results ---
    nearby = get_airports_in_range(args.code, args.min, args.max_dist, 
                                   unit=args.unit, only_large=not args.include_all)

    if nearby is None:
        print(f"Error: Could not find airport '{args.code.upper()}' in the database.")
    elif not nearby:
        print(f"No airports found within {args.max_dist} {args.unit} of {args.code.upper()}.")
    else:
        label = "MAJOR" if not args.include_all else "TOTAL"
        unit_str = UNIT_LABELS[args.unit]
        print(f"Found {len(nearby)} {label} airports within {args.max_dist} {unit_str} of {args.code.upper()}:")
        print("=" * 80)
        print(f"{'Code':<10} | {'Name':<45} | {'Distance'}")
        print("-" * 80)
        for a in nearby:
            # Hide the center airport from results if distance is 0
            if a['distance'] == 0: continue
            print(f"{a['code']:<10} | {a['name'][:45]:<45} | {a['distance']} {unit_str}")
        print("=" * 80)

if __name__ == "__main__":
    main()