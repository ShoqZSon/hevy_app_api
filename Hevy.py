import requests

class Hevy:
    BASE_URL = "https://api.hevyapp.com/v1"

    def __init__(self, api_key: str):
        self.headers = {
            "api-key": api_key,
            "Content-Type": "application/json"
        }

    # ---------- WORKOUTS ----------
    def get_workouts(self, page: int = 1, page_size: int = 5):
        params = {"page": page, "pageSize": page_size}
        response = requests.get(f"{self.BASE_URL}/workouts", headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    #def create_workout(self, data):
    #    return requests.post(f"{self.BASE_URL}/workouts", headers=self.headers, json=data).json()

    def get_workouts_count(self):
        return requests.get(f"{self.BASE_URL}/workouts/count", headers=self.headers).json()

    #def get_workout_events(self, params=None):
    #    return requests.get(f"{self.BASE_URL}/workouts/events", headers=self.headers, params=params).json()

    def get_workout(self, workout_id):
        return requests.get(f"{self.BASE_URL}/workouts/{workout_id}", headers=self.headers).json()

    #def update_workout(self, workout_id, data):
    #    return requests.put(f"{self.BASE_URL}/workouts/{workout_id}", headers=self.headers, json=data).json()

    # ---------- ROUTINES ----------
    def get_routines(self, page: int = 1, page_size: int = 5):
        params = {"page": page, "pageSize": page_size}
        response = requests.get(f"{self.BASE_URL}/routines", headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    #def create_routine(self, data):
    #    return requests.post(f"{self.BASE_URL}/routines", headers=self.headers, json=data).json()

    def get_routine(self, routine_id):
        return requests.get(f"{self.BASE_URL}/routines/{routine_id}", headers=self.headers).json()

    #def update_routine(self, routine_id, data):
    #    return requests.put(f"{self.BASE_URL}/routines/{routine_id}", headers=self.headers, json=data).json()

    # ---------- EXERCISE TEMPLATES ----------
    def get_exercise_templates(self, page=1, page_size=5):
        params = {"page": page, "pageSize": page_size}
        response = requests.get(f"{self.BASE_URL}/exercise_templates", headers=self.headers, params=params).json()
        response.raise_for_status()

        return response

    #def create_exercise_template(self, data):
    #    return requests.post(f"{self.BASE_URL}/exercise_templates", headers=self.headers, json=data).json()

    def get_exercise_template(self, template_id):
        return requests.get(f"{self.BASE_URL}/exercise_templates/{template_id}", headers=self.headers).json()

    # ---------- ROUTINE FOLDERS ----------
    def get_routine_folders(self, page=1, page_size=5):
        params = {"page": page, "pageSize": page_size}
        response = requests.get(f"{self.BASE_URL}/routine_folders", headers=self.headers, params=params).json()
        response.raise_for_status()

        return response

    #def create_routine_folder(self, data):
    #    return requests.post(f"{self.BASE_URL}/routine_folders", headers=self.headers, json=data).json()

    def get_routine_folder(self, folder_id):
        return requests.get(f"{self.BASE_URL}/routine_folders/{folder_id}", headers=self.headers).json()

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
