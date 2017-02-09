import tool
import datetime

shop_pay_count_train_path = tool.path('shop_pay_count_train.txt')
shop_pay_list_train_path = tool.path('shop_pay_list_train.txt')


@tool.state
def main():
    shop_pay_dict = {}
    start_date = datetime.datetime(1970, 1, 1)
    end_date = datetime.datetime(3000, 1, 1)
    shop_pay_count_reader = tool.Reader(shop_pay_count_train_path)
    for row in shop_pay_count_reader:
        shop = int(row[0])
        date = datetime.datetime(int(row[1]), int(row[2]), int(row[3]))
        shop_pay_dict.setdefault(shop, {})
        shop_pay_dict[shop][date] = row[5]
        if date < start_date:
            start_date = date
        elif date > end_date:
            end_date = date
    days = (end_date - start_date).days
    shop_pay_list_train_writer = tool.Writer(shop_pay_list_train_path)
    for shop, pay_dict in sorted(shop_pay_dict.items()):
        pay_list = []
        for d in range(days):
            current_date = start_date + datetime.timedelta(days=d)
            if current_date in pay_dict:
                pay_list.append(pay_dict[current_date])
            else:
                pay_list.append(0)
        shop_pay_list_train_writer.write_row([shop] + pay_list)


if __name__ == '__main__':
    main()
