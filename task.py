from datetime import datetime
import json

class Task:
    def __init__(self, name, description, deadline):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.last_progress = None
        self.completed = False

    def to_dict(self):
        """Convierte la tarea a un diccionario para serialización JSON"""
        return {
            'name': self.name,
            'description': self.description,
            'deadline': self.deadline,
            'last_progress': self.last_progress.isoformat() if self.last_progress else None,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data):
        """Crea una tarea desde un diccionario"""
        task = Task(data['name'], data['description'], data['deadline'])
        task.last_progress = datetime.fromisoformat(data['last_progress']) if data['last_progress'] else None
        task.completed = data['completed']
        return task

    def update_progress(self):
        """Registra un nuevo progreso en la tarea"""
        self.last_progress = datetime.now()