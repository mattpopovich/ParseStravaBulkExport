# ParseStravaBulkExport

#### The Problem:
Strava will let you export all your activities just fine, but it is up to you to find out which activities correspond to biking vs. running, etc. Thankfully, they give you a nice `activities.csv` file telling you some details for each file in the `activities` folder.

#### The Solution:
Parse that `activities.csv` file to pull out the activities we want based on certain parameters.

## Use
Modify the `STRAVA_EXPORTED_FOLDER_PATH` variable in `config.cfg` to point to your **unzipped** [Strava Bulk Export](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#h_01GG58HC4F1BGQ9PQZZVANN6WF) folder.

Enter the Dockerfile, then
```console
$ python main.py
```

You will then see an `exports` folder with a `Run` folder inside it containing all your running workouts.

## Future Work:
Create individual export folders for values other than activity type such as distance, elapsed time, gear, etc. 
