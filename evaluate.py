def loss(real_data, test_data):
    shop_sum = len(real_data)
    day_sum = len(real_data[0])
    loss_value = 0
    for real, test in zip(real_data, test_data):
        for real_day, test_day in zip(real, test):
            loss_value += abs((real_day - test_day) / (real_day + test_day))
    loss_value /= shop_sum * day_sum
