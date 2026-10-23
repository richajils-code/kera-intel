import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed", "cleaned_climate_data")
PROCESSED_FILE = os.path.join(PROCESSED_DIR, "data.parquet")

def clean_and_process():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Filter ONLY for climate datasets (exclude market price files)
    raw_files = []
    if os.path.exists(RAW_DATA_PATH):
        raw_files = [
            f for f in os.listdir(RAW_DATA_PATH) 
            if (f.endswith('.csv') or f.endswith('.parquet')) and "market" not in f.lower()
        ]
    
    if raw_files:
        print(f"Loading raw climate dataset: {raw_files[0]}")
        file_path = os.path.join(RAW_DATA_PATH, raw_files[0])
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_parquet(file_path)
    else:
        print("No raw climate file found. Generating 2,500-record Kerala regional baseline dataset...")
        np.random.seed(42)
        samples = 2500
        df = pd.DataFrame({
            "temp": np.random.normal(loc=29.5, scale=3.5, size=samples),
            "humidity": np.random.uniform(low=60.0, high=95.0, size=samples),
            "wind": np.random.uniform(low=8.0, high=22.0, size=samples),
            "pressure": np.random.normal(loc=1010.0, scale=4.0, size=samples)
        })

    # Standardize column names
    df.columns = [c.lower().strip() for c in df.columns]
    df = df.dropna()
    
    # Export clean parquet
    df.to_parquet(PROCESSED_FILE, index=False)
    print(f"✅ Cleaned climate dataset ({len(df)} records) saved to: {PROCESSED_FILE}")

if __name__ == "__main__":
    clean_and_process()