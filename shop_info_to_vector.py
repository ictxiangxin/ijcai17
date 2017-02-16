import tool
from workflow import Work


@tool.state
def shop_info_to_vector(input_path: str, output_path: str, with_city: bool, with_cate: bool):
    data = []
    city_set = set()
    city = {}
    cate1_set = set()
    cate1 = {}
    cate2_set = set()
    cate2 = {}
    cate3_set = set()
    cate3 = {}
    shop_info_reader = tool.Reader(input_path)
    for row in shop_info_reader:
        if row[9] == '':
            row[9] = row[8]
        if with_city:
            city_set.add(row[1])
        if with_cate:
            cate1_set.add(row[7])
            cate2_set.add(row[8])
            cate3_set.add(row[9])
        data.append(row)
    if with_city:
        city_sum = len(city_set)
        for index, city_name in zip(range(city_sum), city_set):
            city_vector = [0] * city_sum
            city_vector[index] = 1
            city[city_name] = city_vector
    if with_cate:
        cate1_sum = len(cate1_set)
        for index, cate1_name in zip(range(cate1_sum), cate1_set):
            cate1_vector = [0] * cate1_sum
            cate1_vector[index] = 1
            cate1[cate1_name] = cate1_vector
        cate2_sum = len(cate2_set)
        for index, cate2_name in zip(range(cate2_sum), cate2_set):
            cate2_vector = [0] * cate2_sum
            cate2_vector[index] = 1
            cate2[cate2_name] = cate2_vector
        cate3_sum = len(cate3_set)
        for index, cate3_name in zip(range(cate3_sum), cate3_set):
            cate3_vector = [0] * cate3_sum
            cate3_vector[index] = 1
            cate3[cate3_name] = cate3_vector
    shop_info_vector_writer = tool.Writer(output_path)
    for row in data:
        vector = [row[0]] + row[3:7]
        if with_city:
            vector += city[row[1]]
        if with_cate:
            vector += cate1[row[7]] + cate2[row[8]] + cate3[row[9]]
        shop_info_vector_writer.write_row(vector)


class ShopInfoToVector(Work):
    def function(self):
        return shop_info_to_vector
