# ParseStravaBulkExport

![Python badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/mattpopovich/ParseStravaBulkExport)

### The Problem:
Strava will let you export all your activities just fine, but it is up to you to find out which activities correspond to biking vs. running, etc. Thankfully, they give you a nice `activities.csv` file telling you some details for each file in the `activities` folder.

### The Solution:
Parse that `activities.csv` file to pull out the activities we want based on certain parameters.

## Use
Modify the `STRAVA_EXPORTED_FOLDER_PATH` variable in `config.cfg` to point to your **unzipped** [Strava Bulk Export](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#h_01GG58HC4F1BGQ9PQZZVANN6WF) folder.

On a computer that has Python installed:
```console
$ python main.py 
Parsing the strava_export_12345678/activities.csv file...
Copied 14 files to the exports/Alpine Ski folder
Copied 181 files to the exports/E-Bike Ride folder
Copied 1 files to the exports/Golf folder
Copied 36 files to the exports/Hike folder
Copied 1 files to the exports/Ice Skate folder
Copied 20 files to the exports/Inline Skate folder
Copied 13 files to the exports/Kayaking folder
Copied 6 files to the exports/Kitesurf folder
Copied 261 files to the exports/Ride folder
Copied 98 files to the exports/Run folder
Copied 56 files to the exports/Snowboard folder
Copied 1 files to the exports/Stand Up Paddling folder
Copied 11 files to the exports/Swim folder
Copied 145 files to the exports/Velomobile folder
Copied 1 files to the exports/Virtual Ride folder
Copied 6 files to the exports/Walk folder
Complete!
```

You will then see an `exports` folder with folders inside of it each containing their respective activities files.

## Future Work:
Create individual export folders for values other than activity type such as distance, elapsed time, gear, etc. 
