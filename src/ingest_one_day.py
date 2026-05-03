import argparse
from pathlib import Path
from pybaseball import statcast
import pandas as pd

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

# Start pulling statcast game data

start_date = run_date
end_date = run_date

statcast_df = statcast(start_dt=start_date, end_dt=end_date)

if statcast_df.empty:
    print("No MLB data for this date!")

else:
    statcast_df.to_csv(raw_file_path, index=False) # Convert to CSV, write to raw file path if df not empty

print(f"Running MLB ingestion for date: {run_date}")
print(f"Raw path: {raw_file_path}")
print(f"Silver path: {silver_file_path}")
print(statcast_df.shape)

