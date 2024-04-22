from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFormLayout, QSpinBox, QListWidget, QTableWidgetItem, QTabWidget, QTableWidget, QHeaderView
import json
from PyQt5.QtGui import QFont


class MRPProductManager(QDialog):
    def __init__(self, parent = None):
        super(MRPProductManager, self).__init__(parent)
        self.setWindowTitle("MRP Product Manager")
        self.setGeometry(100, 100, 600, 400)
        
         # Setup layout directly on QDialog
        self.layout = QVBoxLayout(self)  # Set the layout on the QDialog itself

        # If you need a central widget, you can still add one:
        self.central_widget = QWidget(self)
        self.layout.addWidget(self.central_widget)
        
        # Now setup more widgets into the central_widget if necessary
        self.inner_layout = QVBoxLayout(self.central_widget)  # Create an inner layout for central_widget
        
        # Form for Product Entry
        self.form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.realization_time_edit = QSpinBox()
        self.nb_of_resources_edit = QSpinBox()
        self.resource_per_unit_edit = QSpinBox()
        self.resource_per_batch_edit = QSpinBox()
        self.mrp_array_lower_level_edit = QLineEdit()
        self.receptions_edit = QLineEdit()

        self.form_layout.addRow("Name:", self.name_edit)
        self.form_layout.addRow("Realization Time (weeks):", self.realization_time_edit)
        self.form_layout.addRow("Number of Resources:", self.nb_of_resources_edit)
        self.form_layout.addRow("Resources per Unit:", self.resource_per_unit_edit)
        self.form_layout.addRow("Resources per Batch:", self.resource_per_batch_edit)
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

        # VARIABLES
        if not hasattr(self, "raw_data"):
            self.raw_data = {}
        
        if not hasattr(self, "value_container"):
            self.values_containers = [
                self.realization_time_edit,
                self.nb_of_resources_edit,
                self.resource_per_unit_edit,
                self.resource_per_batch_edit,
                self.mrp_array_lower_level_edit,
                self.receptions_edit,
            ]

        

    def add_product(self):

        self.raw_data[self.name_edit.text()] = [
            widget.value() if hasattr(widget, 'value') else None if widget.text() == "" else widget.text()
            for widget in self.values_containers
        ]

        product_details = {
            self.name_edit.text():{
            "Realization": self.realization_time_edit.value(), 
            "Resources": self.nb_of_resources_edit.value(),
            "Resources/Unit": self.resource_per_unit_edit.value(),
            "Resources/Batch": self.resource_per_batch_edit.value(), 
            "Lower Level": self.mrp_array_lower_level_edit.text(), 
            "Receptions": self.receptions_edit.text()}}
        
        # Convert dictionary to JSON string
        item_text = json.dumps(product_details)
        self.products_list.addItem(item_text)
        self.clear_form()
    
    def get_data(self):
        return self.raw_data
    
    def open_mrp_manager(self):
        self.mrp_window = MRPProductManager(self)
        result = self.mrp_window.exec_()  # This will now work as MRPProductManager is a QDialog
        if result == QDialog.Accepted:
            self.mrp_data = self.mrp_window.get_data()
    
    def clear_form(self):
        # Clear the form inputs
        self.name_edit.clear()
        self.realization_time_edit.setValue(1)
        self.nb_of_resources_edit.setValue(1)
        self.resource_per_unit_edit.setValue(1)
        self.resource_per_batch_edit.setValue(1)
        self.mrp_array_lower_level_edit.clear()
        self.receptions_edit.clear()

class DataFrameViewer(QDialog):
    def __init__(self, dataframes, parent=None):
        super(DataFrameViewer, self).__init__(parent)
        self.setWindowTitle("MRP Tables")
        self.dataframes = dataframes
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        tab_widget = QTabWidget(self)
        layout.addWidget(tab_widget)

        # Create a tab for each DataFrame
        for idx, df in enumerate(self.dataframes):
            tab = QTableWidget()
            tab_widget.addTab(tab, f'{df.name}')
            self.populate_table_widget(tab, df.mrp_df)

        self.setLayout(layout)
        self.resize(800, 600)

    def populate_table_widget(self, table_widget, dataframe):
        # Set table dimensions
        table_widget.setRowCount(dataframe.shape[0])
        table_widget.setColumnCount(dataframe.shape[1])
        table_widget.setVerticalHeaderLabels(["Gross Req", "Scheduled Receipts", "Projected On Hand", "Net Requirements",
            "Planned Receipts", "Planned Order Release"])
        
        # Styling
        table_widget.setAlternatingRowColors(True)
        # Styling & Fonts & Auto-resize
        table_widget.setFont(QFont("Arial", 10))
        header_font = QFont("Arial", 12)
        table_widget.horizontalHeader().setFont(header_font)
        table_widget.verticalHeader().setFont(header_font)
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Populate the table with items
        for row in range(dataframe.shape[0]):
            for col in range(dataframe.shape[1]):
                item = QTableWidgetItem(str(dataframe.iloc[row, col]))
                table_widget.setItem(row, col, item)

        table_widget.resizeColumnsToContents()
        