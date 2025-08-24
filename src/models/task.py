"""Módulo para la gestión de tareas individuales."""
from enum import Enum
from datetime import datetime, timedelta

class Priority(Enum):
    """Enumeración para los niveles de prioridad de las tareas."""
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"

class Task:
    """Clase que representa una tarea con sus atributos y métodos."""

    # pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-positional-arguments
    def __init__(self, name: str, description: str, deadline: datetime,
                 priority: Priority, category: str = "General"):
        """
        Inicializa una nueva tarea.

        Args:
            name: Nombre de la tarea
            description: Descripción detallada
            deadline: Fecha límite
            priority: Nivel de prioridad
            category: Categoría de la tarea

        Raises:
            ValueError: Si la fecha límite está en el pasado
        """
        if deadline.date() < datetime.now().date():
            raise ValueError("La fecha límite no puede estar en el pasado")

        self.name: str = name
        """Nombre de la tarea."""
        self.description: str = description
        """Descripción detallada de la tarea."""
        self.deadline: datetime = deadline
        """Fecha límite para completar la tarea."""
        self.priority: Priority = priority
        """Nivel de prioridad de la tarea."""
        self.progress: int = 0
        """Porcentaje de progreso de la tarea (0-100)."""
        self.last_update: datetime = datetime.now()
        """Marca de tiempo de la última actualización de la tarea."""
        self.category: str = category
        """Categoría a la que pertenece la tarea."""
        self.completed: bool = False
        """Indica si la tarea ha sido completada."""

    def update_progress(self, new_progress: int) -> None:
        """
        Actualiza el progreso de la tarea.

        Args:
            new_progress: Nuevo porcentaje de progreso (0-100)

        Raises:
            ValueError: Si el progreso no está entre 0 y 100
        """
        if not 0 <= new_progress <= 100:
            raise ValueError("El progreso debe estar entre 0 y 100")
        self.progress = new_progress
        self.last_update = datetime.now()

    def is_procrastinating(self) -> bool:
        """
        Verifica si la tarea está siendo procrastinada.

        Returns:
            bool: True si han pasado más de 24 horas sin actualización
        """
        time_since_update: timedelta = datetime.now() - self.last_update
        return time_since_update > timedelta(hours=24)
