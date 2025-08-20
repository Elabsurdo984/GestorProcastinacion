import json
from .task import Task, Priority
from datetime import datetime
from typing import List

class Storage:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        
    def save_task(self, task: Task) -> None:
        tasks = self.load_tasks()
        tasks.append(task)
        self._save_to_file(tasks)
        
    def load_tasks(self) -> List[Task]:
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                tasks = []
                for task_data in data:
                    task = Task(
                        task_data['name'],
                        task_data['description'],
                        datetime.fromisoformat(task_data['deadline']),
                        Priority[task_data['priority']]
                    )
                    task.progress = task_data['progress']
                    task.last_update = datetime.fromisoformat(task_data['last_update'])
                    tasks.append(task)
                return tasks
        except FileNotFoundError:
            return []
            
    def update_task(self, updated_task: Task) -> None:
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.name == updated_task.name:
                tasks[i] = updated_task
                break
        self._save_to_file(tasks)
        
    def _save_to_file(self, tasks: List[Task]) -> None:
        data = []
        for task in tasks:
            task_dict = {
                'name': task.name,
                'description': task.description,
                'deadline': task.deadline.isoformat(),
                'priority': task.priority.name,
                'progress': task.progress,
                'last_update': task.last_update.isoformat()
            }
            data.append(task_dict)
            
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)