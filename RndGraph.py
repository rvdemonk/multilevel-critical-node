"""
Object structure for graph instance to be used in MCNv2.
"""
import os


class RndGraph:
    folder = "./Instances/tables_MNC/"

    def __init__(self, N, density, Budgets):
        self.N = N
        self.density = density
        self.Budgets = Budgets
        self.Omega, self.Phi, self.Lambda = Budgets
        self._validate()

    def _validate(self):
        name = self.filename
        if not os.path.isdir(folder + name + "/" + name):
            print(f"{name} is is not a recognised graph structure")
        return

    @property
    def filename(self):
        density = f"0{self.density}" if int(self.density) < 10 else self.density
        return f"rndgraph{density}-{self.N}_{self.Omega}-{self.Phi}-{self.Lambda}"

    @property
    def data(self, number):
        name = self.filename
        if os.path.isfile(folder + name + "/" + name + "_" + number):
            V = range(1, N + 1)
            with open(folder + name + "/" + name + "_" + number) as searchfile:
                for line in searchfile:
                    if "A =" in line:
                        A = eval(line[4:])
        else:
            raise Exception(f"no graph with name {name} in folder {folder+name}")
        return V, A

    def get_paper_results(self, number):
        stats = {}
        name = self.filename
        if os.path.isfile(folder + name + "/" + name + "_" + number):
            with open(folder + name + "/" + name + "_" + number) as searchfile:
                for line in searchfile:
                    if "#opt" in line:
                        if "optDA-AD" not in line:
                            stats["solution"] = int(line.split(" ")[0])
                    if "#totTm" in line:
                        stats["time"] = float(line.split(" ")[0])
                    if "#fail" in line:
                        stats["fail"] = line.split(" ")[0]
                    if "Z_dad" in line:
                        stats["Z_sol"] = eval(line.split(" = ")[1])
                    if "Y_dad" in line:
                        stats["Y_sol"] = eval(line.split(" = ")[1])
                    if "X_dad" in line:
                        stats["X_sol"] = eval(line.split(" = ")[1])
                    if "lastADTm" in line:
                        stats["last_AD_time"] = float(line.split(" ")[0])
        else:
            raise Exception(f"no graph with name {name} in folder {folder+name}")
        return stats
