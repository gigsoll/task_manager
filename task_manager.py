import datetime
import json
import os
from dataclasses import asdict

from platformdirs import user_cache_dir

from task import Task


class TaskManager:
    def __init__(self):
        self.cache_dir = user_cache_dir("task_manager", "<gigsoll>")
        self.task_file = "tasks.json"

        if not os.path.exists(self.cache_dir): 
            os.makedirs(self.cache_dir)

        if not os.path.exists(os.path.join(self.cache_dir, self.task_file)): 
            f = open(os.path.join(self.cache_dir, self.task_file), "w")
            f.write("[]")
            f.close()

        self.tasks = self.read_tasks()

    def read_tasks(self):
        with open(os.path.join(self.cache_dir, self.task_file)) as data:
            try:
                tasks = json.load(data)
            except(json.decoder.JSONDecodeError):
                tasks = []
            task_list = []
            for task in tasks:
                try:
                    task_list.append(
                        Task(description=task["description"], 
                             status=task["status"], 
                             createdAt=task["createdAt"], 
                             updatedAt=task["updatedAt"]))
                except TypeError:
                    print(f"Wrong task, {task}")
            return task_list
        
        task_list_dict = {}
        task: dict
        for task in task_list:
            task_list_dict["id"] = {key: value for key, value in task.items() if key != "id"}
        print(task_list_dict)
            
    def save_tasks(self):
        dict_version = []
        for task in self.tasks:
            dict_version.append(asdict(task))
        json_data = json.dumps(dict_version, indent=4)
        with open(os.path.join(self.cache_dir, self.task_file), "w") as data:
            data.write(json_data)

    def add(self, task_description):
        new_task = Task(task_description)
        print(f"Task \"{new_task.description}\" with id {new_task.id} was created")
        self.tasks.append(new_task)
        self.save_tasks()
        
    def delete(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                print(f"Task with id {task.id} was removed")
                break
        self.save_tasks()

    def update_description(self, task_id, new_description):
        for task in self.tasks:
            if task.id == task_id:
                task.description = new_description
                task.updatedAt = datetime.date.today().strftime("%Y-%m-%d")
                print(f"Task with id {task.id} was updated")
                break
        self.save_tasks()

    def change_status(self, task_id, new_status):
        if new_status not in ["done", "in-progress", "todo"]:
            raise ValueError("task status should be done or in-progress")
        
        for task in self.tasks:
            if task.id == task_id:
                task.status = new_status
                task.updatedAt = datetime.date.today().strftime("%Y-%m-%d")
                print(f"Task with id {task.id} was updated")
                break
        self.save_tasks()

    def list_task(self, status):
        if status not in ["done", "todo", "in-progress", "all"]:
            raise ValueError("status should be in [done, todo, in-progress, all]")
        for task in self.tasks:
            if status != "all" and task.status == status:
                print(task, end="\n")
            elif status == "all":
                print(task, end="\n")

def main():
    print("it is a class it not supose to be runned as script")

if __name__ == "__main__":
    main()

