from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QTableWidget, QTableWidgetItem, QSpinBox, QFrame, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src import GHP,MRPParser
from src.mrp_ui import MRPProductManager, DataFrameViewer, SpinBoxConf

class GHPWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GHP Calculator")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # QpyQt5 Widgets
        self.name_label = QLabel("Name:")
        self.name = QLineEdit()
        self.realization_label = QLabel("Realization Time (weeks):")
        self.realization_time = SpinBoxConf()
        self.resources_label = QLabel("Number of Resources:")
        self.nb_of_resources = SpinBoxConf()

        self.mrp_button = QPushButton("Open MRP Manager")
        self.mrp_button.clicked.connect(self.open_mrp_manager)

        self.calculate_button = QPushButton("Calculate GHP")
        self.calculate_button.clicked.connect(self.calculate_ghp)
        #self.result_table = QTableWidget()  


        # Assembling the layout
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.realization_label)
        self.layout.addWidget(self.realization_time)
        self.layout.addWidget(self.resources_label)
        self.layout.addWidget(self.nb_of_resources)

        self.layout.addWidget(self.mrp_button)
        self.layout.addWidget(self.calculate_button)

        
        self.decision_inputs = []

        # Add initial set of inputs
        self.add_new_inputs()
        # Button to save the inputs
        self.saveButton = QPushButton('Save Productions', self)
        self.saveButton.clicked.connect(self.save_inputs)
        self.layout.addWidget(self.saveButton)
        

        ## VARIABLES
        if not hasattr(self, 'mrp_data'):
            self.mrp_data = None
        if not hasattr(self, 'ghp_array'):
            self.ghp_array = [{'week': 0, 'expected_demand': 0, 'production': 0}] # default value
        
        # Default values
        self.name.setText("Dlugopis")
        self.realization_time.setValue(1)
        self.nb_of_resources.setValue(15)
        self.mrp_window = MRPProductManager()
        

    def add_new_inputs(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(divider)

        entry = {
            'week': {'label': QLabel("Choose week:"), 'input': SpinBoxConf()},
            'expected_demand': {'label': QLabel("Expected Demand:"), 'input': SpinBoxConf()},
            'production': {'label': QLabel("Production:"), 'input': SpinBoxConf()}
        }

        self.layout.addWidget(QLabel("Production Input"))
        for key in entry:
            self.layout.addWidget(entry[key]['label'])
            self.layout.addWidget(entry[key]['input'])

        self.decision_inputs.append(entry)

    def save_inputs(self):
        # Implement the save logic here
        # For now, just print the values to check
        for entry in self.decision_inputs:
            data = {key: entry[key]['input'].value() for key in entry}
            print(data)
            self.ghp_array.append(data)

        # Optionally clear inputs after saving
        self.clear_inputs()

    def clear_inputs(self):
        for entry in self.decision_inputs:
            for key in entry:
                entry[key]['input'].setValue(0)  # Reset spin boxes to 0

    def open_mrp_manager(self):
        self.mrp_window.show()
        self.mrp_window.exec_()  # Assuming modal usage
        self.mrp_data = self.mrp_window.get_data()  # Store the data when window closes
        print("MRP Data Retrieved:", self.mrp_data)  # Debug output
    
    
    def collect_data(self):
        data = {
            'name': self.name.text(),
            'realization_time': self.realization_time.value(),
            'nb_of_resources': self.nb_of_resources.value(),
        }

        # Find the maximum number of weeks from the decision array
        max_weeks = max([decision['week'] for decision in self.ghp_array]) + 2 # 2 Looks better than 1
        
        data.setdefault('nb_of_weeks', max_weeks)

        # Populate decision array with converted integer values.
        data['ghp_decision_array'] = self.ghp_array

        return data

    def calculate_ghp(self):
        ghp_data = self.collect_data()
        
        if self.mrp_data:    
            # parsing number of weeks to mrp_data
            
            for _, mrp_object_data in self.mrp_data.items():
                max_weeks = ghp_data['nb_of_weeks']
                if len(mrp_object_data) < 7:
                    mrp_object_data.insert(4, max_weeks)
                else:
                    # Ensures we are not out of bounds
                    mrp_object_data[4] = max_weeks

            try:
                mrp_data = MRPParser.parse(self.mrp_data)                
                print(mrp_data)
            except ValueError as e:
                self.show_warning(str(e))
                return
        else: mrp_data = None
        
        print(ghp_data)
        ghp = GHP(**ghp_data, mrp_array=mrp_data)
        if mrp_data: 
            try:
                ghp.calculate_mrp()
            except IndexError:
                self.show_warning("The MRP data is incomplete. Please check the input data.")
                return
            
        # Display the Calculated Tables
        if ghp.mrp_array:
            viewer = DataFrameViewer([ghp,*ghp.mrp_array])
        else:
            viewer = DataFrameViewer([ghp])
        viewer.exec_()

    def show_warning(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()