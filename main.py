from Hevy import Hevy
from pathlib import Path

plan_folder = Path.cwd() / "plans"

hevy = Hevy()

#workouts_count = hevy.get_workouts_count()
#print(f"Workout Count: {workouts_count}")


# Writes the whole trainingsplan into a file called plans.json
hevy.write_all_current_plans()
hevy.write_specific_plan("Off-Season")
hevy.write_specific_plan("Pre-Season")
hevy.write_specific_plan("In-Season")
hevy.write_specific_plan("Deload")