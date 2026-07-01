def calculate_profit(price, transport_cost):
    return price - transport_cost

def recommend(best_option, current_price, future_price):
    if future_price > current_price:
        return f"Wait and sell at {best_option}"
    else:
        return f"Sell now at {best_option}"