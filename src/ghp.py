import pandas as pd

class GHP:
    def __init__(self,name, realization_time, nb_of_resources, ghp_decision_array, mrp_array, nb_of_weeks=10):
        self.name = name
        self.nb_of_weeks = nb_of_weeks
        self.realization_time = realization_time
        self.nb_of_resources = nb_of_resources
        self.ghp_array = pd.DataFrame(index=["Przewidywany popyt","Produkcja","Dostępne"],
                                      columns=range(0, self.nb_of_weeks)).fillna(0)
        self.ghp_decision_array = ghp_decision_array
        self.mrp_array = mrp_array
        self._calculate_gph()
        print(self.name)
        print(self.ghp_array)

    def calculate_mrp(self):
        for mrp in self.mrp_array:
            mrp.calculate_mrp(self.ghp_decision_array, self.realization_time)

    def _calculate_gph(self):
        for decision in self.ghp_decision_array:
            self._insert_decision(decision)
        self._calculate_remaining_resources()

    def _calculate_remaining_resources(self):
        self.ghp_array.iloc[2, 0] = (self.nb_of_resources + self.ghp_array.iloc[1, 0]) - self.ghp_array.iloc[0, 0]
        for week in range(1, self.nb_of_weeks):
            self.ghp_array.iloc[2, week] = (self.ghp_array.iloc[2, week-1]+self.ghp_array.iloc[1, week]) - self.ghp_array.iloc[0, week]

    def _insert_decision(self, decision):
        week = decision["week"]
        expected_demand = decision["expected_demand"]
        production = decision["production"]
        self.ghp_array.iloc[0, week] = expected_demand
        self.ghp_array.iloc[1, week] = production

