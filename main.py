from Hevy import Hevy
from utils import *

PROJECT_PATH = Path.cwd()
CONFIG_PATH = PROJECT_PATH / "config.toml"

config = read_toml(CONFIG_PATH)

key_dict = config.get("Hevy_API_Key", {})
api_key = key_dict.get("api_key")

hevy = Hevy(api_key=api_key)

print(hevy)

# List workouts
workouts = hevy.get_workouts()
pretty_print_json(workouts)

routines = hevy.get_routines()
pretty_print_json(routines)

workouts_count = hevy.get_workouts_count()
pretty_print_json(workouts_count)

# Get one workout
#workout = hevy.get_workout("Chest")

# Create new routine
#new_routine = hevy.create_routine({"name": "Push Day", "exercises": [...]})
