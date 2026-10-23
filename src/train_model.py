import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_climate_data", "data.parquet")
MODEL_PATH = os.path.join(BASE_DIR, "models", "climate_model.pkl")

def train():
    if not os.path.exists(PROCESSED_DATA_PATH):
        print("Processed data not found. Run clean_data.py first.")
        return

    df = pd.read_parquet(PROCESSED_DATA_PATH)

    temp_cols = [c for c in df.columns if "temp" in c.lower()]
    humid_cols = [c for c in df.columns if "humid" in c.lower()]
    wind_cols = [c for c in df.columns if "wind" in c.lower()]
    press_cols = [c for c in df.columns if "press" in c.lower()]

    if not temp_cols or not humid_cols:
        print("Required climate columns missing.")
        return

    target = temp_cols[0]
    features = [c for c in [humid_cols[0], wind_cols[0] if wind_cols else None, press_cols[0] if press_cols else None] if c]

    X = df[features].fillna(df[features].mean())
    y = df[target].fillna(df[target].mean())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Lightweight Random Forest (Max depth 8, 30 trees) keeping disk footprint under 2MB
    model = RandomForestRegressor(n_estimators=30, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Save with joblib level-3 compression
    joblib.dump({"model": model, "features": features}, MODEL_PATH, compress=3)
    print(f"Model successfully saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()