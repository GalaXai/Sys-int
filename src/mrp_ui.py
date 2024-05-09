from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFormLayout, QSpinBox, QListWidget, QTableWidgetItem, QTabWidget, QTableWidget, QHeaderView
from PyQt5.QtCore import QRegExp
import json
from PyQt5.QtGui import QFont, QRegExpValidator
from re import compile

def SpinBoxConf():
    spin_box = QSpinBox()
    spin_box.setRange(0, 999)  # Set the range
    return spin_box

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
        self.realization_time_edit = SpinBoxConf()
        self.nb_of_resources_edit = SpinBoxConf()
        self.resource_per_unit_edit = SpinBoxConf()
        self.resource_per_batch_edit = SpinBoxConf()
        self.mrp_array_lower_level_edit = QLineEdit()
        self.receptions_edit = QLineEdit()

        self.name_edit.setPlaceholderText("Enter product name")
        self.mrp_array_lower_level_edit.setPlaceholderText("Enter lower level MRP products as: product_name, product_name, ...")
        self.receptions_edit.setPlaceholderText("Enter data as (week, reception), (week, reception)...")

        # Validators
        
        regex = QRegExp(r"\(\d+,\s*\d+\)(,\s*\(\d+,\s*\d+\))*")
        validator = QRegExpValidator(regex)
        self.receptions_edit.setValidator(validator)

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
        self.clear_button.clicked.connect(self.clear_list)
        
        # List to display products
        self.products_list = QListWidget()

        # Assembling the layout
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.products_list)
        self.products_list.itemClicked.connect(self.on_item_clicked)


        # Variables
        self.currently_editing_flag = False

    def compile_product_details(self):
        return {
            self.name_edit.text(): {
                "Realization": self.realization_time_edit.value(),
                "Resources": self.nb_of_resources_edit.value(),
                "Resources/Unit": self.resource_per_unit_edit.value(),
                "Resources/Batch": self.resource_per_batch_edit.value(),
                "Lower Level": self.mrp_array_lower_level_edit.text(),
                "Receptions": self.receptions_edit.text()
            }
        }        

    def add_product(self):
        product_details = self.compile_product_details()
        item_text = json.dumps(product_details)
        self.products_list.addItem(item_text)
        self.clear_form()

    def parse_receptions(self, input_text):
        # Parse the input text and convert into a list of dictionaries
        if not input_text:
            return None
        pattern = compile(r"\((\d+),\s*(\d+)\)")
        matches = pattern.findall(input_text)
        return [{"week": int(week), "reception": int(reception)} for week, reception in matches]

    
    def get_data(self) -> dict:
        data = {}
        for index in range(self.products_list.count()):
            item = self.products_list.item(index)
            item_data = json.loads(item.text())
            details = next(iter(item_data.values()))
            values = [value if value != '' else None for value in details.values()]
            data[next(iter(item_data.keys()))] = values

        for _, value in data.items():
            value[-1] = self.parse_receptions(value[-1])
        return data
    
    def clear_form(self):
        # Clear the form inputs
        self.name_edit.clear()
        self.realization_time_edit.setValue(0)
        self.nb_of_resources_edit.setValue(0)
        self.resource_per_unit_edit.setValue(0)
        self.resource_per_batch_edit.setValue(0)
        self.mrp_array_lower_level_edit.clear()
        self.receptions_edit.clear()

        if self.currently_editing_flag:
            self.swap_button()
    
    def on_item_clicked(self, item):
        data = json.loads(item.text())
        # Assuming data is stored as {name: {details}}
        name, details = next(iter(data.items()))
        self.name_edit.setText(name)
        self.realization_time_edit.setValue(details['Realization'])
        self.nb_of_resources_edit.setValue(details['Resources'])
        self.resource_per_unit_edit.setValue(details['Resources/Unit'])
        self.resource_per_batch_edit.setValue(details['Resources/Batch'])
        self.mrp_array_lower_level_edit.setText(details['Lower Level'])
        self.receptions_edit.setText(details['Receptions'])
        self.currently_editing = item

        self.swap_button()


    def swap_button(self):
        if self.currently_editing_flag:
            self.add_button.disconnect()
            self.add_button.setText("Add Product")
            self.add_button.clicked.connect(self.add_product)
        else:
            self.add_button.disconnect()
            self.add_button.setText("Update Product")
            self.add_button.clicked.connect(self.on_save_clicked)
        self.currently_editing_flag = not self.currently_editing_flag
        
    def on_save_clicked(self):
        updated_item_text = json.dumps(self.compile_product_details())
        self.currently_editing.setText(updated_item_text)            
        self.swap_button()
        self.clear_form()


    def clear_list(self):
        # Clear the form inputs
        self.products_list.clear()
        if self.currently_editing_flag:
            self.swap_button()
    
    def open_mrp_manager(self):
        self.mrp_window = MRPProductManager(self)
        result = self.mrp_window.exec_()  # This will now work as MRPProductManager is a QDialog
        if result == QDialog.Accepted:
            self.mrp_data = self.mrp_window.get_data()

class DataFrameViewer(QDialog):
    def __init__(self, dataframes, parent=None):
        super(DataFrameViewer, self).__init__(parent)
        self.setWindowTitle("Calculated Tables")
        self.dataframes = dataframes
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        tab_widget = QTabWidget(self)
        layout.addWidget(tab_widget)

        # Create a tab for each DataFrame
        for df in self.dataframes:
            if hasattr(df, "mrp_array_lower_level"):
                for df_lower in df.mrp_array_lower_level:
                    tab = QTableWidget()
                    tab_widget.addTab(tab, f'{df_lower.name}')
                    self.populate_table_widget(tab, df_lower.data_df)
            tab = QTableWidget()
            tab_widget.addTab(tab, f'{df.name}')
            self.populate_table_widget(tab, df.data_df)

        self.setLayout(layout)
        self.resize(800, 600)

    def populate_table_widget(self, table_widget, dataframe):
        # Set table dimensions
        table_widget.setRowCount(dataframe.shape[0])
        table_widget.setColumnCount(dataframe.shape[1])
        table_widget.setVerticalHeaderLabels(dataframe.index)

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
        