import tool
import configure
from workflow import Work


@tool.state
def generate_recurrence_data(user_pay_list_path: str, recurrence_data_path: str, week_window: int):
    user_pay_list_reader = tool.Reader(user_pay_list_path)
    recurrence_data_writer = tool.Writer(recurrence_data_path)
    user_pay = user_pay_list_reader.read(numeric=True)
    for row in user_pay:
        data = row[1:]
        for i in range(len(data) // 7 - week_window - configure.predict_weeks + 1):
            offset = i * 7
            current_data = data[offset: offset + (week_window + configure.predict_weeks) * 7]
            recurrence_data_writer.write_row([row[0]] + current_data)


class GenerateRecurrenceData(Work):
    def function(self):
        return generate_recurrence_data
