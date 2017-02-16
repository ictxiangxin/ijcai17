import tool
import compute
from workflow import Work


@tool.state
def predict_median(user_pay_list_path: str, result_path: str, train_weeks: int, offset: int=0):
    shop_pay_list_reader = tool.Reader(user_pay_list_path)
    result_writer = tool.Writer(result_path)
    for row in shop_pay_list_reader:
        pay_list = row[1:]
        pay_list.reverse()
        result = []
        for d in range(7):
            _offset = offset
            new_list = []
            while offset < len(pay_list) - train_weeks * 7:
                week_pays = [int(pay_list[-d + (w + 1) * 7 - 1 + _offset]) for w in range(train_weeks)]
                for n in week_pays:
                    if n != 0:
                        new_list.append(n)
                if new_list:
                    break
                _offset += 7
                new_list = []
            m = int(compute.median(new_list))
            result.append(m)
        result *= 2
        result_writer.write_row([row[0]] + result)


class PredictMedian(Work):
    def function(self):
        return predict_median
