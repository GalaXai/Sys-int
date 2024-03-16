import pandas as pd
import math
class MRP:
    def __init__(
            self,name, realization_time, nb_of_resources, resource_per_unit,
            resource_per_batch, mrp_array_lower_level=None, nb_of_weeks=10, receptions=None):
        self.name = name
        self.nb_of_weeks = nb_of_weeks
        self.realization_time = realization_time
        self.nb_of_resources = nb_of_resources
        self.resource_per_unit = resource_per_unit
        self.resource_per_batch = resource_per_batch
        self.mrp_array_lower_level = mrp_array_lower_level or []
        self.mrp_decision_array = []
        self.mrp_decision_array_lower_level = []
        self.receptions = receptions or []
        self.mrp_array = pd.DataFrame(index=[
            "Całkowite zapotrzebowanie", "Planowane przyjęcia", "Przewidywane na stanie", "Zapotrzebowanie netto",
            "Planowane zamówienia", "Planowane przyjęcie zamówień"
        ], columns=range(1, self.nb_of_weeks+1)).fillna(0)

    def calculate_mrp(self, decision_array, unit_realization_time):
        self._calculate_decision(decision_array, unit_realization_time)
        self._insert_decision()
        self._calculate_remaining_resources()
        print(self.name)
        print(self.mrp_array)
        for mrp in self.mrp_array_lower_level:
            mrp.calculate_mrp(self.mrp_decision_array_lower_level, mrp.realization_time)

    def _calculate_remaining_resources(self):
        self.mrp_array.iloc[2, 0] = (self.nb_of_resources + self.mrp_array.iloc[1, 0] + self.mrp_array.iloc[5, 0]) - self.mrp_array.iloc[0, 0]
        if self.mrp_array.iloc[2, 0] < 0: self.mrp_array.iloc[3, 0] = abs(self.mrp_array.iloc[2, 0])
        for week in range(1, self.nb_of_weeks):
            self.mrp_array.iloc[2, week] = (self.mrp_array.iloc[2, week-1]+self.mrp_array.iloc[1, week] + self.mrp_array.iloc[5, week]) - self.mrp_array.iloc[0, week]
            if self.mrp_array.iloc[2, week] < 0:
                self._calculate_order(week)
                break

    def _calculate_decision(self, decision_array, unit_realization_time):
        for decision in decision_array:
            self.mrp_decision_array.append(
                {
                    "week": decision["week"] - unit_realization_time,
                    "production": decision["production"] * self.resource_per_unit
                }
            )

    def _insert_decision(self):
        for decision in self.mrp_decision_array:
            self.mrp_array.iloc[0, decision["week"]] = decision["production"]
        for reception in self.receptions:
            self.mrp_array.iloc[1, reception["week"]] = reception["reception"]

    def _calculate_order(self, week):
        self.mrp_array.iloc[3, week] = abs(self.mrp_array.iloc[2, week])
        planning_week = week - self.realization_time
        self.mrp_array.iloc[4, planning_week] = math.ceil(
            (self.mrp_array.iloc[3, week] / self.resource_per_batch)) * self.resource_per_batch
        self.mrp_decision_array_lower_level.append(
            {
                "week": planning_week,
                "production": self.mrp_array.iloc[4, planning_week]
            }
        )
        self.mrp_array.iloc[5, week] = self.mrp_array.iloc[4, week - self.realization_time]
        self._calculate_remaining_resources()
