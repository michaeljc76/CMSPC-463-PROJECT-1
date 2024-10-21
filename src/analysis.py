import csv
from datetime import datetime


# Parse CSV into list of dictionaries
def read_stock_data(file_name):
    stock_data = []
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stock_data.append({
                'Date': datetime.strptime(row['Date'], '%m/%d/%Y'),
                'Close': float(row['Close/Last'].replace('$', '')),
                'Volume': int(row['Volume']),
                'Open': float(row['Open'].replace('$', '')),
                'High': float(row['High'].replace('$', '')),
                'Low': float(row['Low'].replace('$', ''))
            })
    return stock_data


# Merge sort for CSV
def merge_sort(data, key):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], key)
    right = merge_sort(data[mid:], key)
    return merge(left, right, key)

# Merge helper function
def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] < right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Kadane's Algorithm for maximum profit
def max_profit_period(stock_data):
    max_profit = 0
    current_profit = 0
    start = end = temp_start = 0

    for i in range(1, len(stock_data)):
        daily_change = stock_data[i]['Close'] - stock_data[i - 1]['Close']
        if current_profit + daily_change > 0:
            current_profit += daily_change
        else:
            current_profit = 0
            temp_start = i

        if current_profit > max_profit:
            max_profit = current_profit
            start = temp_start
            end = i

    return stock_data[start:end + 1], max_profit

# Kadane's Algorithm for maximum loss
def max_loss_period(stock_data):
    max_loss = 0
    current_loss = 0
    start = end = temp = 0

    for i in range(1, len(stock_data)):
        daily_change = stock_data[i]['Close'] - stock_data[i - 1]['Close']

        current_loss += daily_change

        if current_loss > 0:
            current_loss = 0
            temp = i

        if current_loss < max_loss:
            max_loss = current_loss
            start = temp
            end = i

    return stock_data[start:end + 1], max_loss

# Divide and conquer closest pair algorithm points for anomaly detection (price similarity)
def closest_pair(stock_data):
    min_diff = float('inf')
    closest_pair = None
    for i in range(1, len(stock_data)):
        prev = stock_data[i - 1]['Close']
        curr = stock_data[i]['Close']
        diff = abs(curr - prev)
        if diff < min_diff:
            min_diff = diff
            closest_pair = (stock_data[i - 1], stock_data[i])
    return closest_pair

# Divide and conquer closest pair algorithm points for anomaly detection (price disparity)
def farthest_pair(stock_data):
    max_diff = 0
    anomaly_pair = None
    for i in range(1, len(stock_data)):
        prev = stock_data[i-1]['Close']
        curr = stock_data[i]['Close']
        diff = abs(curr - prev)
        if diff > max_diff:
            max_diff = diff
            anomaly_pair = (stock_data[i-1], stock_data[i])
    return anomaly_pair



# Main processing function
def process_stock_data(file_name):
    # Read the stock data
    stock_data = read_stock_data(file_name)

    # Merge sort the stock data
    sorted_data = merge_sort(stock_data, key='Date')

    # Maximum profit and loss (Kadane's algorithm)
    max_profit_data, max_profit = max_profit_period(sorted_data)
    max_loss_data, max_loss = max_loss_period(sorted_data)

    # Anomaly Detection (closest pair)
    closest_anomaly = closest_pair(sorted_data)
    farthest_anomaly = farthest_pair(sorted_data)

    # Output
    print(f"Max Profit Period: ${max_profit_data[0]['Close']} at {max_profit_data[0]['Date'].strftime('%m/%d/%Y')} to ${max_profit_data[len(max_profit_data)-1]['Close']} at {max_profit_data[len(max_profit_data)-1]['Date'].strftime('%m/%d/%Y')}")
    print(f"Max Profit: ${max_profit:.2f}")
    print(f"Max Loss Period: ${max_loss_data[0]['Close']} at {max_loss_data[0]['Date'].strftime('%m/%d/%Y')} to ${max_loss_data[len(max_loss_data)-1]['Close']} at {max_loss_data[len(max_loss_data)-1]['Date'].strftime('%m/%d/%Y')}")
    print(f"Max Loss: ${max_loss:.2f}")
    print(f"Closest Pair Anomaly: {closest_anomaly[0]['Date'].strftime('%m/%d/%Y')} - {closest_anomaly[1]['Date'].strftime('%m/%d/%Y')}, Difference: ${abs(closest_anomaly[1]['Close'] - closest_anomaly[0]['Close']):.2f}")
    print(f"Farthest Pair Anomaly: {farthest_anomaly[0]['Date'].strftime('%m/%d/%Y')} - {farthest_anomaly[1]['Date'].strftime('%m/%d/%Y')}, Difference: ${abs(farthest_anomaly[1]['Close'] - farthest_anomaly[0]['Close']):.2f}")

# Execute
process_stock_data('TSLA.csv')
