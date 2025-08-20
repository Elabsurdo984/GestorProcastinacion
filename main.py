from datetime import datetime, timedelta
import os
import sys
from task import Task, Priority
from storage import TaskStorage
from colorama import init, Fore, Style
from category_manager import CategoryManager

init()  # Inicializar colorama

class ProcrastinationManager:
    def __init__(self):
        self.storage = TaskStorage()
        self.tasks = self.storage.load_tasks()
        self.category_manager = CategoryManager()
        self.procrastination_threshold = timedelta(hours=24)
        
        # Cargar categorías existentes de las tareas
        for task in self.tasks:
            self.category_manager.add_category(task.category)

    def add_task(self):
        """Añade una nueva tarea con categoría"""
        name = input("Nombre de la tarea: ")
        description = input("Descripción: ")
        deadline = input("Fecha límite (YYYY-MM-DD): ")
        
        # Mostrar prioridades
        print("\nPrioridad:")
        print("1. Baja")
        print("2. Media")
        print("3. Alta")
        priority_choice = input("Seleccione la prioridad (1-3) [2]: ").strip() or "2"
        
        # Mostrar categorías
        categories = self.category_manager.get_categories()
        print("\nCategorías disponibles:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print(f"{len(categories) + 1}. Nueva categoría")
        
        cat_choice = input("\nSeleccione una categoría o cree una nueva: ")
        
        try:
            if int(cat_choice) == len(categories) + 1:
                category = input("Nombre de la nueva categoría: ")
                self.category_manager.add_category(category)
            else:
                category = categories[int(cat_choice) - 1]
        except (ValueError, IndexError):
            category = "General"
            
        priority_map = {"1": Priority.BAJA, "2": Priority.MEDIA, "3": Priority.ALTA}
        priority = priority_map.get(priority_choice, Priority.MEDIA)
        
        task = Task(name, description, deadline, priority, category)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        print(f"{Fore.GREEN}¡Tarea añadida con éxito!{Style.RESET_ALL}")

    def list_tasks(self, sort_by_priority=True):
        """Muestra todas las tareas, opcionalmente ordenadas por prioridad"""
        if not self.tasks:
            print("No hay tareas pendientes.")
            return

        tasks_to_show = sorted(self.tasks, key=lambda x: (x.completed, x.priority.value), reverse=True) if sort_by_priority else self.tasks

        for i, task in enumerate(tasks_to_show, 1):
            priority_colors = {
                Priority.ALTA: Fore.RED,
                Priority.MEDIA: Fore.YELLOW,
                Priority.BAJA: Fore.GREEN
            }
            color = priority_colors[task.priority]
            status = "Completada" if task.completed else "Pendiente"
            last_progress = task.last_progress.strftime("%Y-%m-%d %H:%M") if task.last_progress else "Sin progreso"
            
            print(f"\n{color}{i}. {task.name} [{task.priority.name}]{Style.RESET_ALL}")
            print(f"   Descripción: {task.description}")
            print(f"   Fecha límite: {task.deadline}")
            print(f"   Estado: {status}")
            print(f"   Último progreso: {last_progress}")

    def get_priority_tasks(self, priority):
        """Obtiene todas las tareas de una prioridad específica"""
        return [task for task in self.tasks if task.priority == priority and not task.completed]

    def check_procrastination(self):
        """Revisa las tareas para detectar procrastinación, priorizando tareas importantes"""
        now = datetime.now()
        for priority in [Priority.ALTA, Priority.MEDIA, Priority.BAJA]:
            priority_tasks = self.get_priority_tasks(priority)
            for task in priority_tasks:
                if not task.last_progress or \
                   (now - task.last_progress) > self.procrastination_threshold:
                    print(f"\n{Fore.RED}¡Alerta de procrastinación! - Tarea {priority.name}:{Style.RESET_ALL}")
                    print(f"-> {task.name}")  # Cambiado emoji por ->
                    print(">> Mini-reto: Dedica solo 5 minutos a esta tarea ahora.")
                    if priority == Priority.ALTA:
                        print("!! Esta es una tarea de alta prioridad, ¡requiere atención inmediata!")

    def update_task_progress(self):
        """Registra progreso en una tarea existente"""
        if not self.tasks:
            print(f"{Fore.YELLOW}No hay tareas para actualizar.{Style.RESET_ALL}")
            return

        print("\nTareas disponibles:")
        self.list_tasks()
        
        try:
            task_num = int(input("\nSeleccione el número de la tarea: ")) - 1
            if 0 <= task_num < len(self.tasks):
                task = self.tasks[task_num]
                task.update_progress()
                self.storage.save_tasks(self.tasks)
                print(f"{Fore.GREEN}¡Progreso registrado con éxito!{Style.RESET_ALL}")
                
                # Mostrar tiempo desde el último progreso
                if task.last_progress:
                    elapsed = datetime.now() - task.last_progress
                    print(f"Tiempo desde el último progreso: {elapsed.days} días, {elapsed.seconds//3600} horas")
            else:
                print(f"{Fore.RED}Error: Número de tarea inválido{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Error: Por favor ingrese un número válido{Style.RESET_ALL}")

    def show_category_stats(self):
        """Muestra estadísticas por categoría"""
        stats = self.category_manager.get_category_stats(self.tasks)
        
        print("\n=== Estadísticas por Categoría ===")
        for category, data in stats.items():
            print(f"\n{Fore.CYAN}{category}:{Style.RESET_ALL}")
            print(f"  Total tareas: {data['total']}")
            print(f"  Completadas: {data['completed']}")
            print(f"  Pendientes: {data['pending']}")
            print(f"  Alta prioridad: {data['high_priority']}")
            print(f"  Procrastinadas: {data['procrastinated']}")

def main():
    manager = ProcrastinationManager()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== Gestor de Procrastinación ===")
        manager.check_procrastination()
        print("\n1. Añadir tarea")
        print("2. Listar todas las tareas")
        print("3. Listar por prioridad")
        print("4. Listar por categoría")
        print("5. Ver estadísticas por categoría")
        print("6. Registrar progreso")
        print("7. Salir")
        
        choice = input("\nSeleccione una opción: ")
        
        if choice == "1":
            manager.add_task()
        elif choice == "2":
            manager.list_tasks(sort_by_priority=False)
        elif choice == "3":
            print("\nFiltrar por prioridad:")
            print("1. Alta")
            print("2. Media")
            print("3. Baja")
            print("4. Todas (ordenadas por prioridad)")
            priority_choice = input("Seleccione una opción: ")
            
            if priority_choice in ["1", "2", "3"]:
                priority_map = {"1": Priority.ALTA, "2": Priority.MEDIA, "3": Priority.BAJA}
                filtered_tasks = manager.get_priority_tasks(priority_map[priority_choice])
                if not filtered_tasks:
                    print(f"\nNo hay tareas con esta prioridad.")
                else:
                    for task in filtered_tasks:
                        print(f"\n-> {task.name} - {task.description}")  # Cambiado emoji por ->
            else:
                manager.list_tasks(sort_by_priority=True)
        elif choice == "4":
            categories = manager.category_manager.get_categories()
            print("\nCategorías disponibles:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            try:
                cat_choice = int(input("\nSeleccione una categoría: ")) - 1
                if 0 <= cat_choice < len(categories):
                    filtered_tasks = [t for t in manager.tasks if t.category == categories[cat_choice]]
                    if not filtered_tasks:
                        print(f"\nNo hay tareas en esta categoría.")
                    else:
                        for task in filtered_tasks:
                            print(f"\n-> {task.name} - {task.description}")
            except ValueError:
                print("Selección inválida")
        elif choice == "5":
            manager.show_category_stats()
        elif choice == "6":
            manager.update_task_progress()
        elif choice == "7":
            break
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()