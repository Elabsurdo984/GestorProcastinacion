"""Módulo para la gestión de tareas individuales."""
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional

class Priority(Enum):
    """Enumeración para los niveles de prioridad de las tareas."""
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"

class Task:
    """Clase que representa una tarea con sus atributos y métodos."""

    def __init__(self, name: str, description: str, deadline: datetime, priority: Priority):
        """
        Inicializa una nueva tarea.

        Args:
            name: Nombre de la tarea
            description: Descripción detallada
            deadline: Fecha límite
            priority: Nivel de prioridad

        Raises:
            ValueError: Si la fecha límite está en el pasado
        """
        if deadline.date() < datetime.now().date():
            raise ValueError("La fecha límite no puede estar en el pasado")

        self.name = name
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.progress: int = 0
        self.last_update: datetime = datetime.now()
        self.category: str = "General"

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
        time_since_update = datetime.now() - self.last_update
        return time_since_update > timedelta(hours=24)