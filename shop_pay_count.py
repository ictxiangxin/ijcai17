import time
import tool
from workflow import Work


@tool.state
def shop_pay_count(input_path, output_path):
    date_count = {}
    user_pay_reader = tool.Reader(input_path)
    for row in user_pay_reader:
        row_time = time.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        key = (row[1], row_time.tm_year, row_time.tm_mon, row_time.tm_mday, row_time.tm_wday)
        date_count.setdefault(key, 0)
        date_count[key] += 1
    user_pay_count_writer = tool.Writer(output_path)
    for key, count in date_count.items():
        row = list(key) + [count]
        user_pay_count_writer.write_row(row)


class ShopPayCount(Work):
    def function(self):
        return shop_pay_count
