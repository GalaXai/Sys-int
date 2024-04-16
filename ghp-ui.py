from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QTableWidget, QTableWidgetItem, QComboBox, QSpinBox
from PyQt5.QtCore import Qt
import sys
from src import GHP


class GHPWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # TODO improve the appearance of the interface
        self.setWindowTitle("GHP Calculator")
        self.setGeometry(100, 100, 600, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Name input
        self.name_label = QLabel("Name:")
        self.name = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name)

        # Realization time input
        self.realization_label = QLabel("Realization Time (weeks):")
        self.realization_time = QLineEdit()
        self.layout.addWidget(self.realization_label)
        self.layout.addWidget(self.realization_time)

        # Number of resources input
        self.resources_label = QLabel("Number of Resources:")
        self.nb_of_resources = QLineEdit()
        self.layout.addWidget(self.resources_label)
        self.layout.addWidget(self.nb_of_resources)

        # Decision inputs refactored as a list of dictionaries
        self.decision_inputs = []
        for _ in range(2):
            entry = {
                'week': {'label': QLabel(f"Choose week:"), 'input': QSpinBox()},
                'expected_demand': {'label': QLabel("Expected Demand:"), 'input': QSpinBox()},
                'production': {'label': QLabel("Production:"), 'input': QSpinBox()}
            }
            entry['week']['input'].setRange(1, 10)  # Assuming weeks range from 1 to 10
            for key in entry:
                self.layout.addWidget(entry[key]['label'])
                self.layout.addWidget(entry[key]['input'])
            self.decision_inputs.append(entry)
        # TODO add a way to add more entries

        # Default values
        # TODO remove later this is only for testing
        self.name.setText("Dlugopis")
        self.realization_time.setText("1")
        self.nb_of_resources.setText("15")

        self.decision_inputs[0]['week']['input'].setValue(5)
        self.decision_inputs[0]['expected_demand']['input'].setValue(20)
        self.decision_inputs[0]['production']['input'].setValue(28)

        self.decision_inputs[1]['week']['input'].setValue(7)
        self.decision_inputs[1]['expected_demand']['input'].setValue(40)
        self.decision_inputs[1]['production']['input'].setValue(30)

        # Calculate button
        self.calculate_button = QPushButton("Calculate GHP")
        self.calculate_button.clicked.connect(self.calculate_ghp)
        self.layout.addWidget(self.calculate_button)

        # Result table
        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

    def collect_data(self):
        data = {
            'name': self.name.text(),
            'realization_time': int(self.realization_time.text()),
            'nb_of_resources': int(self.nb_of_resources.text()),
        }

        # Add default number of weeks if not present.
        data.setdefault('nb_of_weeks', 10)  # TODO change 10 -> nb_of_weeks

        # Populate decision array with converted integer values.
        data['ghp_decision_array'] = [
            {k: v['input'].value() for k, v in decision.items()}
            for decision in self.decision_inputs
        ]

        return data

    def calculate_ghp(self):
        data = self.collect_data()
        print(data)
        ghp = GHP(**data)

        ghp_data = ghp.ghp_df
        rows, columns = ghp_data.shape
        self.result_table.setRowCount(rows)
        self.result_table.setColumnCount(columns)
        self.result_table.setVerticalHeaderLabels(["Expected Demand", "Production", "In Stock"])

        for i in range(rows):
            for j in range(columns):
                item = QTableWidgetItem(str(ghp_data.iloc[i, j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.result_table.setItem(i, j, item)

    # TODO clear_form method


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GHPWindow()
    window.show()
    sys.exit(app.exec_())
