import csv
import copy
import time
from typing import Any, cast
import os

import srcomapi
import srcomapi.datatypes as DataType

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    print("error: API_KEY environment variable is not set")
    exit(0)


api = srcomapi.SpeedrunCom(API_KEY, debug=1)
PC = cast(dict[str, str], api.get("platforms/pc"))["id"]
GAME = api.get_game("Trailmakers")

LEAGUES = [
    "bionic league",
    "gokart league",
    "muscle league",
    "formula league",
    "jet league",
    "super sonic league",
    "space league",
]


def get_category(name: str) -> DataType.Category:
    categories: list[DataType.Category] = GAME.categories
    return next(x for x in categories if x.data["name"] == name)


def get_runs(name: str) -> list[dict[str, Any]]:
    with open(f"{name}.csv", "r", newline="", encoding="UTF-8") as f:
        contents = list(csv.reader(f))
    header, data = contents[0], contents[1:]
    res = []
    for run in data:
        run_dict: dict[str, Any] = {header[i]: run[i] for i in range(3)}
        variables = {header[i]: run[i] for i in range(3, len(run))}
        run_dict["variables"] = variables
        res.append(run_dict)
        if league := variables.get("league"):
            league_idx = LEAGUES.index(league)
            for league in LEAGUES[league_idx + 1 :]:
                run = copy.deepcopy(run_dict)
                run["variables"]["league"] = league
                res.append(run)
    return res


def submit_runs(category_name: str):
    CATEGORY = get_category(category_name)
    variables_map: dict[str, Any] = {}
    for var in cast(list[DataType.Variable], CATEGORY.variables):
        values: dict[str, dict[str, Any]] = var.data["values"]["values"]
        values_map = {val["label"]: id for id, val in values.items()}
        variables_map[var.data["name"]] = {"id": var.data["id"], "values": values_map}

    runs = get_runs(category_name)
    for run in runs:
        variables = {}
        for name, val in run["variables"].items():
            var_map = variables_map[name.lower()]
            variables[var_map["id"]] = {
                "type": "pre-defined",
                "value": var_map["values"][val.lower()],
            }
        run["variables"] = variables
        run["time"] = float(run["time"])
    print(f"Runs to submit: {len(runs)}")
    for run in runs:
        print(run)
        api.submit_run(
            category=CATEGORY.id,
            platform=PC,  # type: ignore
            times={"realtime": run["time"]},  # type: ignore
            date=run["date"],
            video=run["video"],
            variables=run["variables"],
            # verified=True # Auto-verify run, requires using a moderator's API key
        )
        time.sleep(2)


if __name__ == "__main__":
    submit_runs("race island")
    submit_runs("rally")
