from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QTableWidget, QTableWidgetItem, QComboBox
from PyQt5.QtCore import Qt
import sys

from src import GHP


class GHPWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GHP Calculator")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Name input
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        # Realization time input
        self.realization_label = QLabel("Realization Time (weeks):")
        self.realization_input = QLineEdit()
        self.layout.addWidget(self.realization_label)
        self.layout.addWidget(self.realization_input)

        # Number of resources input
        self.resources_label = QLabel("Number of Resources:")
        self.resources_input = QLineEdit()
        self.layout.addWidget(self.resources_label)
        self.layout.addWidget(self.resources_input)

        # Product level input
        self.level_label = QLabel("Product Level:")
        self.level_input = QLineEdit()
        self.layout.addWidget(self.level_label)
        self.layout.addWidget(self.level_input)

        # Decision inputs
        self.decision_input = []
        for i in range(2):  # Creating two sets of input fields for decision data
            week_label = QLabel(f"Choose week:")
            week_combo = QComboBox()
            week_combo.addItems([str(x) for x in range(1, 11)])
            expected_demand_label = QLabel("Expected Demand:")
            expected_demand_input = QLineEdit()
            production_label = QLabel("Production:")
            production_input = QLineEdit()
            self.layout.addWidget(week_label)
            self.layout.addWidget(week_combo)
            self.layout.addWidget(expected_demand_label)
            self.layout.addWidget(expected_demand_input)
            self.layout.addWidget(production_label)
            self.layout.addWidget(production_input)
            self.decision_input.append((week_combo, expected_demand_input, production_input))

        # Calculate button
        self.calculate_button = QPushButton("Calculate GHP")
        self.calculate_button.clicked.connect(self.calculate_ghp)
        self.layout.addWidget(self.calculate_button)

        # Result table
        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

    def calculate_ghp(self):
        name = self.name_input.text()
        realization_time = int(self.realization_input.text())
        nb_of_resources = int(self.resources_input.text())

        # Prepare GHP decision list from user interface
        ghp_decision_array = []
        for week, (week_combo, expected_demand_input, production_input) in enumerate(self.decision_input, start=1):
            week_index = int(week_combo.currentText()) - 1  # Adjust index to start from 0
            expected_demand = int(expected_demand_input.text())
            production = int(production_input.text())
            ghp_decision_array.append(
                {"week": week_index, "expected_demand": expected_demand, "production": production})

        # Create GHP instance with user-input data
        ghp_calculator = GHP(name, realization_time, nb_of_resources, ghp_decision_array=ghp_decision_array)

        # Set GHP calculation results in the result table
        ghp_result_df = ghp_calculator.ghp_df
        self.result_table.setRowCount(ghp_result_df.shape[0])
        self.result_table.setColumnCount(ghp_result_df.shape[1])

        row_labels = ["Expected Demand", "Production", "In Stock"]
        self.result_table.setVerticalHeaderLabels(row_labels)

        for i in range(ghp_result_df.shape[0]):
            for j in range(ghp_result_df.shape[1]):
                item = QTableWidgetItem(str(ghp_result_df.iloc[i, j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.result_table.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GHPWindow()
    window.show()
    sys.exit(app.exec_())
