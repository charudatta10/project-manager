import json
import logging
from datetime import datetime, timedelta


class ProjectManager:
    def __init__(self, json_file="project_management.json"):
        self.json_file = json_file
        self.load_data()

    def load_data(self):
        try:
            with open(self.json_file, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}
        except json.JSONDecodeError:
            logging.error("Error decoding JSON file.")
            self.data = {}
        self.save_data()

    def save_data(self):
        try:
            with open(self.json_file, "w") as file:
                json.dump(self.data, file, indent=4)
        except IOError as e:
            logging.error(f"Failed to write data to {self.json_file}: {e}")

    def initialize_project(self, project_name):
        if project_name not in self.data:
            self.data[project_name] = {
                "tasks": [],
                "time_logs": [],
            }
            self.save_data()
            logging.info(f"Project '{project_name}' initialized.")
        else:
            logging.warning(f"Project '{project_name}' already exists.")

    def add_task(self, project_name, task_name, due_date=None, tags=None):
        task = {
            "task_name": task_name,
            "status": "TODO",
            "created_at": datetime.now().isoformat(),
            "due_date": due_date,
            "tags": tags or [],
            "time_logs": [],
        }
        self.data[project_name]["tasks"].append(task)
        self.save_data()

    def edit_task(self, project_name, task_name, **updates):
        for task in self.data[project_name]["tasks"]:
            if task["task_name"] == task_name:
                task.update(updates)
                self.save_data()
                return
        logging.warning(f"Task '{task_name}' not found in project '{project_name}'.")

    def view_tasks(self, project_name, status=None):
        tasks = self.data[project_name]["tasks"]
        if status:
            tasks = [task for task in tasks if task["status"] == status]
        return tasks

    def delete_task(self, project_name, task_name):
        self.data[project_name]["tasks"] = [
            task
            for task in self.data[project_name]["tasks"]
            if task["task_name"] != task_name
        ]
        self.save_data()

    def log_time(self, project_name, task_name, hours, tags=None):
        time_log = {
            "task_name": task_name,
            "hours": hours,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat(),
        }

        if project_name not in self.data:
            self.initialize_project(project_name)
            logging.info(f"Project '{project_name}' initialized.")

        task_exists = False
        for task in self.data[project_name]["tasks"]:
            if task["task_name"] == task_name:
                task_exists = True
                task["time_logs"].append(time_log)
                break

        if not task_exists:
            self.add_task(project_name, task_name)
            for task in self.data[project_name]["tasks"]:
                if task["task_name"] == task_name:
                    task["time_logs"].append(time_log)
                    break

        self.data[project_name]["time_logs"].append(time_log)
        self.save_data()
        logging.info(f"Time logged for task '{task_name}' in project '{project_name}'.")

    def categorize_task(self, project_name, task_name, status):
        if status in ["TODO", "DOING", "DONE"]:
            for task in self.data[project_name]["tasks"]:
                if task["task_name"] == task_name:
                    task["status"] = status
                    self.save_data()
                    return
            logging.warning(
                f"Task '{task_name}' not found in project '{project_name}'."
            )

    def add_tag_to_task(self, project_name, task_name, tag):
        for task in self.data[project_name]["tasks"]:
            if task["task_name"] == task_name:
                if tag not in task["tags"]:
                    task["tags"].append(tag)
                    self.save_data()
                return
        logging.warning(f"Task '{task_name}' not found in project '{project_name}'.")

    def add_repeating_task(
        self, project_name, task_name, interval_days, due_date=None, tags=None
    ):
        self.add_task(project_name, task_name, due_date, tags)
        next_due_date = datetime.strptime(due_date, "%Y-%m-%d") + timedelta(
            days=interval_days
        )
        self.add_task(
            project_name,
            f"{task_name} (repeat)",
            next_due_date.strftime("%Y-%m-%d"),
            tags,
        )

    def query_tasks(self, project_name, status=None, due_date=None, overdue=None):
        filtered_tasks = self.data[project_name]["tasks"]

        if status:
            filtered_tasks = [
                task for task in filtered_tasks if task["status"] == status
            ]

        if due_date:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
            filtered_tasks = [
                task
                for task in filtered_tasks
                if task["due_date"]
                and datetime.strptime(task["due_date"], "%Y-%m-%d") == due_date_obj
            ]

        if overdue:
            current_date = datetime.now()
            filtered_tasks = [
                task
                for task in filtered_tasks
                if task["due_date"]
                and datetime.strptime(task["due_date"], "%Y-%m-%d") < current_date
            ]

        return filtered_tasks


# Setting up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Example Usage
if __name__ == "__main__":
    manager = ProjectManager()
    manager.initialize_project("MyProject")
    manager.add_task("MyProject", "Initial Task", "2023-10-01", ["important", "urgent"])
    manager.edit_task("MyProject", "Initial Task", status="DOING")
    manager.log_time("MyProject", "Initial Task", 2, ["development"])
    tasks = manager.view_tasks("MyProject", "DOING")
    print(tasks)
    manager.categorize_task("MyProject", "Initial Task", "DONE")
    manager.add_tag_to_task("MyProject", "Initial Task", "completed")
    manager.add_repeating_task("MyProject", "Daily Standup", 1, "2023-10-02")
    manager.delete_task("MyProject", "Initial Task")
