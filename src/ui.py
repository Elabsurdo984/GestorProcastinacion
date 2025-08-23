from datetime import datetime
from colorama import Fore, Style
from src.task import Priority

class ConsoleUI:
    def __init__(self, manager):
        self.manager = manager

    def run(self):
        while True:
            self._clear_screen()
            print("\n=== Gestor de Procrastinación ===")
            self._check_procrastination()
            print("\n1. Añadir tarea")
            print("2. Listar todas las tareas")
            print("3. Listar por prioridad")
            print("4. Listar por categoría")
            print("5. Ver estadísticas por categoría")
            print("6. Registrar progreso")
            print("7. Completar tarea")
            print("8. Editar tarea")
            print("9. Eliminar tarea")
            print("10. Salir")
            
            choice = input("\nSeleccione una opción: ")
            
            if choice == "1":
                self._add_task()
            elif choice == "2":
                self._list_tasks(sort_by_priority=False)
            elif choice == "3":
                self._list_by_priority()
            elif choice == "4":
                self._list_by_category()
            elif choice == "5":
                self._show_category_stats()
            elif choice == "6":
                self._update_task_progress()
            elif choice == "7":
                self._complete_task()
            elif choice == "8":
                self._edit_task()
            elif choice == "9":
                self._delete_task()
            elif choice == "10":
                break
                
            input("\nPresione Enter para continuar...")

    def _clear_screen(self):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def _check_procrastination(self):
        procrastinated_tasks = self.manager.check_procrastination()
        for task in procrastinated_tasks:
            print(f"\n{Fore.RED}¡Alerta de procrastinación! - Tarea {task.priority.name}:{Style.RESET_ALL}")
            print(f"-> {task.name}")
            print(">> Mini-reto: Dedica solo 5 minutos a esta tarea ahora.")
            if task.priority == Priority.ALTA:
                print("!! Esta es una tarea de alta prioridad, ¡requiere atención inmediata!")

    def _add_task(self):
        name = input("Nombre de la tarea: ")
        description = input("Descripción: ")
        deadline_str = input("Fecha límite (YYYY-MM-DD): ")
        
        print("\nPrioridad:")
        print("1. Baja")
        print("2. Media")
        print("3. Alta")
        priority_choice = input("Seleccione la prioridad (1-3) [2]: ").strip() or "2"
        
        categories = list(self.manager.category_manager.get_categories())
        print("\nCategorías disponibles:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print(f"{len(categories) + 1}. Nueva categoría")
        
        cat_choice = input("\nSeleccione una categoría o cree una nueva: ")
        
        try:
            if int(cat_choice) == len(categories) + 1:
                category = input("Nombre de la nueva categoría: ")
            else:
                category = categories[int(cat_choice) - 1]
        except (ValueError, IndexError):
            category = "General"

        try:
            self.manager.add_task(name, description, deadline_str, priority_choice, category)
            print(f"{Fore.GREEN}¡Tarea añadida con éxito!{Style.RESET_ALL}")
        except ValueError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            print("Inténtelo de nuevo.")

    def _list_tasks(self, sort_by_priority=True):
        tasks = self.manager.get_tasks(sort_by_priority)
        if not tasks:
            print("No hay tareas pendientes.")
            return

        for i, task in enumerate(tasks, 1):
            priority_colors = {
                Priority.ALTA: Fore.RED,
                Priority.MEDIA: Fore.YELLOW,
                Priority.BAJA: Fore.GREEN
            }
            color = priority_colors[task.priority]
            status = "Completada" if task.completed else "Pendiente"
            last_progress = task.last_update.strftime("%Y-%m-%d %H:%M") if task.last_update else "Sin progreso"
            
            print(f"\n{color}{i}. {task.name} [{task.priority.name}]{Style.RESET_ALL}")
            print(f"   Descripción: {task.description}")
            print(f"   Fecha límite: {task.deadline}")
            print(f"   Estado: {status}")
            print(f"   Último progreso: {last_progress}")

    def _list_by_priority(self):
        print("\nFiltrar por prioridad:")
        print("1. Alta")
        print("2. Media")
        print("3. Baja")
        print("4. Todas (ordenadas por prioridad)")
        priority_choice = input("Seleccione una opción: ")
        
        priority_map = {"1": Priority.ALTA, "2": Priority.MEDIA, "3": Priority.BAJA}
        if priority_choice in priority_map:
            filtered_tasks = self.manager.get_priority_tasks(priority_map[priority_choice])
            if not filtered_tasks:
                print(f"\nNo hay tareas con esta prioridad.")
            else:
                for task in filtered_tasks:
                    print(f"\n-> {task.name} - {task.description}")
        else:
            self._list_tasks(sort_by_priority=True)

    def _list_by_category(self):
        categories = list(self.manager.category_manager.get_categories())
        print("\nCategorías disponibles:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        try:
            cat_choice = int(input("\nSeleccione una categoría: ")) - 1
            if 0 <= cat_choice < len(categories):
                category = categories[cat_choice]
                filtered_tasks = self.manager.get_category_tasks(category)
                if not filtered_tasks:
                    print(f"\nNo hay tareas en esta categoría.")
                else:
                    for task in filtered_tasks:
                        print(f"\n-> {task.name} - {task.description}")
        except (ValueError, IndexError):
            print("Selección inválida")

    def _show_category_stats(self):
        stats = self.manager.category_manager.get_category_stats(self.manager.tasks)
        print("\n=== Estadísticas por Categoría ===")
        for category, data in stats.items():
            print(f"\n{Fore.CYAN}{category}:{Style.RESET_ALL}")
            print(f"  Total tareas: {data['total']}")
            print(f"  Completadas: {data['completed']}")
            print(f"  Pendientes: {data['pending']}")
            print(f"  Alta prioridad: {data['high_priority']}")
            print(f"  Procrastinadas: {data['procrastinated']}")

    def _update_task_progress(self):
        tasks = self.manager.get_tasks(sort_by_priority=False)
        if not tasks:
            print(f"{Fore.YELLOW}No hay tareas para actualizar.{Style.RESET_ALL}")
            return

        print("\nTareas disponibles:")
        self._list_tasks(sort_by_priority=False)
        
        try:
            task_num = int(input("\nSeleccione el número de la tarea: ")) - 1
            if 0 <= task_num < len(tasks):
                task = tasks[task_num]
                new_progress = int(input(f"Ingrese el nuevo progreso para '{task.name}' (0-100): "))
                self.manager.update_task_progress(task, new_progress)
                print(f"{Fore.GREEN}¡Progreso registrado con éxito!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error: Número de tarea inválido{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Error: Por favor ingrese un número válido{Style.RESET_ALL}")

    def _complete_task(self):
        pending_tasks = [task for task in self.manager.get_tasks() if not task.completed]
        if not pending_tasks:
            print(f"{Fore.YELLOW}No hay tareas pendientes para completar.{Style.RESET_ALL}")
            return

        print("\nTareas pendientes:")
        for i, task in enumerate(pending_tasks, 1):
            print(f"{i}. {task.name} ({task.category}) - {task.priority.name}")

        try:
            task_num = int(input("\nSeleccione el número de la tarea a completar: ")) - 1
            if 0 <= task_num < len(pending_tasks):
                task_to_complete = pending_tasks[task_num]
                self.manager.complete_task(task_to_complete)
                print(f"{Fore.GREEN}¡Tarea '{task_to_complete.name}' marcada como completada!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error: Número de tarea inválido{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Error: Por favor ingrese un número válido{Style.RESET_ALL}")

    def _edit_task(self):
        tasks = self.manager.get_tasks(sort_by_priority=False)
        if not tasks:
            print(f"{Fore.YELLOW}No hay tareas para editar.{Style.RESET_ALL}")
            return

        print("\nSeleccione la tarea a editar:")
        self._list_tasks(sort_by_priority=False)
        
        try:
            task_num = int(input("\nNúmero de la tarea: ")) - 1
            if 0 <= task_num < len(tasks):
                task = tasks[task_num]
                
                new_name = input(f"Nuevo nombre [{task.name}]: ") or task.name
                new_description = input(f"Nueva descripción [{task.description}]: ") or task.description
                new_deadline_str = input(f"Nueva fecha límite (YYYY-MM-DD) [{task.deadline.strftime('%Y-%m-%d')}]: ") or task.deadline.strftime('%Y-%m-%d')
                
                print("\nNueva prioridad:")
                print("1. Baja")
                print("2. Media")
                print("3. Alta")
                new_priority_choice = input(f"Seleccione la nueva prioridad [{task.priority.name}]: ").strip() or str(list(Priority).index(task.priority) + 1)

                categories = list(self.manager.category_manager.get_categories())
                print("\nNuevas categorías disponibles:")
                for i, cat in enumerate(categories, 1):
                    print(f"{i}. {cat}")
                print(f"{len(categories) + 1}. Nueva categoría")
                
                new_cat_choice = input(f"\nSeleccione una nueva categoría [{task.category}]: ") or task.category
                
                if new_cat_choice.isdigit() and int(new_cat_choice) == len(categories) + 1:
                    new_category = input("Nombre de la nueva categoría: ")
                elif new_cat_choice.isdigit() and 1 <= int(new_cat_choice) <= len(categories):
                    new_category = categories[int(new_cat_choice) - 1]
                else:
                    new_category = new_cat_choice

                self.manager.edit_task(task, new_name, new_description, new_deadline_str, new_priority_choice, new_category)
                print(f"{Fore.GREEN}¡Tarea editada con éxito!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error: Número de tarea inválido{Style.RESET_ALL}")
        except ValueError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _delete_task(self):
        tasks = self.manager.get_tasks(sort_by_priority=False)
        if not tasks:
            print(f"{Fore.YELLOW}No hay tareas para eliminar.{Style.RESET_ALL}")
            return

        print("\nSeleccione la tarea a eliminar:")
        self._list_tasks(sort_by_priority=False)
        
        try:
            task_num = int(input("\nNúmero de la tarea: ")) - 1
            if 0 <= task_num < len(tasks):
                task_to_delete = tasks[task_num]
                confirm = input(f"¿Está seguro de que desea eliminar la tarea '{task_to_delete.name}'? (s/n): ").lower()
                if confirm == 's':
                    self.manager.delete_task(task_to_delete)
                    print(f"{Fore.GREEN}¡Tarea eliminada con éxito!{Style.RESET_ALL}")
                else:
                    print("Operación cancelada.")
            else:
                print(f"{Fore.RED}Error: Número de tarea inválido{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Error: Por favor ingrese un número válido{Style.RESET_ALL}")
