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
opening_title = os.getenv("OPENING_TITLE")
opening_message = os.getenv("OPENING_MESSAGE")

# ANSI escape codes for text colors
COLOR_RESET = "\033[0m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_RED = "\033[91m"  # For highlighting the best option
COLOR_GRAY = "\033[90m"  # Subtle gray color for opening messages
HIGHLIGHT_TITLE = "\033[1;4;91m"  # Bold and underline in red

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

    # Find the best balanced recommendation by minimizing the difference between percentages
    if balanced_recommendations:
        best_combination = min(balanced_recommendations, key=lambda x: abs(x[2] - x[3]))
    else:
        best_combination = None

    # Print balanced recommendations
    separator = "-" * 70
    print(f"{HIGHLIGHT_TITLE}{opening_title}{COLOR_RESET}\n")
    print(f"{COLOR_GRAY}{opening_message}{COLOR_RESET}\n{separator}")

    print(f"{COLOR_GREEN}✅ Recommended balanced sales combinations:{COLOR_RESET}")
    print(separator)
    for i, (shares1, shares2, percent1, percent2, net_value1, net_value2, total_net_value) in enumerate(balanced_recommendations, 1):
        if (shares1, shares2, percent1, percent2, net_value1, net_value2, total_net_value) == best_combination:
            highlight = COLOR_GREEN
        else:
            highlight = COLOR_RESET
        print(f"{highlight}{i}. Stock 1: {percent1:.2f}% {stock1_name} ({shares1} shares, ${net_value1:,.2f}) + {percent2:.2f}% of {stock2_name} ({shares2} shares, ${net_value2:,.2f}) - Total Net Value: ${total_net_value:,.2f}{COLOR_RESET}")

    # Output other combinations
    print("\n" + separator)
    print(f"{COLOR_BLUE}📉 Combinations starting with smaller percentages of {stock1_name} sales:{COLOR_RESET}")
    print(separator)
    best_stock1_combination = min(stock1_combinations.values(), key=lambda x: abs(x[2] - x[3]) if x[6] else float('inf'))
    for i, (percentage, comb) in enumerate(stock1_combinations.items(), 1):
        shares1, shares2, percent1, percent2, net_value1, net_value2, sufficient = comb
        if comb == best_stock1_combination:
            highlight = COLOR_GREEN
        elif sufficient:
            highlight = COLOR_BLUE
        else:
            highlight = COLOR_YELLOW
        if sufficient:
            print(f"{highlight}{i}. Stock 1: {percent1:.2f}% {stock1_name} ({shares1} shares, ${net_value1:,.2f}) + {percent2:.2f}% of {stock2_name} ({shares2} shares, ${net_value2:,.2f}) - Net Value: ${net_value1 + net_value2:,.2f}{COLOR_RESET}")
        else:
            print(f"{highlight}{i}. Stock 1: {percent1:.2f}% {stock1_name} ({shares1} shares) + {percent2:.2f}% of {stock2_name} ({shares2} shares) - Insufficient to meet target{COLOR_RESET}")

    print("\n" + separator)
    print(f"{COLOR_BLUE}📈 Combinations starting with smaller percentages of {stock2_name} sales:{COLOR_RESET}")
    print(separator)
    best_stock2_combination = min(stock2_combinations.values(), key=lambda x: abs(x[2] - x[3]) if x[6] else float('inf'))
    for i, (percentage, comb) in enumerate(stock2_combinations.items(), 1):
        shares1, shares2, percent1, percent2, net_value1, net_value2, sufficient = comb
        if comb == best_stock2_combination:
            highlight = COLOR_GREEN
        elif sufficient:
            highlight = COLOR_BLUE
        else:
            highlight = COLOR_YELLOW
        if sufficient:
            print(f"{highlight}{i}. Stock 2: {percent2:.2f}% {stock2_name} ({shares2} shares, ${net_value2:,.2f}) + {percent1:.2f}% of {stock1_name} ({shares1} shares, ${net_value1:,.2f}) - Net Value: ${net_value1 + net_value2:,.2f}{COLOR_RESET}")
        else:
            print(f"{highlight}{i}. Stock 2: {percent2:.2f}% {stock2_name} ({shares2} shares) + {percent1:.2f}% of {stock1_name} ({shares1} shares) - Insufficient to meet target{COLOR_RESET}")

# Example usage
calculate_sales(stock1_name, stock1_price, stock1_shares, stock2_name, stock2_price, stock2_shares, tax_percentage, target_amount)
