import argparse
from pathlib import Path
import pybaseball
from pybaseball import statcast

parser = argparse.ArgumentParser(description="Date to ingest data for (YYYY-MM-DD)")
parser.add_argument('--date', type=str, required=True,
                    help= "Date to ingest data for (YYYY-MM-DD)") # Dates will be string, REQUIRE a date when running

args = parser.parse_args() # Get the arguments

run_date = args.date # assign date argument to run_date

raw_statcast_folder = Path("data/raw/statcast")
silver_pitches_folder = Path("data/silver/pitches")

raw_file = f"statcast_{run_date}.csv"
silver_file = f"pitches_{run_date}.parquet"

raw_file_path = raw_statcast_folder/raw_file
silver_file_path = silver_pitches_folder/silver_file

# Create data folders for raw and silver if they don't exist
raw_statcast_folder.mkdir(parents=True, exist_ok=True)
silver_pitches_folder.mkdir(parents=True, exist_ok=True)

print(f"Running MLB ingestion for date: {run_date}")
print(f"Raw path: {raw_file_path}")
print(f"Silver path: {silver_file_path}")

