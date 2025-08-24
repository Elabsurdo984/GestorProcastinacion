"""Main module for the Procrastination Manager application."""
import os
import sys

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.manager import ProcrastinationManager
from src.ui.console import ConsoleUI

def main() -> None:
    """Main function to run the Procrastination Manager application."""
    manager = ProcrastinationManager()
    ui = ConsoleUI(manager)
    ui.run()

if __name__ == "__main__":
    main()
