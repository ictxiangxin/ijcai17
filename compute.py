def loss(real_data, test_data):
    shop_sum = len(real_data)
    day_sum = len(real_data[0])
    loss_value = 0
    for real, test in zip(real_data, test_data):
        for real_day, test_day in zip(real, test):
            try:
                loss_value += abs((real_day - test_day) / (real_day + test_day))
            except ZeroDivisionError:
                pass
    loss_value /= shop_sum * day_sum
    return loss_value


def median(data):
    data = sorted(data)
    size = len(data)
    if size == 0:
        m = 0
    elif size % 2 == 0:
        m = (data[size // 2] + data[size // 2 - 1]) / 2
    else:
        m = data[(size - 1) // 2]
    return m
