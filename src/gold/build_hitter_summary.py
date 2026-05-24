# Build out gold hitter summary table

import pandas as pd
import numpy as np
from pybaseball import playerid_reverse_lookup

df = pd.read_parquet("../data/silver/pitches/pitches_2024-04-01.parquet") # Read pitch data parquet file

hitter_df = df[['batter', 'launch_speed', 'launch_angle', 'launch_speed_angle', 'events']] # Get main hitter columns

# Create other main metric columns
hitter_df['barrels'] = np.where(hitter_df['launch_speed_angle'] == 6, 1, 0)
hitter_df['hard_hit'] = np.where(hitter_df['launch_speed'] >= 95,1,0)
hitter_df['home_run'] = np.where(hitter_df['events'] == 'home_run',1,0)
hitter_df['strikeout'] = np.where(hitter_df['events'] == 'strikeout',1,0)
hitter_df['walk'] = np.where(hitter_df['events'] == 'walk',1,0)

# Get unique batter IDs from your cleaned data
unique_batters = hitter_df["batter"].dropna().unique()

# Look up batter names using MLBAM IDs
batter_names_df = playerid_reverse_lookup(
    unique_batters,
    key_type="mlbam"
)

# Format names as "Last, First" to match Statcast player_name format
batter_names_df["player_name"] = (
    batter_names_df["name_last"] + ", " + batter_names_df["name_first"]
)

# Merge names onto hitter dataframe
hitter_df = hitter_df.merge(
    batter_names_df[["key_mlbam", "player_name"]],
    left_on="batter",
    right_on="key_mlbam",
    how="left"
)

# Drop duplicate ID column from lookup
hitter_df = hitter_df.drop(columns=["key_mlbam"])

# Create contact only dataframe
contact_df = hitter_df[hitter_df['launch_speed_angle'].notnull()]

# Create contact summary df, aggregate using dict style for specific columns
contact_summary_df = contact_df.groupby(['batter','player_name']).agg(total_barrels = ('barrels','sum'),
                                                                     total_hard_hits = ('hard_hit','sum'),
                                                                     avg_exit_velocity = ('launch_speed','mean'),
                                                                     avg_launch_angle = ('launch_angle','mean'),
                                                                     total_batted_balls=('launch_speed_angle','count'))

# Create barrel_rate and hard_hit_rate
contact_summary_df['barrel_rate'] = ((contact_summary_df['total_barrels'] / contact_summary_df['total_batted_balls']) * 100).round(2)
contact_summary_df['hard_hit_rate'] = ((contact_summary_df['total_hard_hits'] / contact_summary_df['total_batted_balls']) * 100).round(2)

# Round off other 2 mean columns to 2 decimal places
contact_summary_df['avg_exit_velocity'] = contact_summary_df['avg_exit_velocity'].round(2)
contact_summary_df['avg_launch_angle'] = contact_summary_df['avg_launch_angle'].round(2)

# Reset index of aggregated contact summary df for better analysis later
contact_summary_df.reset_index(inplace=True)
