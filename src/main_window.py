import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QPushButton
from src import ghp_ui, mrp_ui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Połączone okna")

        # Tworzenie głównego widgetu
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Tworzenie siatki
        self.grid_layout = QGridLayout()
        self.central_widget.setLayout(self.grid_layout)

        # Dodawanie pierwszego okna do siatki
        self.tab_label1 = ghp_ui.GHPWindow()
        self.grid_layout.addWidget(self.tab_label1, 0, 0)

        # Dodawanie drugiego okna do siatki
        self.tab_label2 = mrp_ui.MRPProductManager()
        self.grid_layout.addWidget(self.tab_label2, 0, 1)
        
        # Tworzenie przycisku
        self.add_widget_button = QPushButton("Refresh tables") 
        self.add_widget_button.clicked.connect(self.add_new_widget)

        # Dodawanie trzeciego okna do siatki
        self.grid_layout.addWidget(self.add_widget_button, 1, 1)

        self.grid3_f = False
        
    
    def add_new_widget(self):
        self.tab_label1.mrp_data = self.tab_label2.get_data()
        new_widget = self.tab_label1.calculate_ghp()
        item = self.grid_layout.itemAtPosition(2, 0)
        if item is not None:
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        # Dodawanie nowego widgetu do GridLayout
        self.grid_layout.addWidget(new_widget, 2, 0, 1, 3) 

