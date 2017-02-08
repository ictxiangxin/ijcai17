import time
import tool

user_pay_path = tool.path('user_pay.txt')
user_pay_count_path = tool.path('user_pay_count.txt')

if __name__ == '__main__':
    date_count = {}
    csv_reader = tool.Reader(user_pay_path)
    for row in csv_reader:
        row_time = time.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        key = (row[1], row_time.tm_year, row_time.tm_mon, row_time.tm_mday, row_time.tm_wday)
        date_count.setdefault(key, 0)
        date_count[key] += 1
    csv_writer = tool.Writer(user_pay_count_path)
    for key, count in date_count.items():
        row = list(key) + [count]
        csv_writer.write(row)
