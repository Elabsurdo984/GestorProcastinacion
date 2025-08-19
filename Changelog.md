# Changelog
Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.0.0] - 2025-08-19
### Añadido
- Sistema básico de gestión de tareas
  - Crear tareas con nombre, descripción y fecha límite
  - Listar todas las tareas existentes
  - Marcar progreso en tareas
- Detección automática de procrastinación
  - Alerta cuando una tarea lleva más de 24h sin progreso
  - Sistema de mini-retos motivacionales
- Persistencia de datos
  - Almacenamiento de tareas en archivo JSON
  - Carga automática de tareas al iniciar
- Interfaz de consola
  - Menú principal interactivo
  - Visualización clara del estado de las tareas
  - Mensajes de confirmación para las acciones

### Características técnicas
- Arquitectura modular (main.py, task.py, storage.py)
- Programación orientada a objetos
- Manejo de fechas y tiempo
- Sistema de persistencia de datos
- Gestión de estados de tareas