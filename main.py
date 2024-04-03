from src import MRPParser, GHP, MRP


def main():
    # TODO: Test values, need to be changed
    # długopis(wkład, obudowa(skuwka, obudowa główna))
    wklad = MRP("Wkład", 3, 10, 3, 60)
    skuwka = MRP("Skuwka", 1, 5, 1, 30)
    obudowa_czesc = MRP("Główna część obudowy", 2, 35, 1, 40)
    obudowa = MRP("Obudowa", 1, 5, 1, 30, mrp_array_lower_level = [skuwka, obudowa_czesc])
    ghp = GHP("Długopis", 1, 15, 10,[
                        {"week": 5, "expected_demand": 20, "production": 28},
                        {"week": 7, "expected_demand": 40, "production": 30}],
                        [wklad, obudowa])
    ghp.calculate_mrp()

def parser_main():
    data = {"Wklad": [3, 10, 3, 60,],
           "Skuwka": [1, 5, 1, 30],
           "Główna część obudowy": [2, 35, 1, 40],
           "Obudowa":[1, 5, 1, 30, 10,["Skuwka", "Główna część obudowy"]]}
    parsed_data = MRPParser.parse(data)
    print(parsed_data)

    wklad = MRP("Wkład", 3, 10, 3, 60)
    skuwka = MRP("Skuwka", 1, 5, 1, 30)
    obudowa_czesc = MRP("Główna część obudowy", 2, 35, 1, 40)
    obudowa = MRP("Obudowa", 1, 5, 1, 30, mrp_array_lower_level = [skuwka, obudowa_czesc])

    p_ghp = GHP("Długopis", 1, 15, 10,[
                        {"week": 5, "expected_demand": 20, "production": 28},
                        {"week": 7, "expected_demand": 40, "production": 30}],
                        parsed_data)
    ghp = GHP("Długopis", 1, 15, 10,[
                        {"week": 5, "expected_demand": 20, "production": 28},
                        {"week": 7, "expected_demand": 40, "production": 30}],
                        [wklad, obudowa])
    print(p_ghp.calculate_mrp() == ghp.calculate_mrp())

if __name__ == "__main__":
    #main()
    parser_main()

