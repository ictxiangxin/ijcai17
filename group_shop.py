import tool
from sklearn.cluster import KMeans

# shop_pay_list_path = tool.path('shop_pay_list.txt')
# group_path = tool.path('group.txt')
shop_pay_list_path = tool.path('shop_pay_list_train.txt')
group_path = tool.path('group_train.txt')

train_days = 28


def main():
    shop_pay_list_reader = tool.Reader(shop_pay_list_path)
    result_writer = tool.Writer(group_path)
    shop_list = []
    rate = []
    for row in shop_pay_list_reader:
        shop = int(row[0])
        shop_list.append(shop)
        pay_list = row[-train_days:]
        extern = [pay_list[0]] + pay_list
        rate_list = [(int(extern[i + 1]) / int(extern[i]) if int(extern[i]) != 0 else 0) for i in range(len(pay_list))]
        rate.append(rate_list)
    n = 100
    group = {c: [] for c in range(n)}
    kmeans = KMeans(n_clusters=n).fit(rate)
    for s, c in enumerate(kmeans.labels_):
        group[c].append(shop_list[s])
    for _, shops in group.items():
        result_writer.write_row(shops)

if __name__ == '__main__':
    main()
