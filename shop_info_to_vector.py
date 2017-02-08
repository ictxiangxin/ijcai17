import tool

shop_info_path = tool.path('shop_info.txt')
shop_info_vector_path = tool.path('shop_info_vector.txt')

if __name__ == '__main__':
    data = []
    city_set = set()
    city_to_vector = {}
    cate1_set = set()
    cate1_to_vector = {}
    cate2_set = set()
    cate2_to_vector = {}
    cate3_set = set()
    cate3_to_vector = {}
    csv_reader = tool.Reader(shop_info_path)
    for row in csv_reader:
        if row[9] == '':
            row[9] = row[8]
        city_set.add(row[1])
        cate1_set.add(row[7])
        cate2_set.add(row[8])
        cate3_set.add(row[9])
        data.append(row)
    city_sum = len(city_set)
    for index, city_name in zip(range(city_sum), city_set):
        city_vector = [0] * city_sum
        city_vector[index] = 1
        city_to_vector[city_name] = city_vector
    cate1_sum = len(cate1_set)
    for index, cate1_name in zip(range(cate1_sum), cate1_set):
        cate1_vector = [0] * cate1_sum
        cate1_vector[index] = 1
        cate1_to_vector[cate1_name] = cate1_vector
    cate2_sum = len(cate2_set)
    for index, cate2_name in zip(range(cate2_sum), cate2_set):
        cate2_vector = [0] * cate2_sum
        cate2_vector[index] = 1
        cate2_to_vector[cate2_name] = cate2_vector
    cate3_sum = len(cate3_set)
    for index, cate3_name in zip(range(cate3_sum), cate3_set):
        cate3_vector = [0] * cate3_sum
        cate3_vector[index] = 1
        cate3_to_vector[cate3_name] = cate3_vector
    csv_writer = tool.Writer(shop_info_vector_path)
    for row in data:
        vector = row[3:7] +\
                 city_to_vector[row[1]] +\
                 cate1_to_vector[row[7]] +\
                 cate2_to_vector[row[8]] +\
                 cate3_to_vector[row[9]]
        csv_writer.write(vector)
