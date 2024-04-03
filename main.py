from src import MRPParser, GHP, MRP

def main():
    # TODO: Test values, need to be changed
    # długopis(wkład, obudowa(skuwka, obudowa główna))
    data = {"Wklad": [3, 10, 3, 60,],
           "Skuwka": [1, 5, 1, 30],
           "Główna część obudowy": [2, 35, 1, 40],
           "Obudowa":[1, 5, 1, 30, 10,["Skuwka", "Główna część obudowy"]]}
    parsed_data = MRPParser.parser(data)
    
    ghp = GHP("Długopis", 1, 15, 10,[
                        {"week": 5, "expected_demand": 20, "production": 28},
                        {"week": 7, "expected_demand": 40, "production": 30}],
                        parsed_data)
    ghp.calculate_mrp()

if __name__ == "__main__":
    main()