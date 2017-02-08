import time
import tool

user_pay_path = tool.path('user_pay.txt')
user_pay_train_path = tool.path('user_pay_train.txt')
test_path = tool.path('test.csv')

split_data = '2016-10-18'


@tool.state
def main():
    date_count = {}
    user_pay_reader = tool.Reader(user_pay_path)
    user_pay_train_writer = tool.Writer(user_pay_train_path)
    test_writer = tool.Writer(user_pay_train_path)
    split_time = time.strptime(split_data, '%Y-%m-%d')
    for row in user_pay_reader:
        row_time = time.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        if row_time.tm_year >= split_time.tm_year and row_time.tm_mon >= split_time.tm_mon and row_time.tm_mday >= split_time.tm_mday:
            key = (row[1], row_time.tm_year, row_time.tm_mon, row_time.tm_mday, row_time.tm_wday)
            date_count.setdefault(key, 0)
            date_count[key] += 1
        else:
            user_pay_train_writer.write(row)
    for key, count in date_count.items():
        row = list(key) + [count]
        test_writer.write(row)

if __name__ == '__main__':
    main()
