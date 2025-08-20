from enum import Enum
from datetime import datetime, timedelta

class Priority(Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"

class Task:
    def __init__(self, name: str, description: str, deadline: datetime, priority: Priority):
        # Permitimos fechas del mismo día, solo rechazamos fechas anteriores
        if deadline.date() < datetime.now().date():
            raise ValueError("La fecha límite no puede estar en el pasado")
            
        self.name = name
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.progress = 0
        self.last_update = datetime.now()
        
    def update_progress(self, new_progress: int) -> None:
        """Actualiza el progreso de la tarea y la fecha de última actualización"""
        if not 0 <= new_progress <= 100:
            raise ValueError("El progreso debe estar entre 0 y 100")
        self.progress = new_progress
        self.last_update = datetime.now()
        
    def is_procrastinating(self) -> bool:
        """Comprueba si ha pasado más de 24 horas sin actualizar la tarea"""
        time_since_update = datetime.now() - self.last_update
        return time_since_update > timedelta(hours=24)