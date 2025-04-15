# Trailmakers SpeedRunCom Race Upload

This script automates submitting runs to the official race leaderboards in [speedrun.com](https://www.speedrun.com/trailmakers),
uploading runs to all qualifying power core leagues

## Pre-requisites

You need to obtain an API key for [speedrun.com](speedrun). You can obtain it by
going to your profile -> API key -> show API key.

## Usage

1. Clone the repository
2. Add the runs to submit to the `race island.csv` and/or `rally.csv` files.
   For the power core league, specify the league with the least amount of
   power cores allowed that your run qualifies for.
3. Run `API_KEY=<your API key> python3 upload_runs.py`
