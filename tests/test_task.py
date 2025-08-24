import unittest
from datetime import datetime, timedelta
from src.models.task import Task, Priority

class TestTask(unittest.TestCase):
    def setUp(self):
        self.fecha_limite = datetime.now() + timedelta(days=7)
        self.task = Task("Tarea de prueba", "Descripción de prueba", self.fecha_limite, Priority.ALTA)

    def test_creacion_tarea(self):
        self.assertEqual(self.task.name, "Tarea de prueba")
        self.assertEqual(self.task.description, "Descripción de prueba")
        self.assertEqual(self.task.priority, Priority.ALTA)

    def test_actualizar_progreso(self):
        self.task.update_progress(50)
        self.assertEqual(self.task.progress, 50)
        
    def test_validar_fecha_limite(self):
        with self.assertRaises(ValueError):
            Task("Tarea inválida", "Descripción", datetime.now() - timedelta(days=1), Priority.ALTA)

    def test_detectar_procrastinacion(self):
        self.task.last_update = datetime.now() - timedelta(hours=25)
        self.assertTrue(self.task.is_procrastinating())

    def test_actualizar_progreso_invalido(self):
        with self.assertRaises(ValueError):
            self.task.update_progress(101)
        with self.assertRaises(ValueError):
            self.task.update_progress(-1)
