import tool
import datetime
from workflow import Work


@tool.state
def shop_pay_list(shop_pay_count_path: str, shop_pay_list_path: str, remind_days: int):
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
                pay_list.append(pay_dict[current_date])
                week_pay_list[current_date.weekday()].append(int(pay_dict[current_date]))
            else:
                pay_list.append(0)
                week_pay_list[current_date.weekday()].append(0)
        shop_pay_list_train_writer.write_row([shop] + pay_list)


class ShopPayList(Work):
    def function(self):
        return shop_pay_list
