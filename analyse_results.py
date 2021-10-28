import pandas as pd
from helpers import *
import os


def compile_average_results():
    data = {
        "name": [],
        "N": [],
        "density": [],
        "Budgets": [],
        "avg v2 sol time": [],
        "avg og sol time": [],
        "avg v2 success": [],
        "avg og success": [],
        "avg v2 time diff": [],
    }
    for folder in os.listdir(RESULTS_PATH):
        graphname = folder
        path = os.listdir(RESULTS_PATH + folder)[-1]
        if ".csv" in RESULTS_PATH + folder + "/" + path:
            # for each dataset of graph results
            results = pd.read_csv(RESULTS_PATH + folder + "/" + path)
            N, density, Budgets = extract_rndgraph_param(graphname)
            data["name"].append(graphname)
            data["N"].append(N)
            data["density"].append(density)
            data["Budgets"].append(Budgets)
            totalTime = 0
            cnt = 0
            for entry in results["v2 time"].items():
                time = entry[1]
                if not pd.isnull(time):
                    totalTime += time
                    cnt += 1
            avgTime = round(totalTime / cnt, 2)
            data["avg v2 sol time"].append(avgTime)
            data["avg v2 success"].append(cnt / 20)
            totalTime = 0
            ogcnt = 0
            for entry in results["og time"].items():
                time = entry[1]
                if not pd.isnull(time):
                    totalTime += time
                    ogcnt += 1
            data["avg og success"].append(ogcnt / 20)
            OGavgTime = round(totalTime / ogcnt, 2)
            data["avg og sol time"].append(OGavgTime)
            timeDif = round(avgTime - OGavgTime, 2)
            data["avg v2 time diff"].append(timeDif)
    df = pd.DataFrame(data).to_csv("./results_summary.csv")
    return data


def main():
    compile_average_results()


if __name__ == "__main__":
    main()
