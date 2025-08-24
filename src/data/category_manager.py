"""Módulo para la gestión de categorías de tareas."""
from typing import Set, Dict, Any, List
from collections import defaultdict
from datetime import datetime
from src.models.task import Task, Priority # Importar Task y Priority para type hints

class CategoryManager:
    """Clase que gestiona las categorías disponibles para las tareas."""

    def __init__(self) -> None:
        """Inicializa el gestor de categorías con una categoría por defecto."""
        self.categories: Set[str] = {"General"}

    def add_category(self, category_name: str) -> None:
        """
        Añade una nueva categoría.

        Args:
            category_name: Nombre de la nueva categoría

        Raises:
            ValueError: Si la categoría ya existe
        """
        if category_name in self.categories:
            raise ValueError(f"La categoría '{category_name}' ya existe")
        self.categories.add(category_name)

    def remove_category(self, category_name: str) -> None:
        """
        Elimina una categoría existente.

        Args:
            category_name: Nombre de la categoría a eliminar

        Raises:
            ValueError: Si la categoría no existe o es la categoría General
        """
        if category_name == "General":
            raise ValueError("No se puede eliminar la categoría General")
        if category_name not in self.categories:
            raise ValueError(f"La categoría '{category_name}' no existe")
        self.categories.remove(category_name)

    def get_categories(self) -> Set[str]:
        """
        Obtiene todas las categorías disponibles.

        Returns:
            Set[str]: Conjunto con todas las categorías
        """
        return self.categories.copy()

    def get_category_stats(self, tasks: List[Task]) -> Dict[str, Dict[str, Any]]:
        """
        Genera estadísticas por categoría.

        Args:
            tasks: Lista de tareas para analizar.

        Returns:
            Dict[str, Dict[str, Any]]: Diccionario con estadísticas por categoría.
        """
        stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'total': 0,
            'completed': 0,
            'pending': 0,
            'high_priority': 0,
            'procrastinated': 0
        })

        for task in tasks:
            cat = task.category
            stats[cat]['total'] += 1
            stats[cat]['completed'] += 1 if task.completed else 0
            stats[cat]['pending'] += 0 if task.completed else 1
            stats[cat]['high_priority'] += 1 if task.priority == Priority.ALTA else 0

            if task.last_update and not task.completed:
                time_since_progress = datetime.now() - task.last_update
                if time_since_progress.days >= 1:
                    stats[cat]['procrastinated'] += 1

        return dict(stats)
