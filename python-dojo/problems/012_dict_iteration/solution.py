def total_price(prices):
    total = 0
    for key, value in prices.items():
        total += value
    return total
