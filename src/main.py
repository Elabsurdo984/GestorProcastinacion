import os
import sys

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.manager import ProcrastinationManager
from ui.console import ConsoleUI

def main() -> None:
    manager = ProcrastinationManager()
    ui = ConsoleUI(manager)
    ui.run()

if __name__ == "__main__":
    main()
