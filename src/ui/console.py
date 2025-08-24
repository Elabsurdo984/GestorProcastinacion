"""Módulo para la interfaz de usuario de consola del Gestor de Procrastinación."""
import os
from typing import Dict, Optional
from colorama import Fore, Style
from src.models.task import Priority
from src.core.manager import ProcrastinationManager

class ConsoleUI:
    """
    Clase que maneja la interacción con el usuario a través de la consola.
    Proporciona métodos para mostrar menús, obtener entradas y mostrar mensajes.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, manager: ProcrastinationManager) -> None:
        """
        Inicializa la interfaz de usuario de consola.

        Args:
            manager (ProcrastinationManager): Instancia del gestor de procrastinación.
        """
        self.manager = manager

    def _print_success(self, message: str) -> None:
        """Imprime un mensaje de éxito en color verde."""
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    def _print_error(self, message: str) -> None:
        """Imprime un mensaje de error en color rojo."""
        print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")

    def _print_warning(self, message: str) -> None:
        """Imprime un mensaje de advertencia en color amarillo."""
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    def _clear_screen(self) -> None:
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _get_priority_choice(self, current_priority: Optional[Priority] = None) -> str:
        """
        Obtiene la elección de prioridad del usuario.

        Args:
            current_priority (Optional[Priority]): La prioridad actual para el valor por defecto.

        Returns:
            str: La elección de prioridad del usuario.
        """
        print("\nPrioridad:")
        print("1. Baja")
        print("2. Media")
        print("3. Alta")
        default_choice = str(list(Priority).index(current_priority) + 1) if current_priority else "2" # pylint: disable=line-too-long
        return input(f"Seleccione la prioridad (1-3) [{default_choice}]: ").strip() or default_choice # pylint: disable=line-too-long

    def _get_category_choice(self, current_category: Optional[str] = None) -> str:
        """
        Obtiene la elección de categoría del usuario o permite crear una nueva.

        Args:
            current_category (Optional[str]): La categoría actual para el valor por defecto.

        Returns:
            str: La categoría elegida o el nombre de la nueva categoría.
        """
        categories = list(self.manager.category_manager.get_categories())
        print("\nCategorías disponibles:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print(f"{len(categories) + 1}. Nueva categoría")

        default_choice = current_category if current_category else "General"
        cat_choice = input(f"\nSeleccione una categoría o cree una nueva [{default_choice}]: ")

        if cat_choice.isdigit():
            choice_int = int(cat_choice)
            if choice_int == len(categories) + 1:
                return input("Nombre de la nueva categoría: ")
            if 1 <= choice_int <= len(categories):
                return categories[choice_int - 1]
        return cat_choice if cat_choice else default_choice

    def run(self) -> None:
        """Ejecuta el bucle principal de la interfaz de usuario."""
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
            else:
                self._print_error("Opción inválida. Por favor, intente de nuevo.")

            input("\nPresione Enter para continuar...")

    def _check_procrastination(self) -> None:
        """Verifica y muestra las tareas procrastinadas."""
        procrastinated_tasks = self.manager.check_procrastination()
        for task in procrastinated_tasks:
            print(f"{Fore.RED}¡Alerta de procrastinación! - Tarea {task.priority.name}:{Style.RESET_ALL}") # pylint: disable=line-too-long
            print(f"-> {task.name}")
            print(">> Mini-reto: Dedica solo 5 minutos a esta tarea ahora.")
            if task.priority == Priority.ALTA:
                print("!! Esta es una tarea de alta prioridad, ¡requiere atención inmediata!")

    def _add_task(self) -> None:
        """Permite al usuario añadir una nueva tarea."""
        name = input("Nombre de la tarea: ")
        description = input("Descripción: ")
        deadline_str = input("Fecha límite (YYYY-MM-DD): ")
        priority_choice = self._get_priority_choice()
        category = self._get_category_choice()

        try:
            self.manager.add_task(name, description, deadline_str, priority_choice, category)
            self._print_success("¡Tarea añadida con éxito!")
        except ValueError as err:
            self._print_error(str(err))
            print("Inténtelo de nuevo.")

    def _list_tasks(self, sort_by_priority: bool = True) -> None:
        """
        Lista todas las tareas o las tareas filtradas.

        Args:
            sort_by_priority (bool): Si es True, las tareas se ordenan por prioridad.
        """
        tasks = self.manager.get_tasks(sort_by_priority)
        if not tasks:
            self._print_warning("No hay tareas pendientes.")
            return

        for i, task in enumerate(tasks, 1):
            priority_colors: Dict[Priority, str] = {
                Priority.ALTA: Fore.RED,
                Priority.MEDIA: Fore.YELLOW,
                Priority.BAJA: Fore.GREEN
            }
            color = priority_colors[task.priority]
            status = "Completada" if task.completed else "Pendiente"
            last_progress = (task.last_update.strftime("%Y-%m-%d %H:%M")
                             if task.last_update else "Sin progreso")

            print(f"{color}{i}. {task.name} [{task.priority.name}]{Style.RESET_ALL}") # pylint: disable=line-too-long
            print(f"   Descripción: {task.description}")
            print(f"   Fecha límite: {task.deadline.strftime('%Y-%m-%d')}")
            print(f"   Estado: {status}")
            print(f"   Último progreso: {last_progress}")

    def _list_by_priority(self) -> None:
        """Lista tareas filtradas por prioridad."""
        print("\nFiltrar por prioridad:")
        print("1. Alta")
        print("2. Media")
        print("3. Baja")
        print("4. Todas (ordenadas por prioridad)")
        priority_choice = input("Seleccione una opción: ")

        if priority_choice in self.manager.PRIORITY_MAP:
            filtered_tasks = self.manager.get_priority_tasks(
                self.manager.PRIORITY_MAP[priority_choice])
            if not filtered_tasks:
                self._print_warning("\nNo hay tareas con esta prioridad.")
            else:
                for task in filtered_tasks:
                    print(f"\n-> {task.name} - {task.description}")
        else:
            self._list_tasks(sort_by_priority=True)

    def _list_by_category(self) -> None:
        """Lista tareas filtradas por categoría."""
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
                    self._print_warning(f"\nNo hay tareas en esta categoría.")
                else:
                    for task in filtered_tasks:
                        print(f"\n-> {task.name} - {task.description}")
            else:
                self._print_error("Selección inválida")
        except ValueError:
            self._print_error("Por favor ingrese un número válido")

    def _show_category_stats(self) -> None:
        """Muestra estadísticas de tareas por categoría."""
        stats = self.manager.category_manager.get_category_stats(self.manager.tasks)
        print("\n=== Estadísticas por Categoría ===")
        if not stats:
            self._print_warning("No hay categorías para mostrar estadísticas.")
            return

        for category, data in stats.items():
            print(f"{Fore.CYAN}{category}:{Style.RESET_ALL}")
            print(f"  Total tareas: {data['total']}")
            print(f"  Completadas: {data['completed']}")
            print(f"  Pendientes: {data['pending']}")
            print(f"  Alta prioridad: {data['high_priority']}")
            print(f"  Procrastinadas: {data['procrastinated']}")

    def _update_task_progress(self) -> None:
        """Permite al usuario registrar el progreso de una tarea."""
        tasks = self.manager.get_tasks(sort_by_priority=False)
        if not tasks:
            self._print_warning("No hay tareas para actualizar.")
            return

        print("\nTareas disponibles:")
        self._list_tasks(sort_by_priority=False)

        try:
            task_num = int(input("\nSeleccione el número de la tarea: ")) - 1
            if 0 <= task_num < len(tasks):
                task = tasks[task_num]
                new_progress = int(input(f"Ingrese el nuevo progreso para '{task.name}' (0-100): "))
                self.manager.update_task_progress(task, new_progress)
                self._print_success("¡Progreso registrado con éxito!")
            else:
                self._print_error("Número de tarea inválido")
        except ValueError:
            self._print_error("Por favor ingrese un número válido")

    def _complete_task(self) -> None:
        """Permite al usuario marcar una tarea como completada."""
        pending_tasks = [task for task in self.manager.get_tasks() if not task.completed]
        if not pending_tasks:
            self._print_warning("No hay tareas pendientes para completar.")
            return

        print("\nTareas pendientes:")
        for i, task in enumerate(pending_tasks, 1):
            print(f"{i}. {task.name} ({task.category}) - {task.priority.name}")

        try:
            task_num = int(input("\nSeleccione el número de la tarea a completar: ")) - 1
            if 0 <= task_num < len(pending_tasks):
                task_to_complete = pending_tasks[task_num]
                self.manager.complete_task(task_to_complete)
                self._print_success(f"¡Tarea '{task_to_complete.name}' marcada como completada!")
            else:
                self._print_error("Número de tarea inválido")
        except ValueError:
            self._print_error("Por favor ingrese un número válido")

    def _edit_task(self) -> None:
        """Permite al usuario editar una tarea existente."""
        tasks = self.manager.get_tasks(sort_by_priority=False)
        if not tasks:
            self._print_warning("No hay tareas para editar.")
            return

        print("\nSeleccione la tarea a editar:")
        self._list_tasks(sort_by_priority=False)

        try:
            task_num = int(input("\nNúmero de la tarea: ")) - 1
            if 0 <= task_num < len(tasks):
                task = tasks[task_num]

                new_name = input(f"Nuevo nombre [{task.name}]: ") or task.name
                new_description = input(f"Nueva descripción [{task.description}]: ") or task.description
                new_deadline_str = (input(f"Nueva fecha límite (YYYY-MM-DD) [{task.deadline.strftime('%Y-%m-%d')}]: ") # pylint: disable=line-too-long
                                    or task.deadline.strftime('%Y-%m-%d'))

                new_priority_choice = self._get_priority_choice(task.priority)
                new_category = self._get_category_choice(task.category)

                self.manager.edit_task(task, new_name, new_description, new_deadline_str,
                                       new_priority_choice, new_category)
                self._print_success("¡Tarea editada con éxito!")
            else:
                self._print_error("Número de tarea inválido")
        except ValueError as err:
            self._print_error(str(err))

    def _delete_task(self) -> None:
        """Permite al usuario eliminar una tarea."""
        tasks = self.manager.get_tasks(sort_by_priority=False)
        if not tasks:
            self._print_warning("No hay tareas para eliminar.")
            return

        print("\nSeleccione la tarea a eliminar:")
        self._list_tasks(sort_by_priority=False)

        try:
            task_num = int(input("\nNúmero de la tarea: ")) - 1
            if 0 <= task_num < len(tasks):
                task_to_delete = tasks[task_num]
                confirm = input(f"¿Está seguro de que desea eliminar la tarea '{task_to_delete.name}'? (s/n): ").lower() # pylint: disable=line-too-long
                if confirm == 's':
                    self.manager.delete_task(task_to_delete)
                    self._print_success("¡Tarea eliminada con éxito!")
                else:
                    self._print_warning("Operación cancelada.")
            else:
                self._print_error("Número de tarea inválido")
        except ValueError:
            self._print_error("Por favor ingrese un número válido")
