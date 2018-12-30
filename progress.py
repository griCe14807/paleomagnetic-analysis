# -*- coding=utf8 =*-
import pandas as pd
import numpy as np


if __name__ == "__main__":
    # read data
    data = open(r'/Users/grice/Documents/古地磁気関係data/古地磁気測定データ/181229_mod_to_sibmit_islandArc/data_for_progress/raw_data/16PILOT1_IS.txt')
    specimens = data.read().split("\n\n")
    data_site = []
    for specimen in specimens:
        line = specimen.split("\n")
        name = line[0]
        data = np.array([line.split('\t') for line in line[1:]])
        data = data.astype(np.float)
        data_site.append({"site": name,
                          "data": data
                          })

    data = data_site[0]["data"]
    inclination = data[:, 1]
    declination = data[:, 2]
    a, b = np.polyfit(inclination, declination, 1, fit_intercept=False)
    print(a, b)
