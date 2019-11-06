import csv

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



def topN_hottest_coldest(dataset, city, topN):
    data_of_city = [dataset[AVG_TMP_INDEX][i] for i, c in enumerate(dataset[CITY_INDEX]) if c.lower() == city.lower()]
    data_of_city.sort(reverse=True)

    print(f"Top {topN} hottest measurements for {city}:")
    print(data_of_city[:topN])

    print(f"\nTop {topN} coldest measurements for {city}:")
    print(data_of_city[len(data_of_city)-1 : len(data_of_city)-(topN+1) : -1])


def dataset_to_file(dataset, path):
    with open(path, 'w'):
        for i in range(len(dataset[0])):
            for j in range(len(dataset)):
                pass


if __name__ == '__main__':
    # 1.
    dataset = csv2list("data_sets/glt.csv")

    # 2.
    fill_empty_fields(dataset[CITY_INDEX], dataset[AVG_TMP_INDEX])
    fill_empty_fields(dataset[CITY_INDEX], dataset[AVG_TMP_U_INDEX])
    # test(dataset)
    dataset_to_file(dataset, "data_sets/glt_complete.csv")

    # 3.
    # topN_hottest_coldest(dataset, dataset[CITY_INDEX][0], 1000)
