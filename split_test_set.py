import time
import datetime
import tool
import configure
from workflow import Work


@tool.state
def split_test_set(user_pay_path: str, user_pay_train_path: str, test_path: str, split_data: str):
    date_count = {}
    day_pays = {}
    user_pay_reader = tool.Reader(user_pay_path)
    user_pay_train_writer = tool.Writer(user_pay_train_path)
    test_writer = tool.Writer(test_path)
    split_time = time.strptime(split_data, '%Y-%m-%d')
    split_datetime = datetime.datetime(split_time.tm_year, split_time.tm_mon, split_time.tm_mday)
    for row in user_pay_reader:
        row_time = time.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        if row_time.tm_year >= split_time.tm_year and row_time.tm_mon >= split_time.tm_mon and row_time.tm_mday >= split_time.tm_mday:
            key = (row[1], row_time.tm_year, row_time.tm_mon, row_time.tm_mday)
            date_count.setdefault(key, 0)
            date_count[key] += 1
        else:
            user_pay_train_writer.write_row(row)
    for key, count in date_count.items():
        shop = int(key[0])
        day_pays.setdefault(shop, {d: 0 for d in range(configure.predict_weeks)})
        for d in range(configure.predict_weeks):
            current_datetime = datetime.datetime(*key[1:])
            day_difference = (current_datetime - split_datetime).days
            if day_difference < configure.predict_weeks:
                day_pays[shop][day_difference] = count
    for shop, pays in sorted(day_pays.items()):
        row = [shop] + [p for _, p in sorted(pays.items())]
        test_writer.write_row(row)


class SplitTestSet(Work):
    def function(self):
        return split_test_set
