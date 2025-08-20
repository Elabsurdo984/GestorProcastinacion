from datetime import datetime, timedelta
import os
import sys
from task import Task, Priority
from storage import TaskStorage
from colorama import init, Fore, Style

init()  # Inicializar colorama

class ProcrastinationManager:
    def __init__(self):
        self.storage = TaskStorage()
        self.tasks = self.storage.load_tasks()
        self.procrastination_threshold = timedelta(hours=24)

    def add_task(self):
        """Añade una nueva tarea con prioridad"""
        name = input("Nombre de la tarea: ")
        description = input("Descripción: ")
        deadline = input("Fecha límite (YYYY-MM-DD): ")
        
        print("\nPrioridad:")
        print("1. Baja")
        print("2. Media")
        print("3. Alta")
        priority_choice = input("Seleccione la prioridad (1-3) [2]: ").strip() or "2"
        
        priority_map = {"1": Priority.BAJA, "2": Priority.MEDIA, "3": Priority.ALTA}
        priority = priority_map.get(priority_choice, Priority.MEDIA)
        
        task = Task(name, description, deadline, priority)
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

def main():
    manager = ProcrastinationManager()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== Gestor de Procrastinación ===")
        manager.check_procrastination()
        print("\n1. Añadir tarea")
        print("2. Listar todas las tareas")
        print("3. Listar por prioridad")
        print("4. Registrar progreso")
        print("5. Salir")
        
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
            manager.update_task_progress()
        elif choice == "5":
            break
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()