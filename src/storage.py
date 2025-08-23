"""Módulo para la persistencia de datos de tareas."""
import json
from datetime import datetime
from typing import List, Dict, Any
from .task import Task, Priority

class Storage:
    """Clase que maneja el almacenamiento persistente de tareas."""

    def __init__(self, filename: str = "tasks.json") -> None:
        """
        Inicializa el sistema de almacenamiento.

        Args:
            filename: Nombre del archivo para guardar las tareas
        """
        self.filename = filename

    def load_tasks(self) -> List[Task]:
        """
        Carga las tareas desde el archivo.

        Returns:
            List[Task]: Lista de tareas almacenadas
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                tasks = []
                for task_data in data:
                    task = self._create_task_from_dict(task_data)
                    tasks.append(task)
                return tasks
        except FileNotFoundError:
            return []

    def save_task(self, task: Task) -> None:
        """
        Guarda una nueva tarea.

        Args:
            task: Tarea a guardar
        """
        tasks = self.load_tasks()
        tasks.append(task)
        self._save_to_file(tasks)

    def _create_task_from_dict(self, data: Dict[str, Any]) -> Task:
        """
        Crea una tarea desde un diccionario.

        Args:
            data: Diccionario con datos de la tarea

        Returns:
            Task: Nueva instancia de tarea
        """
        task = Task(
            data['name'],
            data['description'],
            datetime.fromisoformat(data['deadline']),
            Priority[data['priority']],
            data.get('category', 'General')
        )
        task.progress = data['progress']
        task.last_update = datetime.fromisoformat(data['last_update'])
        task.completed = data.get('completed', False)
        return task

    def update_task(self, updated_task: Task) -> None:
        """
        Actualiza una tarea existente.

        Args:
            updated_task: Tarea con la información actualizada
        """
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.name == updated_task.name:
                tasks[i] = updated_task
                break
        self._save_to_file(tasks)

    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Guarda todas las tareas en el archivo.

        Args:
            tasks: Lista de tareas a guardar
        """
        self._save_to_file(tasks)

    def _save_to_file(self, tasks: List[Task]) -> None:
        """
        Guarda las tareas en el archivo.

        Args:
            tasks: Lista de tareas a guardar
        """
        data = []
        for task in tasks:
            task_dict = {
                'name': task.name,
                'description': task.description,
                'deadline': task.deadline.isoformat(),
                'priority': task.priority.name,
                'progress': task.progress,
                'last_update': task.last_update.isoformat(),
                'category': task.category,
                'completed': task.completed
            }
            data.append(task_dict)

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
