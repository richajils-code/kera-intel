# PySpark ETL Pipeline
import os
from pyspark.sql import SparkSession

# 1. Initialize Spark Session
spark = SparkSession.builder \
    .appName("ClimateDataProcessing") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Disable verbose logging
spark.sparkContext.setLogLevel("ERROR")

print("--- PySpark Session Successfully Started ---")

# 2. Locate CSV File
data_dir = os.path.join("data", "raw_climate")
csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

if not csv_files:
    raise FileNotFoundError("No CSV file found in data/raw_climate directory!")

file_path = os.path.join(data_dir, csv_files[0])
print(f"Loading dataset: {file_path}")

# 3. Read Raw CSV with PySpark
df = spark.read.csv(file_path, header=True, inferSchema=True)

# 4. Inspect Data Schema & First 5 Rows
print("\n--- Dataset Schema ---")
df.printSchema()

print("\n--- First 5 Rows ---")
df.show(5)

# 5. Check Total Record Count
total_count = df.count()
print(f"\nTotal Records: {total_count}")

# Stop Spark Session cleanly
spark.stop()
