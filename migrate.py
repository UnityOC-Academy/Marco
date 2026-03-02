import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry import Point
import os

# Import your original data from the file you provided
from airports_updated import AIRPORTS

# 2026 Connection String
DB_URL = os.getenv("DATABASE_URL", "postgresql://admin:synology_secure_2026@localhost:5432/aviation")
engine = create_engine(DB_URL)

def run_migration():
    print("📦 Converting AIRPORTS list to GeoDataFrame...")
    df = pd.DataFrame(AIRPORTS)
    
    # Convert lat/lon to Point geometry (EPSG:4326 is standard GPS)
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    print("🚀 Outboarding data to PostGIS 18...")
    # 'replace' ensures we have a clean slate; chunksize protects NAS RAM
    gdf.to_postgis("airports", engine, if_exists='replace', index=False, chunksize=1000)
    
    print("✅ Migration complete. Data is now persistent in PostGIS.")

if __name__ == "__main__":
    run_migration()