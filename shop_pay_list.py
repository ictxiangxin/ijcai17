import tool
import datetime
import numpy
import compute

shop_pay_count_path = tool.path('shop_pay_count.txt')
shop_pay_list_path = tool.path('shop_pay_list.txt')
# shop_pay_count_path = tool.path('shop_pay_count_train.txt')
# shop_pay_list_path = tool.path('shop_pay_list_train.txt')

remind_days = 245
check = True


@tool.state
def main():
    shop_pay_dict = {}
    start_date = datetime.datetime(3000, 1, 1)
    end_date = datetime.datetime(1, 1, 1)
    shop_pay_count_reader = tool.Reader(shop_pay_count_path)
    for row in shop_pay_count_reader:
        shop = int(row[0])
        date = datetime.datetime(int(row[1]), int(row[2]), int(row[3]))
        shop_pay_dict.setdefault(shop, {})
        shop_pay_dict[shop][date] = int(row[5])
        if date < start_date:
            start_date = date
        elif date > end_date:
            end_date = date
    if remind_days != 0:
        start_date = end_date - datetime.timedelta(days=remind_days-1)
        days = remind_days
    else:
        days = (end_date - start_date).days + 1
    shop_pay_list_train_writer = tool.Writer(shop_pay_list_path)
    for shop, pay_dict in sorted(shop_pay_dict.items()):
        pay_list = []
        week_pay_list = {w: [] for w in range(7)}
        for d in range(days):
            current_date = start_date + datetime.timedelta(days=d)
            if current_date in pay_dict:
                if not check:
                    pay_list.append(pay_dict[current_date])
                week_pay_list[current_date.weekday()].append(int(pay_dict[current_date]))
            else:
                if not check:
                    pay_list.append(0)
                week_pay_list[current_date.weekday()].append(0)
        if check:
            for week, pays in sorted(week_pay_list.items()):
                sorted_pays = sorted(pays)
                if 0 in sorted_pays:
                    sorted_pays = sorted_pays[len(sorted_pays) - list(reversed(sorted_pays)).index(0):]
                mean = numpy.mean(pays)
                std = numpy.std(pays)
                median = int(compute.median(sorted_pays))
                lower = median - (mean / std) ** 0.5 * std
                upper = median + (mean / std) ** 0.5 * std
                for i, count in enumerate(pays):
                    if count < lower or count > upper:
                        pays[i] = median
                week_pay_list[week] = pays
                print("{}_{}: {} {} mean: {} median: {} std: {:.2f} a: {:.2f}".format(shop, week, pays, sorted_pays, mean, median, std, mean / std))
            pay_list = []
            for d in range(days):
                week = (start_date + datetime.timedelta(days=d)).weekday()
                pay_list.append(week_pay_list[week][d // 7])
        shop_pay_list_train_writer.write_row([shop] + pay_list)


if __name__ == '__main__':
    main()
