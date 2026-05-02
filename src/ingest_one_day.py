import argparse

parser = argparse.ArgumentParser(description="Date to ingest data for (YYYY-MM-DD)")
parser.add_argument('--date', type=str, required=True,
                    help= "Date to ingest data for (YYYY-MM-DD)") # Dates will be string, REQUIRE a date when running

args = parser.parse_args() # Get the arguments

run_date = args.date # assign date argument to run_date

print(f"Running MLB ingestion for date: {run_date}")

