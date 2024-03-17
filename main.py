from src.ghp import GHP
from src.mrp import MRP


def main():
    # TODO: Test values, need to be changed
    plyta_plisniowa = MRP("Płyty plisniowe",1, 10, 1, 50)
    blaty = MRP("Blaty",3, 22, 1, 40,
                [plyta_plisniowa])
    nogi = MRP("Nogi",2,40,4,120)
    ghp = GHP("Stół",1, 2, [
                        {"week": 5, "expected_demand": 20, "production": 28},
                        {"week": 7, "expected_demand": 40, "production": 30}], [blaty, nogi]
              )
    ghp.calculate_mrp()


if __name__ == "__main__":
    main()
