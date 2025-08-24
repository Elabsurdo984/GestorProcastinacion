"""Manages tasks and categories for the Procrastination Manager application."""
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict

from src.models.task import Task, Priority
from src.data.storage import Storage
from src.data.category_manager import CategoryManager

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class ProcrastinationManager:
    """
    Manages the creation, retrieval, updating, and deletion of tasks.
    Also handles category management and procrastination checks.
    """
    PRIORITY_MAP: Dict[str, Priority] = {"1": Priority.BAJA, "2": Priority.MEDIA, "3": Priority.ALTA}

    def __init__(self) -> None:
        """Initializes the ProcrastinationManager with storage and category manager."""
        self.storage = Storage()
        self.tasks: List[Task] = self.storage.load_tasks()
        self.category_manager = CategoryManager()
        self.procrastination_threshold: timedelta = timedelta(seconds=5) # pylint: disable=line-too-long

        for task in self.tasks:
            if task.category not in self.category_manager.get_categories():
                self.category_manager.add_category(task.category)

    def _validate_deadline(self, deadline_str: str) -> datetime:
        """
        Validates and converts a deadline string to a datetime object.

        Args:
            deadline_str (str): The deadline string in "YYYY-MM-DD" format.

        Returns:
            datetime: The validated datetime object.

        Raises:
            ValueError: If the date format is invalid.
        """
        try:
            return datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD.") from exc # pylint: disable=line-too-long

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def add_task(self, name: str, description: str, deadline_str: str,
                 priority_choice: str, category: str) -> None:
        """
        Adds a new task to the manager.

        Args:
            name (str): The name of the task.
            description (str): The description of the task.
            deadline_str (str): The deadline of the task in "YYYY-MM-DD" format.
            priority_choice (str): The priority choice (e.g., "1", "2", "3").
            category (str): The category of the task.
        """
        deadline = self._validate_deadline(deadline_str)

        if category not in self.category_manager.get_categories():
            self.category_manager.add_category(category)

        priority = self.PRIORITY_MAP.get(priority_choice, Priority.MEDIA)

        task = Task(name, description, deadline, priority, category)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)

    def get_tasks(self, sort_by_priority: bool = True) -> List[Task]:
        """
        Retrieves a list of tasks, optionally sorted by priority.

        Args:
            sort_by_priority (bool): If True, tasks are sorted by completion status and priority.

        Returns:
            List[Task]: A list of tasks.
        """
        return sorted(self.tasks, key=lambda x: (x.completed, x.priority.value), # pylint: disable=line-too-long
                      reverse=True) if sort_by_priority else self.tasks

    def get_priority_tasks(self, priority: Priority) -> List[Task]:
        """
        Retrieves tasks filtered by a specific priority.

        Args:
            priority (Priority): The priority to filter by.

        Returns:
            List[Task]: A list of tasks with the specified priority that are not completed.
        """
        return [task for task in self.tasks if task.priority == priority and not task.completed]

    def get_category_tasks(self, category: str) -> List[Task]:
        """
        Retrieves tasks filtered by a specific category.

        Args:
            category (str): The category to filter by.

        Returns:
            List[Task]: A list of tasks belonging to the specified category.
        """
        return [t for t in self.tasks if t.category == category]

    def check_procrastination(self) -> List[Task]:
        """
        Checks for tasks that are considered procrastinated.

        Returns:
            List[Task]: A list of procrastinated tasks.
        """
        now = datetime.now()
        procrastinated_tasks: List[Task] = []
        for task in self.tasks:
            if not task.completed and (not task.last_update or
                                       (now - task.last_update) > self.procrastination_threshold):
                procrastinated_tasks.append(task)
        return procrastinated_tasks

    def update_task_progress(self, task: Task, new_progress: int) -> None:
        """
        Updates the progress of a given task.

        Args:
            task (Task): The task to update.
            new_progress (int): The new progress percentage.
        """
        task.update_progress(new_progress)
        self.storage.save_tasks(self.tasks)

    def complete_task(self, task: Task) -> None:
        """
        Marks a task as completed.

        Args:
            task (Task): The task to mark as completed.
        """
        task.completed = True
        task.last_update = datetime.now()
        self.storage.save_tasks(self.tasks)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def edit_task(self, task: Task, new_name: str, new_description: str, new_deadline_str: str,
                  new_priority_choice: str, new_category: str) -> None:
        """
        Edits an existing task with new details.

        Args:
            task (Task): The task to edit.
            new_name (str): The new name for the task.
            new_description (str): The new description for the task.
            new_deadline_str (str): The new deadline string in "YYYY-MM-DD" format.
            new_priority_choice (str): The new priority choice.
            new_category (str): The new category for the task.
        """
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
        """
        Deletes a task from the manager.

        Args:
            task (Task): The task to delete.
        """
        self.tasks.remove(task)
        self.storage.save_tasks(self.tasks)
