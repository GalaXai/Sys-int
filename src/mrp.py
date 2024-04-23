import pandas as pd
import math

class MRP:
    def __init__(
            self, name: str, realization_time: int, nb_of_resources: int, resource_per_unit: int,
            resource_per_batch: int, nb_of_weeks: int = 10, mrp_array_lower_level: list = None, receptions: list[dict[str, int]] = None) -> None:
        """
        :param name: Name of the MRP product
        :param realization_time: Time of realization of the product in weeks
        :param nb_of_resources: Number of resources available before the start of the production
        :param resource_per_unit: Number of resources needed to produce one final product
        :param resource_per_batch: Number of resources in one batch
        :param nb_of_weeks: Number of weeks for which the MRP will be calculated
        :param mrp_array_lower_level: List of lower level MRP products
        :param receptions: List of receptions before the start of the production, reception need to be in format:
        {"week": week, "reception": number_of_reception}
        """
        self.name = name
        self.realization_time = realization_time
        self.nb_of_resources = nb_of_resources
        self.resource_per_unit = resource_per_unit
        self.resource_per_batch = resource_per_batch
        self.mrp_array_lower_level = mrp_array_lower_level or []
        self.mrp_decision_array = []
        self.mrp_decision_array_lower_level = []
        self.nb_of_weeks = nb_of_weeks
        self.receptions = receptions or []
        self.data_df = pd.DataFrame(index=[
            "Gross Req", "Scheduled Receipts", "Projected On Hand", "Net Requirements",
            "Planned Receipts", "Planned Order Release"
        ], columns=range(1, self.nb_of_weeks+1)).infer_objects(copy=False).fillna(0).astype('int')

    def calculate_mrp(self, decision_array : list[dict[str, int]], unit_realization_time: int) -> None:
        """
        Calculate MRP
        :param decision_array: List of decisions for the MRP, decision need to be in format:
        {"week": week, "production": number_of_production}
        :param unit_realization_time: Realization time of the higher level MRP product
        :return:
        """
        self._calculate_decision(decision_array, unit_realization_time)
        self._insert_decision()
        self._calculate_remaining_resources()
        # TODO: Test prints, need to be changed
        print(self.name)
        print(self.data_df, end="\n\n")
        for mrp in self.mrp_array_lower_level:
            mrp.calculate_mrp(self.mrp_decision_array_lower_level, mrp.realization_time)

    def _calculate_remaining_resources(self) -> None:
        """
        Calculate remaining resources for MRP based on decisions
        :return:
        """
        self.data_df.iloc[2, 0] = (self.nb_of_resources + self.data_df.iloc[1, 0] + self.data_df.iloc[5, 0]) - self.data_df.iloc[0, 0]
        if self.data_df.iloc[2, 0] < 0: self.data_df.iloc[3, 0] = abs(self.data_df.iloc[2, 0])
        for week in range(1, self.nb_of_weeks):
            self.data_df.iloc[2, week] = (self.data_df.iloc[2, week-1]+self.data_df.iloc[1, week] + self.data_df.iloc[5, week]) - self.data_df.iloc[0, week]
            if self.data_df.iloc[2, week] < 0:
                self._calculate_order(week)
                break

    def _calculate_decision(self, decision_array :list[dict[str, int]], unit_realization_time: int) -> None:
        """
        Calculate decision for MRP product based on higher level MRP product and insert to mrp_decision_array
        :param decision_array: Decision array for higher level MRP product, decision need to be in format:
        {"week": week, "production": number_of_production}
        :param unit_realization_time: Realization time of the higher level MRP product
        :return:
        """
        for decision in decision_array:
            calculated_week = decision["week"] - unit_realization_time
            if calculated_week < 0: calculated_week = 0
            self.mrp_decision_array.append(
                {
                    "week": calculated_week,
                    "production": decision["production"] * self.resource_per_unit
                }
            )

    def _insert_decision(self) -> None:
        """
        Insert decision to MRP DataFrame
        :return:
        """
        for decision in self.mrp_decision_array:
            self.data_df.iloc[0, decision["week"]] = decision["production"]
        for reception in self.receptions:
            self.data_df.iloc[1, reception["week"]] = reception["reception"]

    def _calculate_order(self, week: int) -> None:
        """
        Calculate order for necessary MRP product when there is not enough resources
        :param week: Week when the order needs to be delivered
        :return:
        """
        self.data_df.iloc[3, week] = abs(self.data_df.iloc[2, week])
        planning_week = week - self.realization_time
        if planning_week < 0: return
        self.data_df.iloc[4, planning_week] = math.ceil(
            (self.data_df.iloc[3, week] / self.resource_per_batch)) * self.resource_per_batch
        self.mrp_decision_array_lower_level.append(
            {
                "week": planning_week,
                "production": self.data_df.iloc[4, planning_week]
            }
        )
        self.data_df.iloc[5, week] = self.data_df.iloc[4, week - self.realization_time]
        self._calculate_remaining_resources()
