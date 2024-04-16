import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QFormLayout, QSpinBox, QListWidget
import json
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt


class MRPProductManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MRP Product Manager")
        self.setGeometry(100, 100, 600, 400)
        
        # Central Widget and Layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Form for Product Entry
        self.form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.realization_time_edit = QSpinBox()
        self.nb_of_resources_edit = QSpinBox()
        self.resource_per_unit_edit = QSpinBox()
        self.resource_per_batch_edit = QSpinBox()
        self.nb_of_weeks_edit = QSpinBox()
        self.mrp_array_lower_level_edit = QLineEdit()
        self.receptions_edit = QLineEdit()

        self.form_layout.addRow("Name:", self.name_edit)
        self.form_layout.addRow("Realization Time (weeks):", self.realization_time_edit)
        self.form_layout.addRow("Number of Resources:", self.nb_of_resources_edit)
        self.form_layout.addRow("Resources per Unit:", self.resource_per_unit_edit)
        self.form_layout.addRow("Resources per Batch:", self.resource_per_batch_edit)
        self.form_layout.addRow("Number of Weeks:", self.nb_of_weeks_edit)
        self.form_layout.addRow("Lower Level MRP Products:", self.mrp_array_lower_level_edit)
        self.form_layout.addRow("Receptions (week, reception):", self.receptions_edit)
        
        # Buttons
        self.buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Product")
        self.clear_button = QPushButton("Clear")
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.clear_button)

        self.add_button.clicked.connect(self.add_product)
        self.clear_button.clicked.connect(self.clear_form)
        
        # List to display products
        self.products_list = QListWidget()

        # Assembling the layout
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.products_list)

    def add_product(self):
        product_details = {
            "Name": self.name_edit.text(),
            "Realization": self.realization_time_edit.value(), 
            "Resources": self.nb_of_resources_edit.value(),
            "Resources/Unit": self.resource_per_unit_edit.value(),
            "Resources/Batch": self.resource_per_batch_edit.value(), 
            "Weeks": self.nb_of_weeks_edit.value(),
            "Lower Level": self.mrp_array_lower_level_edit.text(), 
            "Receptions": self.receptions_edit.text()
        }
        # Convert dictionary to JSON string
        item_text = json.dumps(product_details)
        self.products_list.addItem(item_text)
        self.clear_form()
        print(self.get_selected_product_details())

    def get_selected_product_details(self):
        items = []
        for index in range(self.products_list.count()):
            item = self.products_list.item(index)
            items.append(json.loads(item.text()))  # Fetches the display text of the item
        return items
    
    def clear_form(self):
        # Clear the form inputs
        self.name_edit.clear()
        self.realization_time_edit.setValue(0)
        self.nb_of_resources_edit.setValue(0)
        self.resource_per_unit_edit.setValue(0)
        self.resource_per_batch_edit.setValue(0)
        self.nb_of_weeks_edit.setValue(0)
        self.mrp_array_lower_level_edit.clear()
        self.receptions_edit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MRPProductManager()
    main_window.show()
    sys.exit(app.exec_())
