# Gestor de Procrastinación

Una herramienta simple pero efectiva para gestionar tareas y combatir la procrastinación.

## 🎯 Características principales

- Gestión de tareas con:
  - Añadir, editar y eliminar tareas
  - Nombre y descripción
  - Fecha límite
  - Sistema de prioridades (Alta, Media, Baja)
  - Seguimiento del progreso
- Detección automática de procrastinación
- Sistema de mini-retos motivacionales
- Almacenamiento persistente de datos en JSON
- Interfaz con códigos de color para mejor visualización

## 🚀 Instalación

1. Asegúrate de tener Python 3.13 instalado
2. Clona este repositorio:
```bash
git clone https://github.com/tuusuario/GestorProcastinacion
```
3. Navega al directorio del proyecto:
```bash
cd GestorProcastinacion
```
4. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

Ejecuta el programa con:

```bash
python -m src.main
```

### Menú principal:
1. Añadir tarea
2. Listar todas las tareas
3. Listar por prioridad
4. Listar por categoría
5. Ver estadísticas por categoría
6. Registrar progreso
7. Completar tarea
8. Editar tarea
9. Eliminar tarea
10. Salir

### Sistema de prioridades:
- **Alta**: 🔴 Tareas críticas que requieren atención inmediata
- **Media**: 🟡 Tareas importantes pero no urgentes
- **Baja**: 🟢 Tareas que pueden esperar

### Filtrado y visualización:
- Ver todas las tareas
- Filtrar por nivel de prioridad
- Ordenamiento automático por prioridad
- Códigos de color para mejor identificación

## 🏗️ Estructura del proyecto

```
GestorProcastinacion/
│
├── src/
│   ├── __init__.py
│   ├── main.py         # Punto de entrada de la aplicación
│   ├── core/
│   │   ├── __init__.py
│   │   └── manager.py  # Lógica de negocio principal (ProcrastinationManager)
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py     # Clases de modelos (Task, Priority)
│   ├── data/
│   │   ├── __init__.py
│   │   ├── storage.py  # Manejo de persistencia de datos (Storage)
│   │   └── category_manager.py # Gestión de categorías (CategoryManager)
│   └── ui/
│       ├── __init__.py
│       └── console.py  # Interfaz de usuario de consola (ConsoleUI)
│
├── tests/
│   ├── test_task.py           # Pruebas de tareas
│   ├── test_storage.py        # Pruebas de almacenamiento
│   ├── test_category_manager.py # Pruebas de categorías
│   └── test_integration/      # Pruebas de integración
│
├── tasks.json      # Archivo de almacenamiento de tareas
├── README.md       # Este archivo
└── CHANGELOG.md    # Historial de cambios
```

## ⚙️ Requisitos técnicos
- Python 3.13
- colorama (para la interfaz con colores)
- unittest (incluido en Python, para ejecutar pruebas)

## 🔍 Notas de uso
- Para mejor visualización, se recomienda usar Windows Terminal
- En caso de problemas con emojis, el programa se adaptará automáticamente
- Las tareas se guardan automáticamente después de cada modificación
- Para ejecutar las pruebas: `python -m unittest discover -v`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para asegurar la calidad del código y la estabilidad del proyecto, por favor, ten en cuenta lo siguiente al enviar un Pull Request:

1.  **Abre un Issue**: Antes de empezar a trabajar en una nueva característica o corrección de errores, por favor, abre un issue para discutir los cambios que te gustaría hacer. Esto nos ayuda a coordinar el trabajo y evitar duplicidades.
2.  **Estilo de Código (Pylint)**: Asegúrate de que tu código cumple con los estándares de calidad definidos. El CI ejecutará Pylint y el Pull Request no será aprobado si el score es inferior a **8.20**. Puedes ejecutar Pylint localmente con `pylint src/**/*.py`.
3.  **Cobertura de Tests**: Todos los cambios deben estar cubiertos por tests unitarios y/o de integración. El CI verificará que la cobertura de código no sea inferior al **90%**. Puedes ejecutar los tests y verificar la cobertura localmente con `coverage run -m unittest discover -v` y `coverage report -m`.
4.  **Mensajes de Commit Claros**: Utiliza mensajes de commit descriptivos y en español.
5.  **Una Característica por PR**: Cada Pull Request debe enfocarse en una única característica o corrección de error.

Gracias por tu colaboración.

## 📝 Licencia

[MIT](https://choosealicense.com/licenses/mit/)

## 📋 Versiones
- v1.5.0: Refactorización completa de la arquitectura del proyecto para mejorar la modularidad.
- v1.4.0: Mejoras en la calidad del código y refactorización de la lógica interna.
- v1.3.1: Añadidos nuevos tests unitarios y corregida lógica de procrastinación en estadísticas.
- v1.3.0: Añadida funcionalidad para editar y eliminar tareas; refactorización de UI.
- v1.2.5: Añadido `requirements.txt` y flujo de trabajo de CI con GitHub Actions.
- v1.2.4: Corrección de errores de importación y atributos, y mejoras en alertas de procrastinación.
- v1.2.3: Sistema completo de pruebas unitarias y de integración, y mejoras en validación de datos.
- v1.2.2: Nueva organización de carpetas para el código.
- v1.2.1: Nueva funcionalidad para marcar tareas como completadas.
- v1.2.0: Sistema de categorización de tareas y estadísticas detalladas.
- v1.1.0: Sistema de prioridades para tareas y mejoras en la interfaz de consola.
- v1.0.0: Versión inicial con funcionalidades básicas.
