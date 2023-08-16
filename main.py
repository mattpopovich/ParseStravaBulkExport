import configparser         # Reading the config.cfg file
import csv                  # Reading and parsing Strava's activities.csv file
import os                   # File, path, directory, etc. operations
import sys                  # sys.exit()
import argparse             # Parsing command line arguments
import shutil               # Copy and remove files/folders
import gzip                 # Unzipping folders
import fnmatch              # Filename matching with shell patterns
import logging              # Standard python logging module

from typing import Final, List    # Typing hints: Final[variable type]


# Grabs all the "Activity ID"s for the `target_activity_type` from Strava's
#   activities.csv, gets all of the corresponding activities from the activities
#   folder, moves them into their own folder in the exports folder,
#   and unzips any activities (if necessary)
def create_export_folder(target_activity_type: str, csv_file_path: str, STRAVA_EXPORTED_FOLDER_PATH: str):

    # Initialize a list to store Activity IDs
    activity_filenames: List[str] = []

    # Read the CSV file and extract the filenames for the specified Activity Type
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Activity Type'] == target_activity_type:
                filename = row['Filename']
                alternative_filename = filename.rstrip(".gz")
                if filename == "":
                    logging.warning(f"The activity {row['Activity Name']} on {row['Activity Date']} does not have a Filename... skipping")
                elif os.path.exists(STRAVA_EXPORTED_FOLDER_PATH + "/" + filename):
                    activity_filenames.append(STRAVA_EXPORTED_FOLDER_PATH + "/" + filename)
                elif os.path.exists(STRAVA_EXPORTED_FOLDER_PATH + "/" + alternative_filename):
                    # Sometimes Strava's Filename field is wrong??
                    logging.warning(f"Strava thought there was a file: {STRAVA_EXPORTED_FOLDER_PATH + '/' + filename}\n"
                                    f"         We located it at {STRAVA_EXPORTED_FOLDER_PATH + '/' + alternative_filename}")
                    activity_filenames.append(STRAVA_EXPORTED_FOLDER_PATH + "/" + alternative_filename)
                else:
                    logging.warning(f"Strava throught there was a file: {STRAVA_EXPORTED_FOLDER_PATH + '/' + filename}. "
                        "We could not find it. Skipping...")


    # Print the list of filenames for "Ride" activities
    logging.debug(f"Filenames for '{target_activity_type}' activities:")
    for filename in activity_filenames:
        logging.debug("\t" + filename)

    # Create rides folder
    EXPORT_FOLDER_NAME: Final[str] = "exports"
    RIDES_FOLDER_NAME: str = EXPORT_FOLDER_NAME + "/" + target_activity_type
    if os.path.exists(RIDES_FOLDER_NAME):
        if args.overwrite:
            shutil.rmtree(RIDES_FOLDER_NAME)
        else:
            sys.exit(f"{RIDES_FOLDER_NAME} folder already exists,"
                    " please remove it (or run this script again but with the `--overwrite` flag)")

    os.makedirs(RIDES_FOLDER_NAME)

    # Copy rides into rides folder
    for filename in activity_filenames:
        shutil.copy(filename, RIDES_FOLDER_NAME + "/")

    print(f"Copied {len(activity_filenames)} files to the {RIDES_FOLDER_NAME} folder")

    # Unzip any zipped up folders
    zipped_up_file_paths: List[str] = fnmatch.filter(activity_filenames, "*.gz")
    if len(zipped_up_file_paths) > 0:
        for zipped_up_file_path in zipped_up_file_paths:
            zipped_up_filename = os.path.basename(zipped_up_file_path)
            with gzip.open(zipped_up_file_path, 'rb') as f_zip:
                unzipped_filename: str = zipped_up_filename.rstrip(".gz")
                with open(RIDES_FOLDER_NAME + "/" + unzipped_filename, 'wb') as f_unzip:
                    shutil.copyfileobj(f_zip, f_unzip)
                    logging.debug(f"Unzipped {f_zip.name} to {f_unzip.name}")
                    os.remove(RIDES_FOLDER_NAME + "/" + zipped_up_filename)
                    logging.debug(f"Deleted {RIDES_FOLDER_NAME + '/' + zipped_up_filename}")

    # TODO: Replace this with an integration test that makes sure nothing was changed
    # Mark Strava's exported folder permissions back to what they were
    # os.chmod(STRAVA_EXPORTED_FOLDER_PATH, ORIGINAL_FOLDER_PERMISSIONS)
    # os.chmod(ACTIVITIES_FOLDER_PATH, ORIGINAL_FOLDER_PERMISSIONS)
    # os.chmod(csv_file_path, 0o644)


if __name__ == "__main__":
    # Read and parse the config file
    CONFIG_FILE_PATH: Final[str] = "config.cfg"
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Settings for 'Parse Strava Bulk Export'")
    parser.add_argument("--overwrite", action="store_true", 
                        help="Overwrite previously created exports")
    parser.add_argument("--debug", action="store_true", 
                        help="Output more verbose logging to help with debugging")
    args = parser.parse_args()

    # Configure the logger
    LOG_LEVEL: int = logging.ERROR
    if args.debug:
        LOG_LEVEL: int = logging.DEBUG
    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

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
    else:
        print(f"Parsing the {csv_file_path} file...")

    # Define the Activity Type you want to filter for
    all_activity_types: List[str] = []

    # Find all activity types
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_activity_types.append(row['Activity Type'])

    # Loop through each unique activity type (sorted for repeatability)
    for activity_type in sorted(list(set(all_activity_types))):
        create_export_folder(activity_type, csv_file_path, STRAVA_EXPORTED_FOLDER_PATH)

    print("Complete!")
