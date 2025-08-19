from datetime import datetime, timedelta
import os
from task import Task
from storage import TaskStorage

class ProcrastinationManager:
    def __init__(self):
        self.storage = TaskStorage()
        self.tasks = self.storage.load_tasks()
        self.procrastination_threshold = timedelta(hours=24)

    def add_task(self):
        """Añade una nueva tarea"""
        name = input("Nombre de la tarea: ")
        description = input("Descripción: ")
        deadline = input("Fecha límite (YYYY-MM-DD): ")
        
        task = Task(name, description, deadline)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        print("¡Tarea añadida con éxito!")

    def list_tasks(self):
        """Muestra todas las tareas"""
        if not self.tasks:
            print("No hay tareas pendientes.")
            return

        for i, task in enumerate(self.tasks, 1):
            status = "Completada" if task.completed else "Pendiente"
            last_progress = task.last_progress.strftime("%Y-%m-%d %H:%M") if task.last_progress else "Sin progreso"
            print(f"\n{i}. {task.name}")
            print(f"   Descripción: {task.description}")
            print(f"   Fecha límite: {task.deadline}")
            print(f"   Estado: {status}")
            print(f"   Último progreso: {last_progress}")

    def update_task_progress(self):
        """Registra progreso en una tarea"""
        self.list_tasks()
        try:
            task_num = int(input("\nSeleccione el número de la tarea: ")) - 1
            if 0 <= task_num < len(self.tasks):
                self.tasks[task_num].update_progress()
                self.storage.save_tasks(self.tasks)
                print("¡Progreso registrado!")
            else:
                print("Número de tarea inválido")
        except ValueError:
            print("Por favor, ingrese un número válido")

    def check_procrastination(self):
        """Revisa las tareas para detectar procrastinación"""
        now = datetime.now()
        for task in self.tasks:
            if task.completed:
                continue
                
            if not task.last_progress or \
               (now - task.last_progress) > self.procrastination_threshold:
                print(f"\n¡Alerta de procrastinación para: {task.name}!")
                print("💪 Mini-reto: Dedica solo 5 minutos a esta tarea ahora.")
                print("🎯 Cualquier progreso es mejor que ninguno.")

def main():
    manager = ProcrastinationManager()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== Gestor de Procrastinación ===")
        manager.check_procrastination()
        print("\n1. Añadir tarea")
        print("2. Listar tareas")
        print("3. Registrar progreso")
        print("4. Salir")
        
        choice = input("\nSeleccione una opción: ")
        
        if choice == "1":
            manager.add_task()
        elif choice == "2":
            manager.list_tasks()
        elif choice == "3":
            manager.update_task_progress()
        elif choice == "4":
            break
        else:
            print("Opción inválida")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()