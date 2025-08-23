# Changelog
Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.3.1] - 2025-08-23
### Añadido
- Nuevos tests unitarios para mejorar la cobertura de código en:
  - `src/category_manager.py` (cubriendo casos de eliminación de categorías inexistentes y estadísticas)
  - `src/storage.py` (cubriendo la actualización de tareas inexistentes)
  - `src/task.py` (cubriendo la validación de progreso inválido)

### Corregido
- Lógica en `src/category_manager.py` para evitar que las tareas completadas se marquen como "procrastinadas" en las estadísticas.

### Mejorado
- Cobertura de tests unitarios del proyecto, alcanzando un 99%.

## [1.3.0] - 2025-08-23
### Añadido
- Funcionalidad para editar tareas existentes.
- Funcionalidad para eliminar tareas.

### Modificado
- Refactorización mayor: separada la lógica de negocio de la interfaz de usuario.
  - Creada la clase `ConsoleUI` en `src/ui.py` para manejar todas las interacciones con el usuario.
  - `ProcrastinationManager` ahora se enfoca exclusivamente en la lógica de negocio.

## [1.2.5] - 2025-08-23
### Añadido
- `requirements.txt` para gestionar las dependencias del proyecto.
- Flujo de trabajo de Integración Continua (CI) con GitHub Actions para ejecutar pruebas automáticamente.

### Modificado
- El flujo de trabajo de CI ahora instala las dependencias desde `requirements.txt`.

## [1.2.4] - 2025-08-23
### Corregido
- Solucionado `AttributeError` en `Storage` al implementar el método `update_task`.
- Corregido `ImportError` ajustando las importaciones a relativas para la estructura del paquete.
- Solucionado `TypeError` en la creación de tareas al no aceptar la categoría.
- El programa ya no se cierra al introducir una fecha límite en el pasado.

### Añadido
- Alertas de procrastinación ahora son visibles inmediatamente para demostración.

## [1.2.3] - 2025-08-20
### Añadido
- Sistema completo de pruebas unitarias y de integración
  - Tests para gestión de tareas
  - Tests para sistema de almacenamiento
  - Tests para gestor de categorías
  - Tests de integración para flujos completos
- Mejoras en la validación de datos
  - Validación de fechas límite
  - Protección contra categorías duplicadas
  - Validación de progreso de tareas

### Modificado
- Refactorización del sistema de almacenamiento
- Mejora en la gestión de categorías
- Optimización del manejo de fechas límite

## [1.2.2] - 2025-08-20
### Añadido
- Nueva organizacion de carpetas para el codigo

## [1.2.1] - 2025-08-19
### Añadido
- Nueva funcionalidad para marcar tareas como completadas
  - Opción dedicada en el menú principal
  - Lista filtrada de tareas pendientes
  - Confirmación visual al completar una tarea
  - Actualización automática del último progreso al completar

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
