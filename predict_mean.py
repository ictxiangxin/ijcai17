import tool
from workflow import Work


@tool.state
def predict_mean(user_pay_count_path: str, result_path: str, train_weeks: int):
    shop_pay_list_reader = tool.Reader(user_pay_count_path)
    result_writer = tool.Writer(result_path)
    for row in shop_pay_list_reader:
        pay_list = row[1:]
        pay_list.reverse()
        result = []
        for d in range(7):
            offset = 0
            new_list = []
            while offset < len(pay_list) - train_weeks * 7:
                week_pays = [int(pay_list[-d + (w + 1) * 7 - 1 + offset]) for w in range(train_weeks)]
                for n in week_pays:
                    if n != 0:
                        new_list.append(n)
                if new_list:
                    break
                offset += 7
                new_list = []
            try:
                m = int(sum(new_list) / len(new_list))
            except ZeroDivisionError:
                m = 0
            result.append(m)
        result *= 2
        result_writer.write_row([row[0]] + result)


class PredictMean(Work):
    def function(self):
        return predict_mean
