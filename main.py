from src.ghp import GHP
from src.mrp import MRP


def main():
    # TODO: Test values, need to be changed
    # długopis(wkład, obudowa(skuwka, obudowa główna))
    wkład = MRP("Wkład", 3, 10, 3, 60)
    skuwka = MRP("Skuwka", 1, 5, 1, 30)
    obudowa_część = MRP("Główna część obudowy", 2, 35, 1, 40)
    obudowa = MRP("Obudowa", 1, 5, 1, 30, [skuwka, obudowa_część])
    ghp = GHP("Długopis", 1, 15, [
                        {"week": 5, "expected_demand": 20, "production": 28},
                        {"week": 7, "expected_demand": 40, "production": 30}],
                        [wkład, obudowa])
    ghp.calculate_mrp()


if __name__ == "__main__":
    main()

