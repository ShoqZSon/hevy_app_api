import json
import math
import os
from pathlib import Path

import requests
from difflib import get_close_matches

class Hevy:
    BASE_URL = "https://api.hevyapp.com/v1"

    def __init__(self, api_key: str, project_path: Path):
        self.headers = {
            "api-key": api_key,
            "Content-Type": "application/json"
        }
        self.project_path = project_path
        self.plans_path = project_path / "plans"

    # ---------- WORKOUTS ----------
    def get_workouts(self, page: int = 1, page_size: int = 5):
        params = {"page": page, "pageSize": page_size}
        response = requests.get(f"{self.BASE_URL}/workouts", headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_workout_by_id(self, workout_id):
        response = requests.get(f"{self.BASE_URL}/workouts/{workout_id}", headers=self.headers)
        response.raise_for_status()

        return response.json()

    def get_workouts_count(self) -> str:
        response = requests.get(f"{self.BASE_URL}/workouts/count", headers=self.headers)
        response.raise_for_status()
        count = response.json()["workout_count"]
        return count

    # ---------- ROUTINES ----------
    def get_routines(self, page: int = 1, page_size: int = 5):
        params = {"page": page, "pageSize": page_size}
        response = requests.get(f"{self.BASE_URL}/routines", headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_routine_by_id(self, routine_id):
        response = requests.get(f"{self.BASE_URL}/routines/{routine_id}", headers=self.headers)
        response.raise_for_status()

        return response.json()

    # ---------- EXERCISE TEMPLATES ----------
    def get_exercise_templates(self, page=1, page_size=5):
        params = {"page": page, "pageSize": page_size}
        response = requests.get(f"{self.BASE_URL}/exercise_templates", headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_exercise_template_by_id(self, template_id):
        response = requests.get(f"{self.BASE_URL}/exercise_templates/{template_id}", headers=self.headers)
        response.raise_for_status()

        return response.json()

    # ---------- ROUTINE FOLDERS ----------
    def get_routine_folders(self, page=1, page_size=5):
        params = {"page": page, "pageSize": page_size}
        response = requests.get(f"{self.BASE_URL}/routine_folders", headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_routine_folder_by_id(self, folder_id):
        response = requests.get(f"{self.BASE_URL}/routine_folders/{folder_id}", headers=self.headers)
        response.raise_for_status()

        return response.json()

    # ---------- WEBHOOK SUBSCRIPTION ----------
    #def create_webhook_subscription(self, data):
    #    return requests.post(f"{self.BASE_URL}/webhook-subscription", headers=self.headers, json=data).json()

    #def delete_webhook_subscription(self):
    #    return requests.delete(f"{self.BASE_URL}/webhook-subscription", headers=self.headers).json()

    #def get_webhook_subscription(self):
    #    return requests.get(f"{self.BASE_URL}/webhook-subscription", headers=self.headers).json()

    # ---------- EXERCISE HISTORY ----------
    def get_exercise_history_for(self, exercise_template_id, start_date=None, end_date=None):
        if start_date and end_date:
            params = {"exerciseTemplateId": exercise_template_id, "start_date": start_date, "end_date": end_date}
        if not start_date and not end_date:
            params = {"exerciseTemplateId": exercise_template_id}
        else:
            raise ValueError("start_date and end_date must be provided or neither at all.")
        response = requests.get(f"{self.BASE_URL}/exercise_history", headers=self.headers, params=params).json()
        response.raise_for_status()

        return response

    # ---------- Get complete data ----------
    def write_all_current_plans(self) -> None:
        """
        Returns all routines within in their respective folders.
        Specifically returns the routines (strength upper/lower, athletic upper/lower etc. in Off-Season etc.).

        Return Type: Json
        """
        plans_json = self.plans_path / "plans.json"
        # Get only 1 routine item to calculate the page_count
        routines = self.get_routines(page=1, page_size=1)
        page_count = math.ceil(routines["page_count"] / 10)
        routines["routines"] = []

        # Extract all routines
        for i in range(1, page_count + 1):
            routines_tmp = self.get_routines(page=i, page_size=10)
            routines["routines"].extend(routines_tmp["routines"])

        # Get all routine folders (Off-Season, Pre-Season, In-Season, Deload)
        folders = self.get_routine_folders(page=1, page_size=10)

        # Match routines to their respective folders
        for folder in folders["routine_folders"]:
            folder["routines"] = [r for r in routines["routines"] if r["folder_id"] == folder["id"]]

        with open(plans_json, "w") as f:
            json.dump(folders, f, indent=4)

    def write_specific_plan(self, plan_name: str):
        plans_json = self.plans_path / "plans.json"
        self.write_all_current_plans()

        with open(plans_json, "r") as f:
            plans = json.load(f)

        folders = plans["routine_folders"]
        plan_lower = plan_name.lower()

        # Compare only against the short prefix before ":"
        short_titles = [f["title"].split(":")[0].lower() for f in folders]
        matches = get_close_matches(plan_lower, short_titles, n=1, cutoff=0.3)

        if not matches:
            titles = [f["title"] for f in folders]
            raise ValueError(f"No plan found matching '{plan_name}'. Available plans: {titles}")

        matched_folder = folders[short_titles.index(matches[0])]

        path_to_specific_plan = self.plans_path / f"{plan_name}.json"
        with open(path_to_specific_plan, "w") as f:
            json.dump(matched_folder, f, indent=4)