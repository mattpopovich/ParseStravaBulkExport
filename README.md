# ParseStravaBulkExport

### The Problem:
Strava will let you export all your activities just fine, but it is up to you to find out which activities correspond to biking vs. running, etc. Thankfully, they give you a nice `activities.csv` file telling you some details for each file in the `activities` folder.

### The Solution:
Parse that `activities.csv` file to pull out the activities we want based on certain parameters.

## Use
Modify the `STRAVA_EXPORTED_FOLDER_PATH` variable in `config.cfg` to point to your **unzipped** [Strava Bulk Export](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#h_01GG58HC4F1BGQ9PQZZVANN6WF) folder.

Enter the Dockerfile, then
```console
$ python main.py 
Parsing the strava_export_12345678/activities.csv file...
Copied 1 files to the exports/Stand Up Paddling folder
Copied 6 files to the exports/Kitesurf folder
Copied 6 files to the exports/Walk folder
Copied 20 files to the exports/Inline Skate folder
Copied 145 files to the exports/Velomobile folder
Copied 1 files to the exports/Virtual Ride folder
Copied 1 files to the exports/Golf folder
Copied 1 files to the exports/Ice Skate folder
Copied 98 files to the exports/Run folder
Copied 56 files to the exports/Snowboard folder
Copied 36 files to the exports/Hike folder
Copied 14 files to the exports/Alpine Ski folder
Copied 181 files to the exports/E-Bike Ride folder
Copied 11 files to the exports/Swim folder
Copied 261 files to the exports/Ride folder
Copied 13 files to the exports/Kayaking folder
```

You will then see an `exports` folder folders inside of it each containing their respective activities files.

## Future Work:
Create individual export folders for values other than activity type such as distance, elapsed time, gear, etc. 
