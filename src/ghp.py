import pandas as pd

class GHP:
    def __init__(self,name, realization_time, nb_of_resources, ghp_decision_array, mrp_array, nb_of_weeks=10):
        """
        :param name: Name of the GHP product
        :param realization_time: Time of realization of the product in weeks
        :param nb_of_resources: Number of resources available before the start of the production
        :param ghp_decision_array:  List of decisions for the GHP, decision need to be in format:
        {"week": week, "expected_demand": number_of_expected_demand, "production": number_of_production}
        :param mrp_array: List of lower level MRP products
        :param nb_of_weeks: Number of weeks for which the GHP will be calculated
        """
        self.name = name
        self.realization_time = realization_time
        self.nb_of_resources = nb_of_resources
        self.ghp_df = pd.DataFrame(index=["Przewidywany popyt","Produkcja","Dostępne"],
                                      columns=range(0, self.nb_of_weeks)).fillna(0)
        self.ghp_decision_array = ghp_decision_array
        self.mrp_array = mrp_array
        self.nb_of_weeks = nb_of_weeks
        self._calculate_gph()
        # TODO :Test prints, need to be changed
        print(self.name)
        print(self.ghp_df)

    def calculate_mrp(self):
        """
        Calculate lower level MRP`s products for the GHP
        :return:
        """
        for mrp_object in self.mrp_array:
            mrp_object.calculate_mrp(self.ghp_decision_array, self.realization_time)

    def _calculate_gph(self):
        """
        Calculate GHP
        :return:
        """
        for decision in self.ghp_decision_array:
            self._insert_decision(decision)
        self._calculate_remaining_resources()

    def _calculate_remaining_resources(self):
        """
        Calculate remaining resources for GHP based on decisions
        :return:
        """
        self.ghp_df.iloc[2, 0] = (self.nb_of_resources + self.ghp_df.iloc[1, 0]) - self.ghp_df.iloc[0, 0]
        for week in range(1, self.nb_of_weeks):
            self.ghp_df.iloc[2, week] = (self.ghp_df.iloc[2, week-1]+self.ghp_df.iloc[1, week]) - self.ghp_df.iloc[0, week]

    def _insert_decision(self, decision):
        """
        Insert decision to GHP DataFrame
        :param decision: should be in format:
         {"week": week, "expected_demand": number_of_expected_demand, "production": number_of_production}
        :return:
        """
        week = decision["week"]
        expected_demand = decision["expected_demand"]
        production = decision["production"]
        self.ghp_df.iloc[0, week] = expected_demand
        self.ghp_df.iloc[1, week] = production

