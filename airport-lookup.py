import argparse
import pandas as pd
from sqlalchemy import create_engine, text

# 2026 Python 3.14 Performance: We use the engine globally
DB_URL = "postgresql://admin:synology_secure_2026@db:5432/aviation"
engine = create_engine(DB_URL)

def get_airport_by_code(code):
    """Lookup by IATA or ICAO using indexed SQL."""
    query = text("SELECT * FROM airports WHERE iata = :c OR icao = :c")
    return pd.read_sql(query, engine, params={"c": code.upper()})

def search_nearby(lat, lon, radius_km=100):
    """The 'Cool' Spatial Query: Finds airports within a radius."""
    query = text("""
        SELECT name, city, iata, icao,
               ST_Distance(geometry::geography, ST_MakePoint(:lon, :lat)::geography) / 1000 as dist_km
        FROM airports
        WHERE ST_DWithin(geometry::geography, ST_MakePoint(:lon, :lat)::geography, :dist)
        ORDER BY dist_km ASC
    """)
    params = {"lat": lat, "lon": lon, "dist": radius_km * 1000}
    return pd.read_sql(query, engine, params=params)

def main():
    parser = argparse.ArgumentParser(description="2026 Spatial Airport CLI")
    parser.add_argument("code", help="IATA or ICAO code", nargs='?')
    parser.add_argument("--nearby", help="Search near lat,lon (e.g. 33.9,-118.4)", type=str)
    
    args = parser.parse_args()

    if args.nearby:
        lat, lon = map(float, args.nearby.split(','))
        results = search_nearby(lat, lon)
        print(f"\n📍 Airports within 100km of {lat}, {lon}:")
        print(results[['name', 'iata', 'dist_km']].to_string(index=False))
        
    elif args.code:
        res = get_airport_by_code(args.code)
        if not res.empty:
            print(f"\n✈️ Found: {res.iloc[0]['name']}")
            print(f"📍 Location: {res.iloc[0]['city']}, {res.iloc[0]['country']}")
            print(f"⏰ Timezone: {res.iloc[0]['tz']}")
        else:
            print(f"❌ Code '{args.code}' not found.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()