import tool
from sklearn.cluster import KMeans
from workflow import Work


@tool.state
def k_means_cluster_shop(shop_pay_list_path: str, cluster_path: str, train_weeks: int, k: int):
    shop_pay_list_reader = tool.Reader(shop_pay_list_path)
    result_writer = tool.Writer(cluster_path)
    shop_list = []
    rate = []
    for row in shop_pay_list_reader:
        shop = int(row[0])
        shop_list.append(shop)
        pay_list = row[-train_weeks * 3:]
        extern = [pay_list[0]] + pay_list
        rate_list = [(int(extern[i + 1]) / int(extern[i]) if int(extern[i]) != 0 else 0) for i in range(len(pay_list))]
        rate.append(rate_list)
    group = [[] for _ in range(k)]
    k_means = KMeans(n_clusters=k).fit(rate)
    for s, c in enumerate(k_means.labels_):
        group[c].append(shop_list[s])
    for shops in group:
        result_writer.write_row(shops)


class KMeansClusterShop(Work):
    def function(self):
        return k_means_cluster_shop
