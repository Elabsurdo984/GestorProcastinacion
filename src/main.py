from datetime import datetime, timedelta
from .task import Task, Priority
from .storage import Storage
from .category_manager import CategoryManager
from .ui import ConsoleUI

class ProcrastinationManager:
    def __init__(self):
        self.storage = Storage()
        self.tasks = self.storage.load_tasks()
        self.category_manager = CategoryManager()
        self.procrastination_threshold = timedelta(seconds=5)
        
        for task in self.tasks:
            if task.category not in self.category_manager.get_categories():
                self.category_manager.add_category(task.category)

    def add_task(self, name, description, deadline_str, priority_choice, category):
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD.")
        
        if category not in self.category_manager.get_categories():
            self.category_manager.add_category(category)
            
        priority_map = {"1": Priority.BAJA, "2": Priority.MEDIA, "3": Priority.ALTA}
        priority = priority_map.get(priority_choice, Priority.MEDIA)
        
        task = Task(name, description, deadline, priority, category)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)

    def get_tasks(self, sort_by_priority=True):
        return sorted(self.tasks, key=lambda x: (x.completed, x.priority.value), reverse=True) if sort_by_priority else self.tasks

    def get_priority_tasks(self, priority):
        return [task for task in self.tasks if task.priority == priority and not task.completed]

    def get_category_tasks(self, category):
        return [t for t in self.tasks if t.category == category]

    def check_procrastination(self):
        now = datetime.now()
        procrastinated_tasks = []
        for priority in [Priority.ALTA, Priority.MEDIA, Priority.BAJA]:
            priority_tasks = self.get_priority_tasks(priority)
            for task in priority_tasks:
                if not task.last_update or (now - task.last_update) > self.procrastination_threshold:
                    procrastinated_tasks.append(task)
        return procrastinated_tasks

    def update_task_progress(self, task, new_progress):
        task.update_progress(new_progress)
        self.storage.save_tasks(self.tasks)

    def complete_task(self, task):
        task.completed = True
        task.last_update = datetime.now()
        self.storage.save_tasks(self.tasks)

    def edit_task(self, task, new_name, new_description, new_deadline_str, new_priority_choice, new_category):
        try:
            new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD.")

        if new_category not in self.category_manager.get_categories():
            self.category_manager.add_category(new_category)

        priority_map = {"1": Priority.BAJA, "2": Priority.MEDIA, "3": Priority.ALTA}
        new_priority = priority_map.get(new_priority_choice, task.priority)

        task.name = new_name
        task.description = new_description
        task.deadline = new_deadline
        task.priority = new_priority
        task.category = new_category
        task.last_update = datetime.now()
        
        self.storage.save_tasks(self.tasks)

    def delete_task(self, task):
        self.tasks.remove(task)
        self.storage.save_tasks(self.tasks)

def main():
    manager = ProcrastinationManager()
    ui = ConsoleUI(manager)
    ui.run()

if __name__ == "__main__":
    main()
