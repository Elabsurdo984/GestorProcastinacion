import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.task import Task, Priority
from src.data.storage import Storage
from src.data.category_manager import CategoryManager

class ProcrastinationManager:
    PRIORITY_MAP: Dict[str, Priority] = {"1": Priority.BAJA, "2": Priority.MEDIA, "3": Priority.ALTA}

    def __init__(self) -> None:
        self.storage = Storage()
        self.tasks: List[Task] = self.storage.load_tasks()
        self.category_manager = CategoryManager()
        self.procrastination_threshold: timedelta = timedelta(seconds=5)
        
        for task in self.tasks:
            if task.category not in self.category_manager.get_categories():
                self.category_manager.add_category(task.category)

    def _validate_deadline(self, deadline_str: str) -> datetime:
        try:
            return datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD.")

    def add_task(self, name: str, description: str, deadline_str: str, priority_choice: str, category: str) -> None:
        deadline = self._validate_deadline(deadline_str)
        
        if category not in self.category_manager.get_categories():
            self.category_manager.add_category(category)
            
        priority = self.PRIORITY_MAP.get(priority_choice, Priority.MEDIA)
        
        task = Task(name, description, deadline, priority, category)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)

    def get_tasks(self, sort_by_priority: bool = True) -> List[Task]:
        return sorted(self.tasks, key=lambda x: (x.completed, x.priority.value), reverse=True) if sort_by_priority else self.tasks

    def get_priority_tasks(self, priority: Priority) -> List[Task]:
        return [task for task in self.tasks if task.priority == priority and not task.completed]

    def get_category_tasks(self, category: str) -> List[Task]:
        return [t for t in self.tasks if t.category == category]

    def check_procrastination(self) -> List[Task]:
        now = datetime.now()
        procrastinated_tasks: List[Task] = []
        for task in self.tasks:
            if not task.completed and (not task.last_update or (now - task.last_update) > self.procrastination_threshold):
                procrastinated_tasks.append(task)
        return procrastinated_tasks

    def update_task_progress(self, task: Task, new_progress: int) -> None:
        task.update_progress(new_progress)
        self.storage.save_tasks(self.tasks)

    def complete_task(self, task: Task) -> None:
        task.completed = True
        task.last_update = datetime.now()
        self.storage.save_tasks(self.tasks)

    def edit_task(self, task: Task, new_name: str, new_description: str, new_deadline_str: str, new_priority_choice: str, new_category: str) -> None:
        new_deadline = self._validate_deadline(new_deadline_str)

        if new_category not in self.category_manager.get_categories():
            self.category_manager.add_category(new_category)

        new_priority = self.PRIORITY_MAP.get(new_priority_choice, task.priority)

        task.name = new_name
        task.description = new_description
        task.deadline = new_deadline
        task.priority = new_priority
        task.category = new_category
        task.last_update = datetime.now()
        
        self.storage.save_tasks(self.tasks)

    def delete_task(self, task: Task) -> None:
        self.tasks.remove(task)
        self.storage.save_tasks(self.tasks)
