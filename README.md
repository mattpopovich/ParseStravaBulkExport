# ParseStravaBulkExport

#### The Problem:
Strava will let you export all your activities just fine, but it is up to you to find out which activities correspond to biking vs. running, etc. Thankfully, they give you a nice `activities.csv` file telling you some details for each file in the `activities` folder.

#### The Solution:
Parse that `activities.csv` file to pull out the activities we want based on certain parameters.

## Use
Enter the Dockerfile, then
```console
$ python main.py
```
