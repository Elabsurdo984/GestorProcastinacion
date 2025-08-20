# Changelog
Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.2.0] - 2025-08-19
### Añadido
- Sistema de categorización de tareas
  - Creación de categorías personalizadas
  - Categoría "General" por defecto
  - Filtrado de tareas por categoría
- Estadísticas detalladas por categoría
  - Total de tareas
  - Tareas completadas y pendientes
  - Tareas de alta prioridad
  - Tareas procrastinadas
- Mejoras en la interfaz de usuario
  - Nuevo menú para categorías
  - Visualización de estadísticas

## [1.1.0] - 2025-08-19
### Añadido
- Sistema de prioridades para tareas
  - Niveles: Alta, Media, Baja
  - Código de colores para diferentes prioridades
  - Ordenamiento por prioridad
  - Filtrado de tareas por prioridad
- Mejoras en la interfaz de consola
  - Colores para mejor visualización
  - Indicadores visuales de prioridad
- Alertas especiales para tareas de alta prioridad

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