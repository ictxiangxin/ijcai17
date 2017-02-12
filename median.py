import tool
import compute

user_pay_count_path = tool.path('shop_pay_list.txt')
result_path = tool.path('median_result.csv')
# user_pay_count_path = tool.path('shop_pay_list_train.txt')
# result_path = tool.path('median_test_result.csv')

train_days = 35


@tool.state
def main():
    shop_pay_list_reader = tool.Reader(user_pay_count_path)
    result_writer = tool.Writer(result_path)
    for row in shop_pay_list_reader:
        pay_list = row[-train_days:]
        pay_list.reverse()
        result = []
        for d in range(7):
            week_pays = [pay_list[-d + (w + 1) * 7 - 1] for w in range(train_days // 7)]
            m = compute.median(week_pays)
            result.append(m)
        result *= 2
        result_writer.write_row([row[0]] + result)


if __name__ == '__main__':
    main()
