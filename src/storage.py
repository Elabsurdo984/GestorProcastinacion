import json
from task import Task

class TaskStorage:
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def save_tasks(self, tasks):
        """Guarda la lista de tareas en un archivo JSON"""
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)

    def load_tasks(self):
        """Carga las tareas desde el archivo JSON"""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(task_dict) for task_dict in data]
        except FileNotFoundError:
            return []