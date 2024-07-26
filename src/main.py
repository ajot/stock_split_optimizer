from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from .env file
stock1_name = os.getenv("STOCK1_NAME")
stock1_price = float(os.getenv("STOCK1_PRICE"))
stock1_shares = int(os.getenv("STOCK1_SHARES"))
stock2_name = os.getenv("STOCK2_NAME")
stock2_price = float(os.getenv("STOCK2_PRICE"))
stock2_shares = int(os.getenv("STOCK2_SHARES"))
tax_percentage = float(os.getenv("TAX_PERCENTAGE"))
target_amount = float(os.getenv("TARGET_AMOUNT"))
opening_message = os.getenv("OPENING_MESSAGE")

def calculate_sales(stock1_name, stock1_price, stock1_shares, stock2_name, stock2_price, stock2_shares, tax_percentage, target_amount):
    # Convert tax percentage to a decimal
    tax_rate = tax_percentage / 100

    # Dictionaries to store possible combinations
    stock1_combinations = {}
    stock2_combinations = {}
    balanced_recommendations = []

    # Stock 1 combinations first
    for percentage in range(10, 110, 10):
        shares_to_sell1 = round((percentage / 100) * stock1_shares)
        net_value_stock1 = shares_to_sell1 * stock1_price * (1 - tax_rate)

        remaining_target = target_amount - net_value_stock1
        if remaining_target <= 0:
            stock1_combinations[percentage] = (shares_to_sell1, 0, percentage, 0, net_value_stock1, 0, True)
            continue

        shares_to_sell2_needed = round(remaining_target / (stock2_price * (1 - tax_rate)))
        percentage2_needed = min((shares_to_sell2_needed / stock2_shares) * 100, 100)
        sufficient = shares_to_sell2_needed <= stock2_shares

        net_value_stock2 = shares_to_sell2_needed * stock2_price * (1 - tax_rate)
        stock1_combinations[percentage] = (shares_to_sell1, min(shares_to_sell2_needed, stock2_shares), percentage, percentage2_needed, net_value_stock1, net_value_stock2, sufficient)
        if sufficient and abs(percentage - percentage2_needed) <= 10:
            total_net_value = net_value_stock1 + net_value_stock2
            balanced_recommendations.append((shares_to_sell1, shares_to_sell2_needed, percentage, percentage2_needed, net_value_stock1, net_value_stock2, total_net_value))

    # Stock 2 combinations
    for percentage in range(10, 110, 10):
        shares_to_sell2 = round((percentage / 100) * stock2_shares)
        net_value_stock2 = shares_to_sell2 * stock2_price * (1 - tax_rate)

        remaining_target = target_amount - net_value_stock2
        if remaining_target <= 0:
            stock2_combinations[percentage] = (0, shares_to_sell2, 0, percentage, 0, net_value_stock2, True)
            continue

        shares_to_sell1_needed = round(remaining_target / (stock1_price * (1 - tax_rate)))
        percentage1_needed = min((shares_to_sell1_needed / stock1_shares) * 100, 100)
        sufficient = shares_to_sell1_needed <= stock1_shares

        net_value_stock1 = shares_to_sell1_needed * stock1_price * (1 - tax_rate)
        stock2_combinations[percentage] = (min(shares_to_sell1_needed, stock1_shares), shares_to_sell2, percentage1_needed, percentage, net_value_stock1, net_value_stock2, sufficient)
        if sufficient and abs(percentage1_needed - percentage) <= 10:
            total_net_value = net_value_stock1 + net_value_stock2
            balanced_recommendations.append((shares_to_sell1_needed, shares_to_sell2, percentage1_needed, percentage, net_value_stock1, net_value_stock2, total_net_value))

    # Print balanced recommendations
    separator = "-" * 70
    print("\n" + separator)
    print("✅ Recommended balanced sales combinations:")
    print(separator)
    for i, (shares1, shares2, percent1, percent2, net_value1, net_value2, total_net_value) in enumerate(balanced_recommendations, 1):
        print(f"{i}. Stock 1: {percent1:.2f}% {stock1_name} ({shares1} shares, ${net_value1:,.2f}) + {percent2:.2f}% of {stock2_name} ({shares2} shares, ${net_value2:,.2f}) - Total Net Value: ${total_net_value:,.2f} 💰")

    # Output other combinations
    print("\n" + separator)
    print(f"📉 Combinations starting with smaller percentages of {stock1_name} sales:")
    print(separator)
    for i, (percentage, comb) in enumerate(stock1_combinations.items(), 1):
        shares1, shares2, percent1, percent2, net_value1, net_value2, sufficient = comb
        if sufficient:
            print(f"{i}. Stock 1: {percent1:.2f}% {stock1_name} ({shares1} shares, ${net_value1:,.2f}) + {percent2:.2f}% of {stock2_name} ({shares2} shares, ${net_value2:,.2f}) - Net Value: ${net_value1 + net_value2:,.2f}")
        else:
            print(f"{i}. Stock 1: {percent1:.2f}% {stock1_name} ({shares1} shares) + {percent2:.2f}% of {stock2_name} ({shares2} shares) - Insufficient to meet target")

    print("\n" + separator)
    print(f"📈 Combinations starting with smaller percentages of {stock2_name} sales:")
    print(separator)
    for i, (percentage, comb) in enumerate(stock2_combinations.items(), 1):
        shares1, shares2, percent1, percent2, net_value1, net_value2, sufficient = comb
        if sufficient:
            print(f"{i}. Stock 2: {percent2:.2f}% {stock2_name} ({shares2} shares, ${net_value2:,.2f}) + {percent1:.2f}% of {stock1_name} ({shares1} shares, ${net_value1:,.2f}) - Net Value: ${net_value1 + net_value2:,.2f}")
        else:
            print(f"{i}. Stock 2: {percent2:.2f}% {stock2_name} ({shares2} shares) + {percent1:.2f}% of {stock1_name} ({shares1} shares) - Insufficient to meet target")

# Print the opening message
print(opening_message)

# Example usage
calculate_sales(stock1_name, stock1_price, stock1_shares, stock2_name, stock2_price, stock2_shares, tax_percentage, target_amount)
