import configparser
import csv
import os
import sys                  # sys.exit()
import glob
import argparse
import shutil
import gzip
import fnmatch

from typing import Final, List    # Typing hints: Final[variable type]

CONFIG_FILE_PATH: str = "config.cfg"

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

parser = argparse.ArgumentParser(description="Settings for 'Parse Strava Bulk Export'")
parser.add_argument("--overwrite", action="store_true", help="Overwrite previously created exports")
args = parser.parse_args()

# Define the path to your CSV file
STRAVA_EXPORTED_FOLDER_PATH: Final[str] = config['DEFAULT']['STRAVA_EXPORTED_FOLDER_PATH']
ACTIVITIES_FOLDER_PATH: Final[str] = STRAVA_EXPORTED_FOLDER_PATH + "/activities"
csv_file_path: Final[str] = STRAVA_EXPORTED_FOLDER_PATH + "/activities.csv"

# Mark the exported folder path as read only so that we don't accidentally modify anything
ORIGINAL_FOLDER_PERMISSIONS = os.stat(STRAVA_EXPORTED_FOLDER_PATH).st_mode & 0o777
# Folders are 755
# Files are 644
# os.chmod(STRAVA_EXPORTED_FOLDER_PATH, 0o555)
# os.chmod(ACTIVITIES_FOLDER_PATH, 0o555)
# os.chmod(csv_file_path, 0o444)

# Check if the CSV file exists before reading
if csv_file_path == "strava_export_########":
    print("Please modify the `STRAVA_EXPORTED_FOLDER_PATH` variable in config.cfg to "
          "match your exported folder name")
elif not os.path.exists(csv_file_path):
    print(f"The CSV file '{csv_file_path}' does not exist, please update "
           "`STRAVA_EXPORTED_FOLDER_PATH` in config.cfg")

# Define the Activity Type you want to filter for
target_activity_type = 'Ride'

# Initialize a list to store Activity IDs
ride_activity_filenames: List[str] = []

# Read the CSV file and extract the filenames for the specified Activity Type
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Activity Type'] == target_activity_type:
            filename = row['Filename']
            alternative_filename = filename.rstrip(".gz")
            if filename == "":
                print(f"WARNING: The activity {row['Activity Name']} on {row['Activity Date']} does not have a Filename... skipping")
            elif os.path.exists(STRAVA_EXPORTED_FOLDER_PATH + "/" + filename):
                ride_activity_filenames.append(STRAVA_EXPORTED_FOLDER_PATH + "/" + filename)
            elif os.path.exists(STRAVA_EXPORTED_FOLDER_PATH + "/" + alternative_filename):
                # Sometimes Strava's Filename field is wrong??
                print(f"WARNING: Strava thought there was a file: {STRAVA_EXPORTED_FOLDER_PATH + '/' + filename}")
                print(f"         We located it at {STRAVA_EXPORTED_FOLDER_PATH + '/' + alternative_filename}")
                ride_activity_filenames.append(STRAVA_EXPORTED_FOLDER_PATH + "/" + alternative_filename)
            else:
                print(f"WARNING: Strava throught there was a file: {STRAVA_EXPORTED_FOLDER_PATH + '/' + filename}. "
                    "We could not find it. Skipping...")


# Print the list of filenames for "Ride" activities
print("Filenames for 'Ride' activities:")
for filename in ride_activity_filenames:
    print("\t" + filename)

# Create rides folder
EXPORT_FOLDER_NAME: Final[str] = "exports"
RIDES_FOLDER_NAME: str = EXPORT_FOLDER_NAME + "/" + target_activity_type
if os.path.exists(RIDES_FOLDER_NAME):
    if args.overwrite:
        shutil.rmtree(RIDES_FOLDER_NAME)
    else:
        sys.exit(f"{RIDES_FOLDER_NAME} folder already exists,"
                  " please remove it then run this script again")

os.makedirs(RIDES_FOLDER_NAME)

# Copy rides into rides folder
for filename in ride_activity_filenames:
    shutil.copy(filename, RIDES_FOLDER_NAME + "/")

print(f"Copied {len(ride_activity_filenames)} files to the {RIDES_FOLDER_NAME} folder")

# Unzip any zipped up folders
zipped_up_file_paths: List[str] = fnmatch.filter(ride_activity_filenames, "*.gz")
if len(zipped_up_file_paths) > 0:
    for zipped_up_file_path in zipped_up_file_paths:
        zipped_up_filename = os.path.basename(zipped_up_file_path)
        with gzip.open(zipped_up_file_path, 'rb') as f_zip:
            unzipped_filename: str = zipped_up_filename.rstrip(".gz")
            with open(RIDES_FOLDER_NAME + "/" + unzipped_filename, 'wb') as f_unzip:
                shutil.copyfileobj(f_zip, f_unzip)
                print(f"Unzipped {f_zip.name} to {f_unzip.name}")
                os.remove(RIDES_FOLDER_NAME + "/" + zipped_up_filename)
                print(f"Deleted {RIDES_FOLDER_NAME + '/' + zipped_up_filename}")

# TODO: Replace this with an integration test that makes sure nothing was changed
# Mark Strava's exported folder permissions back to what they were
# os.chmod(STRAVA_EXPORTED_FOLDER_PATH, ORIGINAL_FOLDER_PERMISSIONS)
# os.chmod(ACTIVITIES_FOLDER_PATH, ORIGINAL_FOLDER_PERMISSIONS)
# os.chmod(csv_file_path, 0o644)
