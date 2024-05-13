from src import GHPWindow, MainWindow
import sys
from PyQt5.QtWidgets import QApplication

def main():
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = GHPWindow()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())