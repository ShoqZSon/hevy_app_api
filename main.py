import os
from Hevy import Hevy
from utils import *

PROJECT_PATH = Path.cwd()

CONFIG_PATH = PROJECT_PATH / "config.toml"
config = read_toml(CONFIG_PATH)
plan_folder = PROJECT_PATH / "plans"

if not plan_folder.exists():
    os.mkdir(plan_folder)

key_dict = config.get("Hevy_API_Key", {})
api_key = key_dict.get("api_key")
if api_key is None:
    print("API key not found in config.toml")
    exit(1)

hevy = Hevy(api_key=api_key, project_path=PROJECT_PATH)

#workouts_count = hevy.get_workouts_count()
#print(f"Workout Count: {workouts_count}")


# Writes the whole trainingsplan into a file called plans.json
hevy.write_all_current_plans()
hevy.write_specific_plan("Off-Season")
hevy.write_specific_plan("Pre-Season")
hevy.write_specific_plan("In-Season")
hevy.write_specific_plan("Deload")