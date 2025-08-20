from collections import defaultdict
from datetime import datetime

class CategoryManager:
    def __init__(self):
        self.categories = set(["General"])  # Categoría por defecto

    def add_category(self, category_name):
        """Añade una nueva categoría"""
        self.categories.add(category_name)
        return True

    def get_categories(self):
        """Retorna todas las categorías disponibles"""
        return sorted(list(self.categories))

    def get_category_stats(self, tasks):
        """Genera estadísticas por categoría"""
        stats = defaultdict(lambda: {
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
            stats[cat]['high_priority'] += 1 if task.priority.name == 'ALTA' else 0
            
            if task.last_progress:
                time_since_progress = datetime.now() - task.last_progress
                if time_since_progress.days >= 1:
                    stats[cat]['procrastinated'] += 1

        return dict(stats)