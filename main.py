import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainApp

def main():
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()