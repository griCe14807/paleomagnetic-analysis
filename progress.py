# -*- coding=utf8 =*-
import numpy as np
import math

def load_data(path):

    """
    :warning
    --------
    progressに入れるデータの形をしていることが前提（下記の通り）
    specimen名など
    消磁レベル  declination  inclination  磁化強度
    [改行]

    :parameter
    --------
    data:
    一列目: level
    二列目: declination
    三列目: inclination
    四列目: x (north)
    五列目: y (west)
    六列目: z (up)

    :return
    --------
    data_site = [{"specimen": "", "data": numpy: level*4}, {}, {}]
    のように、specimenごとのリストを作成し、各リストの中身は、
    {"specimen": サイト名などの情報, "data": 消磁段階ごとにlevel, inc, dec, strength} という辞書

    """

    # returnを定義しておく
    data_site = []

    # ファイルを開き、specimenごとに分ける
    data = open(path)
    specimens = data.read().split("\n\n")

    for specimen in specimens:
        line = specimen.split("\n")
        name = line[0]
        data = np.array([line.split('\t') for line in line[1:]])
        data = data.astype(np.float)

        # inclination, declinationからx, y, zを計算。ただし、Northをx軸正方向、Eastをy軸正方向、Upをz軸正方向とする
        dec = np.radians(data[:, 1])
        inc = np.radians(data[:, 2])

        x = (np.cos(dec) * np.cos(inc)).reshape(-1, 1)
        y = (np.sin(dec) * np.cos(inc)).reshape(-1, 1)
        z = - np.sin(inc).reshape(-1, 1)

        data = np.hstack((data, x))
        data = np.hstack((data, y))
        data = np.hstack((data, z))

        data_site.append({"specimen": name,
                          "data": data
                          })

    return data_site

def convert_trendline_to_inc_and_dec(slope_xy, slope_xz):

    dec_rad = math.atan(slope_xy)
    dec = math.degrees(dec_rad)

    inc_rad = - math.atan(slope_xz)
    inc = math.degrees(inc_rad)

    return dec, inc



if __name__ == "__main__":
    input = {"path": r'/Users/grice/Documents/古地磁気関係data/古地磁気測定データ/181229_mod_to_sibmit_islandArc/data_for_progress/raw_data/1608_TC.txt',
             "specimen": 2,
             "fit_from": 10,
             "fit_to": -1
             }

    data_site = load_data(input["path"])

    data = data_site[input["specimen"]]["data"]
    x = data[input["fit_from"]:input["fit_to"], 4]
    y = data[input["fit_from"]:input["fit_to"], 5]
    z = data[input["fit_from"]:input["fit_to"], 6]

    a, b = np.polyfit(x, y, 1, fit_intercept=False)
    c, d = np.polyfit(x, z, 1, fit_intercept=False)

    dec, inc = convert_trendline_to_inc_and_dec(a, c)
    print(data_site[input["specimen"]]["specimen"])
    print("regression from {0} to {1}".format(data[input["fit_from"], 0], data[input["fit_to"], 0]))
    print("inclination = {0}, declination = {1}".format(dec, inc))