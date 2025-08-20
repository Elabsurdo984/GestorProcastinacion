from enum import Enum
from datetime import datetime
import json

class Priority(Enum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3

    @staticmethod
    def from_string(priority_str):
        priority_map = {
            'baja': Priority.BAJA,
            'media': Priority.MEDIA,
            'alta': Priority.ALTA
        }
        return priority_map.get(priority_str.lower(), Priority.MEDIA)

class Task:
    def __init__(self, name, description, deadline, priority=Priority.MEDIA):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.last_progress = None
        self.completed = False

    def to_dict(self):
        """Convierte la tarea a un diccionario para serialización JSON"""
        return {
            'name': self.name,
            'description': self.description,
            'deadline': self.deadline,
            'priority': self.priority.name,
            'last_progress': self.last_progress.isoformat() if self.last_progress else None,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data):
        """Crea una tarea desde un diccionario"""
        task = Task(
            data['name'], 
            data['description'], 
            data['deadline'],
            Priority.from_string(data.get('priority', 'MEDIA'))
        )
        task.last_progress = datetime.fromisoformat(data['last_progress']) if data['last_progress'] else None
        task.completed = data['completed']
        return task

    def update_progress(self):
        """Registra un nuevo progreso en la tarea"""
        self.last_progress = datetime.now()