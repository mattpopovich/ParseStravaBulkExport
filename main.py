import configparser
import csv
import os
import sys                  # sys.exit()
import glob
import argparse
import shutil

from typing import Final, List    # Typing hints: Final[variable type]

CONFIG_FILE_PATH: str = "config.cfg"

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

parser = argparse.ArgumentParser(description="Settings for 'Parse Strava Bulk Export'")
parser.add_argument("--overwrite", action="store_true", help="Overwrite previously created exports")
args = parser.parse_args()

# Define the path to your CSV file
EXPORTED_FOLDER_PATH: Final[str] = config['DEFAULT']['EXPORTED_FOLDER_PATH']
ACTIVITIES_FOLDER_PATH: Final[str] = EXPORTED_FOLDER_PATH + "/activities"
csv_file_path: Final[str] = EXPORTED_FOLDER_PATH + "/activities.csv"

# Check if the CSV file exists before reading
if csv_file_path == "strava_export_########":
    print("Please modify the `EXPORTED_FOLDER_PATH` variable in config.cfg to "
          "match your exported folder name")
elif not os.path.exists(csv_file_path):
    print(f"The CSV file '{csv_file_path}' does not exist, please update "
           "`EXPORTED_FOLDER_PATH` in config.cfg")

# Define the Activity Type you want to filter for
target_activity_type = 'Ride'

# Initialize a list to store Activity IDs
ride_activity_filenames: List[str] = []

# Read the CSV file and extract Activity IDs for the specified Activity Type
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Activity Type'] == target_activity_type:
            ride_activity_filenames.append(EXPORTED_FOLDER_PATH + "/" + row['Filename'])

# Print the list of Activity IDs for "Ride" activities
print("Activity IDs for 'Ride' activities:")
for activity_id in ride_activity_filenames:
    print(activity_id)

# Create rides folder
EXPORT_FOLDER_NAME: Final[str] = "exports"
RIDES_FOLDER_NAME: str = EXPORT_FOLDER_NAME + "/rides"
if os.path.exists(RIDES_FOLDER_NAME):
    if args.overwrite:
        os.rmdir(RIDES_FOLDER_NAME)
    else:
        sys.exit(f"{RIDES_FOLDER_NAME} folder already exists,"
            " please remove it then run this script again")

os.makedirs(RIDES_FOLDER_NAME)

# Copy rides into rides folder
for filename in ride_activity_filenames:
    shutil.copy(filename, RIDES_FOLDER_NAME + "/")

print(f"Copied {len(ride_activity_filenames)} files to the {RIDES_FOLDER_NAME} folder")
