import tool
import compute
from workflow import Work


@tool.state
def predict_median(user_pay_count_path: str, result_path: str, train_weeks: int):
    shop_pay_list_reader = tool.Reader(user_pay_count_path)
    result_writer = tool.Writer(result_path)
    for row in shop_pay_list_reader:
        pay_list = row[-train_weeks * 7:]
        pay_list.reverse()
        result = []
        for d in range(7):
            week_pays = [int(pay_list[-d + (w + 1) * 7 - 1]) for w in range(train_weeks)]
            m = int(compute.median(week_pays))
            result.append(m)
        result *= 2
        result_writer.write_row([row[0]] + result)


class PredictMedian(Work):
    def function(self):
        return predict_median
