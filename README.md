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
│   ├── main.py         # Lógica de negocio principal
│   ├── ui.py           # Interfaz de usuario de consola
│   ├── task.py         # Clase Task y enum Priority
│   ├── storage.py      # Manejo de persistencia de datos
│   └── category_manager.py # Gestión de categorías
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

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📝 Licencia

[MIT](https://choosealicense.com/licenses/mit/)

## 📋 Versiones
- v1.0.0: Versión inicial con funcionalidades básicas
- v1.1.0: Añadido sistema de prioridades y mejoras visuales
- v1.2.0: Sistema de categorización y estadísticas
- v1.2.1: Funcionalidad para marcar tareas como completadas
- v1.2.2: Nueva organización de carpetas
- v1.2.3: Sistema completo de pruebas y validaciones
