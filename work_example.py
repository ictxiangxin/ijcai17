from workflow import WorkFlow
from shop_info_to_vector import ShopInfoToVector
from shop_pay_count import ShopPayCount
from shop_pay_list import ShopPayList
from split_test_set import SplitTestSet

WorkFlow() >> 'shop_info.txt' >> ShopInfoToVector() >> 'shop_info_vector.txt'
WorkFlow() >> 'user_pay.txt' >> ShopPayCount() >> 'shop_pay_count.txt' >> ShopPayList(remind_days=245) >> 'shop_pay_list.txt'
WorkFlow() >> 'user_pay.txt' >> SplitTestSet(split_data='2016-10-18') >> ('user_pay_train.txt', 'test.csv')
