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

    # Select columns to keep that are ideal for future analysis

    selected_columns = [
        "game_date",
        "game_pk",
        "pitcher",
        "batter",
        "player_name",
        "pitch_type",
        "pitch_name",
        "release_speed",
        "release_spin_rate",
        "spin_axis",
        "release_extension",
        "pfx_x",
        "pfx_z",
        "plate_x",
        "plate_z",
        "zone",
        "launch_speed",
        "launch_angle",
        "launch_speed_angle",
        "hit_distance_sc",
        "bb_type",
        "events",
        "estimated_ba_using_speedangle",
        "estimated_woba_using_speedangle",
        "woba_value",
        "babip_value",
        "iso_value",
        "delta_run_exp",
        "delta_home_win_exp",
        "balls",
        "strikes",
        "outs_when_up",
        "inning",
        "inning_topbot",
        "stand",
        "p_throws",
        "home_team",
        "away_team",
        "at_bat_number",
        "pitch_number"
    ]

    available_columns = [col for col in selected_columns if col in statcast_df.columns] # keep available columns to prevent crashing

    # Create silver dataframe from available/selected columns, clean data types

    silver_pitches_df = statcast_df[available_columns].copy()
    
    silver_pitches_df["game_date"] = pd.to_datetime(silver_pitches_df["game_date"], errors="coerce")
    silver_pitches_df["release_speed"] = pd.to_numeric(silver_pitches_df["release_speed"], errors="coerce")
    silver_pitches_df["launch_speed"] = pd.to_numeric(silver_pitches_df["launch_speed"], errors="coerce")
    silver_pitches_df["launch_angle"] = pd.to_numeric(silver_pitches_df["launch_angle"], errors="coerce")

    # Save silver pitches file as Parquet

    silver_pitches_df.to_parquet(silver_file_path, index = False)

    print(f"Running MLB ingestion for date: {run_date}")
    print(f"Raw path: {raw_file_path}")
    print(f"Silver path: {silver_file_path}")
    print(statcast_df.shape)

