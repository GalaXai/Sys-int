import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QPushButton
from src import ghp_ui, mrp_ui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHP & MRP app")

        # Creating main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Creating grid
        self.grid_layout = QGridLayout()
        self.central_widget.setLayout(self.grid_layout)

        # Displaying information
        self.info_label = QLabel("Please click on 'Refresh tables' button after entering any changes")
        self.info_label.setStyleSheet("QLabel { background : white; font-size: 12pt; padding: 5px;}")
        self.grid_layout.addWidget(self.info_label)

        # Adding first widget
        self.tab_label1 = ghp_ui.GHPWindow()
        self.grid_layout.addWidget(self.tab_label1, 1, 0)

        # Adding second widget
        self.tab_label2 = mrp_ui.MRPProductManager()
        self.grid_layout.addWidget(self.tab_label2, 1, 1)
        
        # Creating button
        self.add_widget_button = QPushButton("Refresh tables") 
        self.add_widget_button.setStyleSheet("QPushButton { background : #A7C7E7;}")
        self.add_widget_button.clicked.connect(self.add_new_widget)

        # Adding button
        self.grid_layout.addWidget(self.add_widget_button, 2, 1)

        self.grid3_f = False
        
    
    def add_new_widget(self):
        self.tab_label1.mrp_data = self.tab_label2.get_data()
        new_widget = self.tab_label1.calculate_ghp()
        item = self.grid_layout.itemAtPosition(3, 0)
        if item is not None:
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        # Adding third widget
        self.grid_layout.addWidget(new_widget, 3, 0, 1, 3) 

