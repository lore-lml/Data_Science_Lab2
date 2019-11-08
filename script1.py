import csv
import matplotlib.pyplot as plt
import numpy as np

header = ""
AVG_TMP_INDEX = 1
AVG_TMP_U_INDEX = 2
CITY_INDEX = 3


def csv2list(path):

    with open(path, encoding='utf8') as glt:
        global header
        reader = csv.reader(glt)
        header = next(reader)
        n_cols = len(header)
        dataset = [[] for i in range(n_cols)]
        for row in reader:
            if len(row) != n_cols:
                continue
            for i, e in enumerate(row):
                dataset[i].append(e)

        return dataset


def test(dataset):
    for i in range(35, 83):
        for j in range(len(dataset)):
            print(dataset[j][i], end=" ")
        print()


def fill_empty_fields(cities, avg_tmp):

    right = 0
    consecutive = 0
    for i, c in enumerate(cities):
        # se l'elemento corrente non è vuoto allora converto solo da stringa a float
        if avg_tmp[i] != '':
            avg_tmp[i] = float(avg_tmp[i])
            consecutive = 0
            continue

        # se l'elemento corrente è vuoto allora controllo se sia primo ...
        if i == 0 or cities[i] != cities[i-1]:
            left = 0
        else:
            left = float(avg_tmp[i-1])

        # ... o ultimo
        if i == len(cities) - 1 or cities[i] != cities[i+1]:
            right = 0
        # se ci sono più campi vuoti consecutivi
        elif consecutive > 0:
            consecutive -= 1
        elif avg_tmp[i+1] == '':
            found = False
            for j in range(i+1, len(cities)):
                if avg_tmp[j] != '':
                    right = float(avg_tmp[j])
                    found = True
                    break
                consecutive += 1

            if not found:
                right = 0
        else:
            right = float(avg_tmp[i+1])

        avg_tmp[i] = (left + right) / 2


def topn_hottest_coldest(dataset, city, topN):
    data_of_city = [dataset[AVG_TMP_INDEX][i] for i, c in enumerate(dataset[CITY_INDEX]) if c.lower() == city.lower()]
    data_of_city.sort(reverse=True)

    print(f"Top {topN} hottest measurements for {city}:")
    print(data_of_city[:topN])

    print(f"\nTop {topN} coldest measurements for {city}:")
    print(data_of_city[len(data_of_city)-1 : len(data_of_city)-(topN+1) : -1])


def dataset2csv(dataset, path):
    with open(path, 'w', encoding='utf8') as fp:
        fp.write(f"{','.join(header)}\n")

        for i in range(len(dataset[0])):
            row = []
            for j in range(len(dataset)):
                row.append(str(dataset[j][i]))
            fp.write(f'{",".join(row)}\n')


def get_avg_tmp(city, dataset):
    return [dataset[AVG_TMP_INDEX][i] for i in range(len(dataset[CITY_INDEX])) if dataset[CITY_INDEX][i].lower() == city.lower()]


def plot_avg_tmp(cities):

    print()
    for c, array in cities.items():
        plt.hist(array, label=c)
        print(f"{c}: Average = {np.array(array).mean():.2f}; Std Dev = {np.array(array).std():.2f}")
    plt.legend()
    _ = plt.xlabel('AverageTemperature')
    plt.show()


# TF=1.8⋅TC+32 -> TC = (TF-32)/1.8
def farhenheit2celsius(array):
    return list(map(lambda x: (float(x)-32)/1.8, array))


if __name__ == '__main__':
    # 1.
    dataset = csv2list("data_sets/glt.csv")

    # 2.
    fill_empty_fields(dataset[CITY_INDEX], dataset[AVG_TMP_INDEX])
    fill_empty_fields(dataset[CITY_INDEX], dataset[AVG_TMP_U_INDEX])
    # test(dataset)
    # dataset2csv(dataset, "data_sets/glt_complete.csv")

    # 3.
    topn_hottest_coldest(dataset, "Rome", 5)

    # 4.
    plot_avg_tmp({"Rome": get_avg_tmp("Rome", dataset),
                  "Bangkok": get_avg_tmp("Bangkok", dataset)})

    # 5.
    plot_avg_tmp({"Rome": get_avg_tmp("Rome", dataset),
                  "Bangkok": farhenheit2celsius(get_avg_tmp("Bangkok", dataset))})