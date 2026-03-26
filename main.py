from Hevy import Hevy
from utils import *

PROJECT_PATH = Path.cwd()
CONFIG_PATH = PROJECT_PATH / "config.toml"
config = read_toml(CONFIG_PATH)

key_dict = config.get("Hevy_API_Key", {})
api_key = key_dict.get("api_key")

hevy = Hevy(api_key=api_key)

#workouts_count = hevy.get_workouts_count()
#print(f"Workout Count: {workouts_count}")

routines = hevy.get_routines(page=1, page_size=1)
page_count = int((routines["page_count"]/10) + 1)
routines["routines"] = []

for i in range(1, page_count + 1):
    routines_tmp = hevy.get_routines(page=i, page_size=10)
    for j in range(len(routines_tmp["routines"])):
        routines["routines"].append(routines_tmp["routines"][j])
        #print(routines["routines"][j])

routines_tmp = None

folders = hevy.get_routine_folders(page=1,page_size=10)
folder_count = len(folders["routine_folders"])

# Appends empty arrays as placeholder for the routines
for folder in folders["routine_folders"]:
    folder["routines"] = []

# Appends the routines into the array and matches the folder_id within routines
for folder in folders["routine_folders"]:
    folder_id = folder["id"]
    for routine in routines["routines"]:
        if routine["folder_id"] == folder_id:
            folder["routines"].append(routine)

# Writes the whole trainingsplan into a file
with open("trainingsplan.json", "w") as f:
    json.dump(folders, f, indent=4)
