from workflow import WorkFlow
from shop_info_to_vector import ShopInfoToVector
from shop_pay_count import ShopPayCount
from shop_pay_list import ShopPayList
from split_test_set import SplitTestSet
from predict_median import PredictMedian
from predict_mean import PredictMean
from validate_result import ValidateResult
from k_means_cluster_shop import KMeansClusterShop


WorkFlow() >> 'shop_info.txt' >> ShopInfoToVector(with_city=False, with_cate=True) >> 'shop_info_vector.txt'
WorkFlow() >> 'user_pay.txt' >> ShopPayCount() >> 'shop_pay_count.txt' >> ShopPayList(remind_days=245) >> 'shop_pay_list.txt'
WorkFlow() >> 'shop_pay_count_train.txt' >> ShopPayList(remind_days=245, check=False) >> 'shop_pay_list_train.txt'
WorkFlow() >> 'user_pay.txt' >> SplitTestSet(split_data='2016-10-18') >> ('user_pay_train.txt', 'test.csv')
WorkFlow() >> (WorkFlow() >> 'shop_pay_list_train.txt' >> PredictMean(train_weeks=3) >> 'mean_result_test.csv', 'test.csv') >> ValidateResult() >> None
WorkFlow() >> (WorkFlow() >> 'shop_pay_list_train.txt' >> PredictMedian(train_weeks=3) >> 'median_result_test.csv', 'test.csv') >> ValidateResult() >> None
WorkFlow() >> 'shop_pay_list.txt' >> PredictMean(train_weeks=3) >> 'mean_result.csv'
WorkFlow() >> 'shop_pay_list.txt' >> PredictMedian(train_weeks=3) >> 'median_result.csv'
WorkFlow() >> 'shop_pay_list.txt' >> KMeansClusterShop(train_weeks=3, k=100) >> 'shop_cluster.txt'
