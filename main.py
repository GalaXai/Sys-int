from src import GHPWindow
import sys
from PyQt5.QtWidgets import QApplication

def main():
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GHPWindow()
    window.show()
    sys.exit(app.exec_())