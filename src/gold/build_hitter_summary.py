# Build out gold hitter summary table
import pandas as pd
import numpy as np
from pybaseball import playerid_reverse_lookup

df = pd.read_parquet("../data/silver/pitches/pitches_2024-04-01.parquet") # Read pitch data parquet file

